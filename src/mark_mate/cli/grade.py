#!/usr/bin/env python3
"""
MarkMate Grade Command

Automated grading using multiple LLM providers with comprehensive analysis integration.
"""

import argparse
import os
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def add_parser(subparsers) -> argparse.ArgumentParser:
    """Add grade command parser."""
    parser = subparsers.add_parser(
        "grade",
        help="Grade student submissions using AI",
        description="Automated grading using multiple LLM providers with comprehensive analysis"
    )
    
    parser.add_argument(
        "extracted_content",
        help="Path to extracted content JSON file (from extract command)"
    )
    
    parser.add_argument(
        "assignment_spec",
        help="Path to assignment specification/rubric file"
    )
    
    parser.add_argument(
        "--output",
        default="grading_results.json",
        help="Output JSON file for grading results (default: grading_results.json)"
    )
    
    parser.add_argument(
        "--rubric",
        help="Path to separate rubric file (optional, can be extracted from assignment spec)"
    )
    
    parser.add_argument(
        "--max-students",
        type=int,
        help="Maximum number of students to grade (for testing)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be graded without actually calling LLM APIs"
    )
    
    parser.add_argument(
        "--providers",
        nargs="+",
        choices=["claude", "openai", "gemini", "all"],
        default=["all"],
        help="LLM providers to use for grading (default: all available)"
    )
    
    parser.add_argument(
        "--config",
        help="Path to YAML grading configuration file"
    )
    
    parser.add_argument(
        "--enhanced",
        action="store_true",
        help="Use enhanced multi-run grading system with statistical aggregation"
    )
    
    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Number of runs per grader (only with --enhanced, default: 1)"
    )
    
    return parser


def load_extracted_content(content_file):
    """
    Load extracted content from JSON file.
    
    Args:
        content_file: Path to the extracted content JSON file
        
    Returns:
        Dictionary containing extracted content data
    """
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        if "students" not in content:
            raise ValueError("Invalid content file format: missing 'students' key")
        
        logger.info(f"Loaded content for {len(content['students'])} students")
        return content
        
    except Exception as e:
        logger.error(f"Error loading extracted content: {e}")
        raise


def load_assignment_spec(spec_file):
    """
    Load assignment specification/rubric.
    
    Args:
        spec_file: Path to the assignment specification file
        
    Returns:
        String containing the assignment specification
    """
    try:
        with open(spec_file, 'r', encoding='utf-8') as f:
            spec = f.read()
        
        logger.info(f"Loaded assignment specification from: {spec_file}")
        return spec
        
    except Exception as e:
        logger.error(f"Error loading assignment specification: {e}")
        raise


def check_api_keys(providers):
    """
    Check if required API keys are available.
    
    Args:
        providers: List of providers to check
        
    Returns:
        Dictionary indicating which providers are available
    """
    available = {}
    
    if "claude" in providers or "all" in providers:
        available["claude"] = bool(os.getenv("ANTHROPIC_API_KEY"))
        if not available["claude"]:
            logger.warning("ANTHROPIC_API_KEY not found - Claude grading will be disabled")
    
    if "openai" in providers or "all" in providers:
        available["openai"] = bool(os.getenv("OPENAI_API_KEY"))
        if not available["openai"]:
            logger.warning("OPENAI_API_KEY not found - OpenAI grading will be disabled")
    
    if "gemini" in providers or "all" in providers:
        available["gemini"] = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
        if not available["gemini"]:
            logger.warning("GEMINI_API_KEY or GOOGLE_API_KEY not found - Gemini grading will be disabled")
    
    return available


def grade_submission_legacy(student_data, assignment_spec, providers, rubric=None):
    """
    Grade a single student submission using legacy grading system.
    
    Args:
        student_data: Extracted content for the student
        assignment_spec: Assignment specification/rubric
        providers: List of providers to use
        rubric: Optional separate rubric
        
    Returns:
        Dictionary containing grading results
    """
    from ..core.grader import GradingSystem
    
    try:
        grader = GradingSystem()
        result = grader.grade_submission(
            student_data,
            assignment_spec,
            providers=providers,
            rubric=rubric
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error grading student {student_data.get('student_id', 'unknown')}: {e}")
        return {
            "error": str(e),
            "graded": False,
            "timestamp": datetime.now().isoformat()
        }


def grade_submission_enhanced(student_data, assignment_spec, grading_system, rubric=None):
    """
    Grade a single student submission using enhanced grading system.
    
    Args:
        student_data: Extracted content for the student
        assignment_spec: Assignment specification/rubric
        grading_system: EnhancedGradingSystem instance
        rubric: Optional separate rubric
        
    Returns:
        Dictionary containing grading results
    """
    try:
        result = grading_system.grade_submission(
            student_data,
            assignment_spec,
            rubric=rubric
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error grading student {student_data.get('student_id', 'unknown')}: {e}")
        return {
            "error": str(e),
            "graded": False,
            "timestamp": datetime.now().isoformat()
        }


def main(args) -> int:
    """Main grading logic."""
    content_file = args.extracted_content
    spec_file = args.assignment_spec
    output_file = args.output
    rubric_file = args.rubric
    max_students = args.max_students
    dry_run = args.dry_run
    providers = args.providers
    
    logger.info(f"Grading extracted content from: {content_file}")
    logger.info(f"Assignment specification: {spec_file}")
    if rubric_file:
        logger.info(f"Separate rubric file: {rubric_file}")
    if dry_run:
        logger.info("DRY RUN MODE - No API calls will be made")
    
    # Normalize providers list
    if "all" in providers:
        providers = ["claude", "openai", "gemini"]
    
    logger.info(f"Using providers: {', '.join(providers)}")
    
    # Determine grading mode
    enhanced_mode = args.enhanced or args.config
    if enhanced_mode:
        logger.info("Using Enhanced Multi-Run Grading System")
        if args.runs > 1:
            logger.info(f"Configured for {args.runs} runs per grader")
    else:
        logger.info("Using Legacy Single-Run Grading System")
    
    # Initialize grading system
    grading_system = None
    if enhanced_mode:
        try:
            from ..core.enhanced_grader import EnhancedGradingSystem
            
            # Create or modify config if using simple options
            config_path = args.config
            if not config_path and (args.runs > 1 or enhanced_mode):
                # Create temporary config
                from ..config.grading_config import GradingConfigManager
                config_manager = GradingConfigManager()
                temp_config = config_manager.DEFAULT_CONFIG.copy()
                temp_config['grading']['runs_per_grader'] = args.runs
                
                # Filter graders based on available providers
                available_graders = []
                for grader in temp_config['graders']:
                    if grader['provider'] in providers:
                        available_graders.append(grader)
                temp_config['graders'] = available_graders
                
                # Add Gemini if requested
                if 'gemini' in providers:
                    temp_config['graders'].append({
                        'name': 'gemini-pro',
                        'provider': 'gemini',
                        'model': 'gemini-1.5-pro',
                        'weight': 1.0,
                        'rate_limit': 60
                    })
                
                # Save temp config
                import tempfile
                import yaml
                with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
                    yaml.dump(temp_config, f)
                    config_path = f.name
            
            grading_system = EnhancedGradingSystem(config_path)
            logger.info(f"Initialized enhanced grading with {len(grading_system.config.graders)} graders")
            
        except Exception as e:
            logger.error(f"Failed to initialize enhanced grading system: {e}")
            logger.info("Falling back to legacy grading system")
            enhanced_mode = False
    
    # Check API keys for legacy mode or if enhanced mode failed
    if not enhanced_mode and not dry_run:
        available_providers = check_api_keys(providers)
        active_providers = [p for p, available in available_providers.items() if available]
        
        if not active_providers:
            logger.error("No API keys available for any selected providers")
            return 1
        
        if len(active_providers) < len(providers):
            logger.warning(f"Only {len(active_providers)} of {len(providers)} providers available")
        
        providers = active_providers
    
    # Load content and assignment spec
    try:
        content_data = load_extracted_content(content_file)
        assignment_spec = load_assignment_spec(spec_file)
        
        rubric = None
        if rubric_file:
            rubric = load_assignment_spec(rubric_file)  # Same loading logic
            
    except Exception as e:
        logger.error(f"Failed to load required files: {e}")
        return 1
    
    # Filter students if max_students is specified
    students = content_data["students"]
    if max_students:
        student_ids = list(students.keys())[:max_students]
        students = {sid: students[sid] for sid in student_ids}
        logger.info(f"Processing only first {len(students)} students")
    
    if dry_run:
        logger.info("DRY RUN - Would grade the following students:")
        for student_id in sorted(students.keys()):
            logger.info(f"  {student_id}")
        if enhanced_mode:
            logger.info(f"Enhanced mode - using {len(grading_system.config.graders)} configured graders")
        else:
            logger.info(f"Legacy mode - using providers: {', '.join(providers)}")
        return 0
    
    # Grade each student
    grading_results = {
        "grading_session": {
            "timestamp": datetime.now().isoformat(),
            "total_students": len(students),
            "grading_mode": "enhanced" if enhanced_mode else "legacy",
            "assignment_spec_file": spec_file,
            "rubric_file": rubric_file,
            "source_content_file": content_file
        },
        "results": {}
    }
    
    if enhanced_mode:
        grading_results["grading_session"]["config"] = {
            "graders": [g.name for g in grading_system.config.graders],
            "runs_per_grader": grading_system.config.runs_per_grader,
            "averaging_method": grading_system.config.averaging_method
        }
    else:
        grading_results["grading_session"]["providers"] = providers
    
    graded_count = 0
    for student_id, student_data in sorted(students.items()):
        logger.info(f"Grading student {student_id} ({graded_count + 1}/{len(students)})")
        
        if enhanced_mode:
            result = grade_submission_enhanced(
                student_data,
                assignment_spec,
                grading_system,
                rubric=rubric
            )
        else:
            result = grade_submission_legacy(
                student_data,
                assignment_spec,
                providers,
                rubric=rubric
            )
        
        grading_results["results"][student_id] = result
        graded_count += 1
    
    # Save results
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(grading_results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Grading complete!")
        logger.info(f"Graded {graded_count} students")
        logger.info(f"Results saved to: {output_file}")
        
        # Show summary statistics
        successful_grades = [r for r in grading_results["results"].values() if not r.get("error")]
        if successful_grades:
            logger.info(f"Successfully graded: {len(successful_grades)} students")
        
        # Show enhanced grading statistics if available
        if enhanced_mode and grading_system:
            session_summary = grading_system.get_session_summary()
            logger.info(f"Total API calls: {session_summary['session_stats']['total_api_calls']}")
            logger.info(f"Total cost: ${session_summary['session_stats']['total_cost']:.4f}")
            if session_summary['duration_seconds'] > 0:
                logger.info(f"Processing time: {session_summary['duration_seconds']:.1f} seconds")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error saving results: {e}")
        return 1