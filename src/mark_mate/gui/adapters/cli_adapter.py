"""
CLI adapter for MarkMate GUI.

This module provides a bridge between the GUI interface and the existing CLI commands,
allowing the GUI to reuse all the core business logic while providing a better user experience.
"""

import asyncio
import logging
from typing import Any, Callable, Dict, Optional
from pathlib import Path

from ...cli import consolidate, scan, extract, grade, generate_config

logger = logging.getLogger(__name__)


class ProgressCallback:
    """Callback interface for reporting progress from CLI operations."""
    
    def __init__(self, update_fn: Callable[[str, float], None]):
        self.update_fn = update_fn
    
    def update(self, message: str, progress: float):
        """Update progress with message and percentage (0.0 to 1.0)."""
        self.update_fn(message, progress)


class CLIAdapter:
    """Adapter class to run CLI commands from the GUI with progress reporting."""
    
    def __init__(self):
        self.current_operation: Optional[str] = None
        self.is_running = False
    
    async def consolidate_async(
        self, 
        folder_path: str,
        output_dir: str = "processed_submissions",
        no_zip: bool = False,
        wordpress: bool = False,
        keep_mac_files: bool = False,
        progress_callback: Optional[Callable[[str, Optional[float]], None]] = None,
    ) -> Dict[str, Any]:
        """
        Run consolidate command asynchronously.
        
        Args:
            folder_path: Path to submissions folder
            output_dir: Output directory for processed submissions
            no_zip: Whether to discard zip files
            wordpress: Enable WordPress processing
            keep_mac_files: Keep Mac system files
            progress_callback: Progress reporting callback
            
        Returns:
            Dictionary with results and statistics
        """
        self.current_operation = "consolidate"
        self.is_running = True
        
        try:
            if progress_callback:
                progress_callback("Starting consolidation...", 10.0)
            
            # Create mock args object for CLI function
            class MockArgs:
                def __init__(self):
                    self.folder_path = folder_path
                    self.output_dir = output_dir
                    self.no_zip = no_zip
                    self.wordpress = wordpress
                    self.keep_mac_files = keep_mac_files
            
            args = MockArgs()
            
            if progress_callback:
                progress_callback("Processing submissions...", 50.0)
            
            # Run the consolidate command in a thread pool to avoid blocking
            result = await asyncio.get_event_loop().run_in_executor(
                None, consolidate.main, args
            )
            
            if progress_callback:
                progress_callback("Consolidation complete!", 100.0)
            
            return {
                "success": True,
                "result": result,
                "message": "Consolidation completed successfully",
            }
            
        except Exception as e:
            logger.error(f"Consolidate operation failed: {e}")
            if progress_callback:
                progress_callback(f"Error: {str(e)}", 0.0)
            
            return {
                "success": False,
                "error": str(e),
                "message": f"Consolidation failed: {str(e)}",
            }
        
        finally:
            self.is_running = False
            self.current_operation = None
    
    async def scan_async(
        self,
        submissions_folder: str,
        output: str = "github_urls.txt",
        encoding: str = "utf-8",
        progress_callback: Optional[Callable[[str, Optional[float]], None]] = None,
    ) -> Dict[str, Any]:
        """
        Run scan command asynchronously.
        
        Args:
            submissions_folder: Path to submissions folder
            output: Output file for GitHub URLs
            encoding: Text encoding to use
            progress_callback: Progress reporting callback
            
        Returns:
            Dictionary with results and statistics
        """
        self.current_operation = "scan"
        self.is_running = True
        
        try:
            if progress_callback:
                progress_callback("Starting URL scan...", 10.0)
            
            class MockArgs:
                def __init__(self):
                    self.submissions_folder = submissions_folder
                    self.output = output
                    self.encoding = encoding
            
            args = MockArgs()
            
            if progress_callback:
                progress_callback("Scanning for GitHub URLs...", 50.0)
            
            # Import scan function and run it
            from ...cli.scan import scan_submissions_folder, write_url_mapping
            
            # Run the actual scan
            student_urls = await asyncio.get_event_loop().run_in_executor(
                None, scan_submissions_folder, submissions_folder, encoding
            )
            
            if progress_callback:
                progress_callback("Writing results...", 80.0)
            
            # Write the mapping file
            await asyncio.get_event_loop().run_in_executor(
                None, write_url_mapping, student_urls, output
            )
            
            if progress_callback:
                progress_callback("Scan complete!", 100.0)
            
            # Calculate statistics
            total_students = len(student_urls)
            students_with_urls = len([s for s, urls in student_urls.items() if urls])
            total_urls = sum(len(urls) for urls in student_urls.values())
            
            return {
                "success": True,
                "urls_found": total_urls,
                "students_with_urls": students_with_urls,
                "total_students": total_students,
                "files_scanned": "multiple",  # CLI doesn't track individual file count
                "output_file": output,
                "message": f"Found {total_urls} URLs for {students_with_urls}/{total_students} students",
            }
            
        except Exception as e:
            logger.error(f"Scan operation failed: {e}")
            if progress_callback:
                progress_callback(f"Error: {str(e)}", 0.0)
            
            return {
                "success": False,
                "error": str(e),
                "message": f"Scan failed: {str(e)}",
            }
        
        finally:
            self.is_running = False
            self.current_operation = None
    
    async def extract_async(
        self,
        submissions_folder: str,
        output: str = "extracted_content.json",
        wordpress: bool = False,
        github_urls: Optional[str] = None,
        dry_run: bool = False,
        max_students: Optional[int] = None,
        progress_callback: Optional[Callable[[str, Optional[float]], None]] = None,
    ) -> Dict[str, Any]:
        """
        Run extract command asynchronously.
        
        Args:
            submissions_folder: Path to submissions folder
            output: Output JSON file
            wordpress: Enable WordPress processing
            github_urls: GitHub URL mapping file
            dry_run: Preview without extraction
            max_students: Limit number of students
            progress_callback: Progress reporting callback
            
        Returns:
            Dictionary with results and statistics
        """
        self.current_operation = "extract"
        self.is_running = True
        
        try:
            if progress_callback:
                progress_callback("Starting content extraction...", 10.0)
            
            class MockArgs:
                def __init__(self):
                    self.submissions_folder = submissions_folder
                    self.output = output
                    self.wordpress = wordpress
                    self.github_urls = github_urls
                    self.dry_run = dry_run
                    self.max_students = max_students
            
            args = MockArgs()
            
            if progress_callback:
                progress_callback("Extracting content...", 50.0)
            
            result = await asyncio.get_event_loop().run_in_executor(
                None, extract.main, args
            )
            
            if progress_callback:
                progress_callback("Extraction complete!", 100.0)
            
            return {
                "success": True,
                "result": result,
                "message": "Content extraction completed successfully",
            }
            
        except Exception as e:
            logger.error(f"Extract operation failed: {e}")
            if progress_callback:
                progress_callback(f"Error: {str(e)}", 0.0)
            
            return {
                "success": False,
                "error": str(e),
                "message": f"Extraction failed: {str(e)}",
            }
        
        finally:
            self.is_running = False
            self.current_operation = None
    
    async def grade_async(
        self,
        extracted_content: str,
        assignment_spec: str,
        output: str = "grading_results.json",
        rubric: Optional[str] = None,
        max_students: Optional[int] = None,
        dry_run: bool = False,
        config: Optional[str] = None,
        progress_callback: Optional[Callable[[str, Optional[float]], None]] = None,
    ) -> Dict[str, Any]:
        """
        Run grade command asynchronously.
        
        Args:
            extracted_content: Path to extracted content JSON
            assignment_spec: Path to assignment specification
            output: Output JSON file for results
            rubric: Optional separate rubric file
            max_students: Limit number of students
            dry_run: Preview without API calls
            config: Path to grading configuration
            progress_callback: Progress reporting callback
            
        Returns:
            Dictionary with results and statistics
        """
        self.current_operation = "grade"
        self.is_running = True
        
        try:
            if progress_callback:
                progress_callback("Starting grading process...", 10.0)
            
            class MockArgs:
                def __init__(self):
                    self.extracted_content = extracted_content
                    self.assignment_spec = assignment_spec
                    self.output = output
                    self.rubric = rubric
                    self.max_students = max_students
                    self.dry_run = dry_run
                    self.config = config
            
            args = MockArgs()
            
            if progress_callback:
                progress_callback("Running AI grading...", 50.0)
            
            result = await asyncio.get_event_loop().run_in_executor(
                None, grade.main, args
            )
            
            if progress_callback:
                progress_callback("Grading complete!", 100.0)
            
            return {
                "success": True,
                "result": result,
                "message": "Grading completed successfully",
            }
            
        except Exception as e:
            logger.error(f"Grade operation failed: {e}")
            if progress_callback:
                progress_callback(f"Error: {str(e)}", 0.0)
            
            return {
                "success": False,
                "error": str(e),
                "message": f"Grading failed: {str(e)}",
            }
        
        finally:
            self.is_running = False
            self.current_operation = None
    
    async def generate_config_async(
        self,
        output: str = "grading_config.yaml",
        template: str = "full",
        provider: Optional[str] = None,
        force: bool = False,
        progress_callback: Optional[Callable[[str, Optional[float]], None]] = None,
    ) -> Dict[str, Any]:
        """
        Run generate-config command asynchronously.
        
        Args:
            output: Output YAML file path
            template: Configuration template type
            provider: Single provider for single-provider template
            force: Overwrite existing file
            progress_callback: Progress reporting callback
            
        Returns:
            Dictionary with results and statistics
        """
        self.current_operation = "generate_config"
        self.is_running = True
        
        try:
            if progress_callback:
                progress_callback("Generating configuration...", 50.0)
            
            class MockArgs:
                def __init__(self):
                    self.output = output
                    self.template = template
                    self.provider = provider
                    self.force = force
            
            args = MockArgs()
            
            result = await asyncio.get_event_loop().run_in_executor(
                None, generate_config.main, args
            )
            
            if progress_callback:
                progress_callback("Configuration generated!", 100.0)
            
            return {
                "success": True,
                "result": result,
                "message": "Configuration generated successfully",
            }
            
        except Exception as e:
            logger.error(f"Generate config operation failed: {e}")
            if progress_callback:
                progress_callback(f"Error: {str(e)}", 0.0)
            
            return {
                "success": False,
                "error": str(e),
                "message": f"Configuration generation failed: {str(e)}",
            }
        
        finally:
            self.is_running = False
            self.current_operation = None
    
    def cancel_operation(self):
        """Cancel the current operation if possible."""
        if self.is_running:
            logger.info(f"Canceling operation: {self.current_operation}")
            # Note: This is a simple flag - more sophisticated cancellation
            # would require modifying the CLI functions to check for cancellation
            self.is_running = False