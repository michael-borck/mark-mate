"""
MarkMate Enhanced Grading System

Advanced multi-provider grading with statistical aggregation, confidence scoring,
and comprehensive error handling using LiteLLM unified interface.
"""

import os
import json
import logging
import asyncio
import concurrent.futures
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from statistics import mean, median, stdev
import time
import re

from .llm_provider import LLMProvider
from ..config.grading_config import GradingConfigManager, GradingConfig, GraderConfig

logger = logging.getLogger(__name__)


class EnhancedGradingSystem:
    """Enhanced grading system with multi-run capability and statistical aggregation."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the enhanced grading system.
        
        Args:
            config_path: Path to YAML configuration file
        """
        self.config_manager = GradingConfigManager()
        self.config = self.config_manager.load_config(config_path)
        self.llm_provider = LLMProvider()
        
        # Filter graders by available providers
        available_providers = self.llm_provider.get_available_providers()
        self.config = self.config_manager.filter_graders_by_availability(
            self.config, available_providers
        )
        
        # Session tracking
        self.session_stats = {
            'total_students': 0,
            'successful_grades': 0,
            'failed_grades': 0,
            'total_api_calls': 0,
            'total_cost': 0.0,
            'start_time': None,
            'end_time': None
        }
    
    def grade_submission(self, student_data: Dict[str, Any], assignment_spec: str, 
                        rubric: Optional[str] = None, 
                        max_cost_override: Optional[float] = None) -> Dict[str, Any]:
        """
        Grade a single student submission using the enhanced multi-grader system.
        
        Args:
            student_data: Extracted content and metadata for the student
            assignment_spec: Assignment specification/requirements
            rubric: Optional separate rubric
            max_cost_override: Override the default max cost per student
            
        Returns:
            Dictionary containing comprehensive grading results
        """
        student_id = student_data.get("student_id", "unknown")
        
        if not self.session_stats['start_time']:
            self.session_stats['start_time'] = datetime.now()
        
        logger.info(f"Starting enhanced grading for student {student_id}")
        
        result = {
            "student_id": student_id,
            "timestamp": datetime.now().isoformat(),
            "config": {
                "runs_per_grader": self.config.runs_per_grader,
                "averaging_method": self.config.averaging_method,
                "graders_used": [g.name for g in self.config.graders]
            },
            "grader_results": {},
            "aggregate": {},
            "metadata": {
                "total_runs": 0,
                "successful_runs": 0,
                "failed_runs": 0,
                "total_cost": 0.0,
                "processing_time": 0.0,
                "errors": []
            }
        }
        
        # Extract rubric if not provided
        if not rubric:
            rubric = self._extract_rubric(assignment_spec)
        
        # Build grading prompt
        grading_prompt = self._build_grading_prompt(student_data, assignment_spec, rubric)
        
        # Check cost constraints
        max_cost = max_cost_override or self.config.max_cost_per_student
        estimated_cost = self._estimate_total_cost(grading_prompt)
        
        if estimated_cost > max_cost:
            logger.warning(f"Estimated cost ${estimated_cost:.4f} exceeds limit ${max_cost:.4f}")
            result["metadata"]["errors"].append(
                f"Estimated cost ${estimated_cost:.4f} exceeds limit ${max_cost:.4f}"
            )
        
        # Process each grader
        start_time = time.time()
        
        for grader in self.config.graders:
            grader_result = self._process_grader(
                grader, grading_prompt, assignment_spec, max_cost
            )
            result["grader_results"][grader.name] = grader_result
            
            # Update metadata
            result["metadata"]["total_runs"] += grader_result["metadata"]["total_runs"]
            result["metadata"]["successful_runs"] += grader_result["metadata"]["successful_runs"]
            result["metadata"]["failed_runs"] += grader_result["metadata"]["failed_runs"]
            result["metadata"]["total_cost"] += grader_result["metadata"]["total_cost"]
            result["metadata"]["errors"].extend(grader_result["metadata"]["errors"])
        
        # Calculate processing time
        end_time = time.time()
        result["metadata"]["processing_time"] = end_time - start_time
        
        # Aggregate results
        result["aggregate"] = self._aggregate_all_results(result["grader_results"], assignment_spec)
        
        # Update session statistics
        self.session_stats['total_students'] += 1
        if result["aggregate"].get("mark", 0) > 0 or result["metadata"]["successful_runs"] > 0:
            self.session_stats['successful_grades'] += 1
        else:
            self.session_stats['failed_grades'] += 1
        
        self.session_stats['total_api_calls'] += result["metadata"]["total_runs"]
        self.session_stats['total_cost'] += result["metadata"]["total_cost"]
        
        logger.info(f"Completed grading for student {student_id}: "
                   f"{result['metadata']['successful_runs']}/{result['metadata']['total_runs']} runs, "
                   f"${result['metadata']['total_cost']:.4f}")
        
        return result
    
    def _process_grader(self, grader: GraderConfig, prompt: str, 
                       assignment_spec: str, max_cost: float) -> Dict[str, Any]:
        """Process multiple runs for a single grader."""
        grader_result = {
            "grader_name": grader.name,
            "provider": grader.provider,
            "model": grader.model,
            "weight": grader.weight,
            "runs": [],
            "aggregated": {},
            "metadata": {
                "total_runs": 0,
                "successful_runs": 0,
                "failed_runs": 0,
                "total_cost": 0.0,
                "average_response_time": 0.0,
                "errors": []
            }
        }
        
        successful_runs = []
        total_response_time = 0.0
        
        for run_number in range(self.config.runs_per_grader):
            # Check cost constraint
            if grader_result["metadata"]["total_cost"] >= max_cost:
                logger.warning(f"Cost limit reached for {grader.name}, stopping runs")
                break
            
            run_result = self._execute_single_run(
                grader, prompt, run_number + 1, assignment_spec
            )
            
            grader_result["runs"].append(run_result)
            grader_result["metadata"]["total_runs"] += 1
            
            if run_result["success"]:
                successful_runs.append(run_result)
                grader_result["metadata"]["successful_runs"] += 1
                total_response_time += run_result.get("response_time", 0)
            else:
                grader_result["metadata"]["failed_runs"] += 1
                grader_result["metadata"]["errors"].append(
                    f"Run {run_number + 1}: {run_result.get('error', 'Unknown error')}"
                )
            
            grader_result["metadata"]["total_cost"] += run_result.get("cost", 0.0)
        
        # Calculate average response time
        if successful_runs:
            grader_result["metadata"]["average_response_time"] = total_response_time / len(successful_runs)
        
        # Aggregate runs for this grader
        if successful_runs:
            grader_result["aggregated"] = self._aggregate_grader_runs(
                successful_runs, assignment_spec
            )
        else:
            grader_result["aggregated"] = {
                "mark": 0,
                "feedback": f"All runs failed for {grader.name}",
                "confidence": 0.0,
                "max_mark": self._extract_max_mark(assignment_spec)
            }
        
        return grader_result
    
    def _execute_single_run(self, grader: GraderConfig, prompt: str, 
                           run_number: int, assignment_spec: str) -> Dict[str, Any]:
        """Execute a single grading run."""
        try:
            # Add retry logic
            for attempt in range(self.config.retry_attempts):
                try:
                    llm_result = self.llm_provider.grade_submission(
                        provider=grader.provider,
                        model=grader.model,
                        prompt=prompt,
                        system_prompt=grader.system_prompt,
                        temperature=grader.temperature,
                        max_tokens=grader.max_tokens,
                        rate_limit=grader.rate_limit,
                        timeout=self.config.timeout_per_run
                    )
                    
                    if llm_result["success"]:
                        # Parse the grading response
                        parsed_result = self._parse_grading_response(
                            llm_result["content"], assignment_spec
                        )
                        
                        return {
                            "run_number": run_number,
                            "attempt": attempt + 1,
                            "success": True,
                            "mark": parsed_result["mark"],
                            "feedback": parsed_result["feedback"],
                            "max_mark": parsed_result["max_mark"],
                            "response_time": llm_result["usage"]["response_time"],
                            "cost": llm_result["usage"]["cost"],
                            "token_usage": {
                                "input_tokens": llm_result["usage"]["input_tokens"],
                                "output_tokens": llm_result["usage"]["output_tokens"]
                            },
                            "timestamp": llm_result["timestamp"]
                        }
                    else:
                        if attempt == self.config.retry_attempts - 1:
                            # Last attempt failed
                            raise Exception(llm_result.get("error", "LLM call failed"))
                        else:
                            logger.warning(f"Attempt {attempt + 1} failed for {grader.name} run {run_number}, retrying...")
                            time.sleep(2 ** attempt)  # Exponential backoff
                
                except Exception as e:
                    if attempt == self.config.retry_attempts - 1:
                        logger.error(f"All attempts failed for {grader.name} run {run_number}: {e}")
                        return {
                            "run_number": run_number,
                            "attempt": attempt + 1,
                            "success": False,
                            "error": str(e),
                            "cost": 0.0,
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        logger.warning(f"Attempt {attempt + 1} failed, retrying: {e}")
                        time.sleep(2 ** attempt)
        
        except Exception as e:
            logger.error(f"Unexpected error in {grader.name} run {run_number}: {e}")
            return {
                "run_number": run_number,
                "success": False,
                "error": str(e),
                "cost": 0.0,
                "timestamp": datetime.now().isoformat()
            }
    
    def _aggregate_grader_runs(self, successful_runs: List[Dict[str, Any]], 
                              assignment_spec: str) -> Dict[str, Any]:
        """Aggregate multiple runs from a single grader."""
        marks = [run["mark"] for run in successful_runs]
        feedbacks = [run["feedback"] for run in successful_runs]
        
        # Calculate aggregated mark
        if self.config.averaging_method == "mean":
            aggregated_mark = mean(marks)
        elif self.config.averaging_method == "median":
            aggregated_mark = median(marks)
        elif self.config.averaging_method == "trimmed_mean":
            # Remove highest and lowest, then take mean
            if len(marks) > 2:
                sorted_marks = sorted(marks)
                trimmed_marks = sorted_marks[1:-1]
                aggregated_mark = mean(trimmed_marks) if trimmed_marks else mean(marks)
            else:
                aggregated_mark = mean(marks)
        else:  # Default to mean
            aggregated_mark = mean(marks)
        
        # Calculate confidence based on consistency
        if len(marks) > 1:
            mark_std = stdev(marks)
            max_mark = self._extract_max_mark(assignment_spec)
            confidence = max(0.1, 1.0 - (mark_std / max_mark))
        else:
            confidence = 0.7  # Lower confidence for single run
        
        # Combine feedback (use most detailed one)
        primary_feedback = max(feedbacks, key=len)
        
        return {
            "mark": round(aggregated_mark, 1),
            "feedback": primary_feedback,
            "confidence": round(confidence, 3),
            "max_mark": self._extract_max_mark(assignment_spec),
            "run_marks": marks,
            "mark_std_dev": round(stdev(marks), 2) if len(marks) > 1 else 0.0,
            "runs_used": len(successful_runs)
        }
    
    def _aggregate_all_results(self, grader_results: Dict[str, Any], 
                              assignment_spec: str) -> Dict[str, Any]:
        """Aggregate results from all graders."""
        # Extract aggregated results from each grader
        grader_aggregates = []
        weights = []
        
        for grader_name, grader_result in grader_results.items():
            if grader_result["metadata"]["successful_runs"] > 0:
                grader_aggregates.append(grader_result["aggregated"])
                weights.append(grader_result["weight"])
        
        if not grader_aggregates:
            return {
                "mark": 0,
                "feedback": "No successful grading runs",
                "confidence": 0.0,
                "max_mark": self._extract_max_mark(assignment_spec),
                "grader_marks": [],
                "final_method": "failed"
            }
        
        # Calculate weighted average
        marks = [result["mark"] for result in grader_aggregates]
        
        if self.config.averaging_method == "weighted_mean":
            weighted_sum = sum(mark * weight for mark, weight in zip(marks, weights))
            total_weight = sum(weights)
            final_mark = weighted_sum / total_weight
        else:
            # Use the same method as individual grader aggregation
            if self.config.averaging_method == "median":
                final_mark = median(marks)
            elif self.config.averaging_method == "trimmed_mean" and len(marks) > 2:
                sorted_marks = sorted(marks)
                trimmed_marks = sorted_marks[1:-1]
                final_mark = mean(trimmed_marks) if trimmed_marks else mean(marks)
            else:
                final_mark = mean(marks)
        
        # Calculate overall confidence
        mark_std = stdev(marks) if len(marks) > 1 else 0
        max_mark = self._extract_max_mark(assignment_spec)
        base_confidence = max(0.3, 1.0 - (mark_std / max_mark))
        
        # Boost confidence based on number of successful graders
        grader_bonus = min(0.2, len(grader_aggregates) * 0.05)
        final_confidence = min(0.95, base_confidence + grader_bonus)
        
        # Get primary feedback (from primary_feedback grader if available)
        primary_feedback = ""
        for grader_name, grader_result in grader_results.items():
            grader_config = next((g for g in self.config.graders if g.name == grader_name), None)
            if grader_config and grader_config.primary_feedback and grader_result["metadata"]["successful_runs"] > 0:
                primary_feedback = grader_result["aggregated"]["feedback"]
                break
        
        # If no primary feedback grader, use the most detailed feedback
        if not primary_feedback and grader_aggregates:
            primary_feedback = max(grader_aggregates, key=lambda x: len(x["feedback"]))["feedback"]
        
        return {
            "mark": round(final_mark, 1),
            "feedback": primary_feedback,
            "confidence": round(final_confidence, 3),
            "max_mark": max_mark,
            "grader_marks": marks,
            "mark_std_dev": round(mark_std, 2),
            "final_method": self.config.averaging_method,
            "graders_used": len(grader_aggregates),
            "total_runs": sum(gr["metadata"]["total_runs"] for gr in grader_results.values())
        }
    
    def _build_grading_prompt(self, student_data: Dict[str, Any], assignment_spec: str, 
                             rubric: str) -> str:
        """Build the grading prompt for LLM providers."""
        student_id = student_data.get("student_id", "unknown")
        content = student_data.get("content", {})
        
        # Serialize content for the prompt
        content_summary = self._summarize_content(content)
        
        prompt = f"""
You are an expert academic grader evaluating a student submission. Please provide a detailed assessment.

ASSIGNMENT SPECIFICATION:
{assignment_spec}

GRADING RUBRIC:
{rubric}

STUDENT SUBMISSION (Student ID: {student_id}):
{content_summary}

Please provide your assessment in the following format:

MARK: [numerical mark out of total possible marks]
FEEDBACK: [detailed constructive feedback explaining the mark, highlighting strengths and areas for improvement]

Be fair, consistent, and constructive in your evaluation. Consider all aspects of the submission including technical implementation, documentation quality, and adherence to requirements.
"""
        
        return prompt
    
    def _summarize_content(self, content: Dict[str, Any]) -> str:
        """Summarize extracted content for the grading prompt."""
        summary_parts = []
        
        # Document content
        if "documents" in content:
            summary_parts.append("DOCUMENTS:")
            for doc in content["documents"]:
                summary_parts.append(f"- {doc.get('filename', 'Unknown')}: {len(doc.get('text', ''))} characters")
        
        # Code content
        if "code" in content:
            summary_parts.append("CODE FILES:")
            for code_file in content["code"]:
                summary_parts.append(f"- {code_file.get('filename', 'Unknown')}: {len(code_file.get('content', ''))} lines")
        
        # Web content
        if "web" in content:
            summary_parts.append("WEB FILES:")
            for web_file in content["web"]:
                summary_parts.append(f"- {web_file.get('filename', 'Unknown')}: {web_file.get('file_type', 'unknown')} file")
        
        # GitHub analysis
        if "github_analysis" in content:
            github = content["github_analysis"]
            summary_parts.append("GITHUB REPOSITORY:")
            summary_parts.append(f"- Commits: {github.get('total_commits', 0)}")
            summary_parts.append(f"- Development span: {github.get('development_span_days', 0)} days")
        
        # WordPress analysis
        if any(key.startswith("wordpress_") for key in content.keys()):
            summary_parts.append("WORDPRESS ANALYSIS:")
            for key, value in content.items():
                if key.startswith("wordpress_"):
                    component = key.replace("wordpress_", "")
                    summary_parts.append(f"- {component}: {len(value.get('files_found', []))} files")
        
        return "\n".join(summary_parts) if summary_parts else "No content extracted"
    
    def _extract_rubric(self, assignment_spec: str) -> str:
        """Extract rubric information from assignment specification."""
        # Look for common rubric patterns
        rubric_patterns = [
            r"(?i)rubric[:\s]*(.*?)(?=\n\n|\Z)",
            r"(?i)assessment criteria[:\s]*(.*?)(?=\n\n|\Z)",
            r"(?i)marking scheme[:\s]*(.*?)(?=\n\n|\Z)",
            r"(?i)grading[:\s]*(.*?)(?=\n\n|\Z)"
        ]
        
        for pattern in rubric_patterns:
            match = re.search(pattern, assignment_spec, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        # If no specific rubric found, return the whole assignment spec
        return assignment_spec
    
    def _extract_max_mark(self, assignment_spec: str) -> int:
        """Extract maximum mark from assignment specification."""
        # Look for patterns like "Total: 100", "out of 50", "marks: 30"
        mark_patterns = [
            r"(?i)total[:\s]*(\d+)",
            r"(?i)out of[:\s]*(\d+)",
            r"(?i)marks?[:\s]*(\d+)",
            r"(?i)points?[:\s]*(\d+)"
        ]
        
        for pattern in mark_patterns:
            match = re.search(pattern, assignment_spec)
            if match:
                return int(match.group(1))
        
        # Default to 100 if no max mark found
        return 100
    
    def _parse_grading_response(self, response_text: str, assignment_spec: str) -> Dict[str, Any]:
        """Parse LLM grading response into structured format."""
        result = {
            "mark": 0,
            "feedback": "",
            "max_mark": self._extract_max_mark(assignment_spec),
            "timestamp": datetime.now().isoformat()
        }
        
        # Extract mark
        mark_match = re.search(r"MARK[:\s]*(\d+(?:\.\d+)?)", response_text, re.IGNORECASE)
        if mark_match:
            result["mark"] = float(mark_match.group(1))
        
        # Extract feedback
        feedback_match = re.search(r"FEEDBACK[:\s]*(.*?)(?=\n\n|\Z)", response_text, re.IGNORECASE | re.DOTALL)
        if feedback_match:
            result["feedback"] = feedback_match.group(1).strip()
        else:
            # If no explicit feedback section, use the whole response
            result["feedback"] = response_text.strip()
        
        return result
    
    def _estimate_total_cost(self, prompt: str) -> float:
        """Estimate total cost for all grading runs."""
        total_cost = 0.0
        
        # Rough token estimation (characters / 4)
        input_tokens = len(prompt) // 4
        output_tokens = 500  # Estimated output
        
        for grader in self.config.graders:
            grader_cost = self.llm_provider.estimate_cost(
                grader.provider, grader.model, input_tokens, output_tokens
            )
            total_cost += grader_cost * self.config.runs_per_grader
        
        return total_cost
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of the current grading session."""
        self.session_stats['end_time'] = datetime.now()
        
        if self.session_stats['start_time']:
            duration = self.session_stats['end_time'] - self.session_stats['start_time']
            duration_seconds = duration.total_seconds()
        else:
            duration_seconds = 0
        
        # Get total usage from LLM provider
        usage_stats = self.llm_provider.get_total_usage()
        
        return {
            "session_stats": self.session_stats,
            "duration_seconds": duration_seconds,
            "usage_stats": usage_stats,
            "config_summary": {
                "graders": len(self.config.graders),
                "runs_per_grader": self.config.runs_per_grader,
                "averaging_method": self.config.averaging_method
            }
        }