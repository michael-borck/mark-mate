"""
MarkMate: Your AI Teaching Assistant for Assignments and Assessment

A comprehensive system for processing, consolidating, and grading student submissions
with support for multiple content types, GitHub repository analysis, WordPress assignments,
and AI-powered assessment.
"""

__version__ = "0.1.0"
__author__ = "MarkMate Development Team"
__email__ = "dev@markmate.ai"

# Import main classes for library usage
from .core.grader import GradingSystem
from .core.enhanced_grader import EnhancedGradingSystem
from .core.llm_provider import LLMProvider
from .core.processor import AssignmentProcessor
from .core.analyzer import ContentAnalyzer
from .config.grading_config import GradingConfigManager

__all__ = [
    "GradingSystem", 
    "EnhancedGradingSystem",
    "LLMProvider",
    "AssignmentProcessor", 
    "ContentAnalyzer",
    "GradingConfigManager",
    "__version__"
]