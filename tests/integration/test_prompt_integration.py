"""Integration tests for prompt abstraction system."""

from unittest.mock import Mock, patch

import pytest

from mark_mate.core.enhanced_grader import EnhancedGradingSystem
from mark_mate.core.prompt_manager import PromptManager


class TestPromptIntegration:
    """Integration tests for the complete prompt abstraction system."""

    @pytest.fixture
    def sample_student_data(self):
        """Sample student submission data."""
        return {
            "student_id": "TEST123",
            "content": {
                "documents": [
                    {
                        "filename": "assignment.txt",
                        "text": "This is my assignment submission with detailed explanations.",
                    }
                ],
                "code": [
                    {
                        "filename": "main.py",
                        "content": "def hello():\n    print('Hello, World!')\n",
                        "language": "python",
                    }
                ],
            },
            "metadata": {
                "submission_time": "2025-01-01T10:00:00Z",
                "file_count": 2,
            },
        }

    @pytest.fixture
    def test_config(self):
        """Test configuration with prompts."""
        return {
            "grading": {
                "runs_per_grader": 1,
                "averaging_method": "mean",
                "parallel_execution": False,
            },
            "graders": [
                {
                    "name": "test-grader",
                    "provider": "anthropic",
                    "model": "claude-3-sonnet",
                    "weight": 1.0,
                    "primary_feedback": True,
                    "temperature": 0.1,
                    "max_tokens": 1000,
                }
            ],
            "execution": {
                "max_cost_per_student": 0.10,
                "timeout_per_run": 30,
                "retry_attempts": 1,
                "show_progress": False,
            },
            "prompts": {
                "default": {
                    "system": "You are a test grader.",
                    "template": """TEST ASSIGNMENT:
{assignment_spec}

RUBRIC:
{rubric}

STUDENT (ID: {student_id}):
{content_summary}

Please grade this submission out of {max_mark} marks.
{output_format}""",
                },
                "programming": {
                    "system": "You are a programming instructor.",
                    "template": """PROGRAMMING ASSIGNMENT:
{assignment_spec}

CODE SUBMISSION (Student: {student_id}):
{content_summary}

Evaluate the code quality and functionality.
{output_format}""",
                },
            },
            "prompt_sections": {
                "output_format": """Output Format: JSON with "mark", "feedback", "confidence" fields.""",
                "additional_instructions": {
                    "programming": "Focus on code structure and logic.",
                    "general": "Focus on content and presentation.",
                },
            },
        }

    def test_prompt_manager_initialization_with_config(self, test_config):
        """Test PromptManager initialization with configuration."""
        prompt_config = {
            "prompts": test_config["prompts"],
            "prompt_sections": test_config["prompt_sections"],
        }

        manager = PromptManager(prompt_config)

        assert "default" in manager.prompts
        assert "programming" in manager.prompts
        assert "output_format" in manager.prompt_sections

    def test_prompt_building_with_student_data(self, test_config, sample_student_data):
        """Test building prompts with real student data."""
        prompt_config = {
            "prompts": test_config["prompts"],
            "prompt_sections": test_config["prompt_sections"],
        }

        manager = PromptManager(prompt_config)

        result = manager.build_grading_prompt(
            student_data=sample_student_data,
            assignment_spec="Create a Python program that prints hello world",
            rubric="Functionality (50%), Code quality (30%), Documentation (20%)",
            max_mark=100,
        )

        assert "system" in result
        assert "user" in result
        assert "TEST123" in result["user"]
        assert "Python program" in result["user"]
        assert "DOCUMENTS: 1 files" in result["user"]
        assert "CODE FILES: 1 files" in result["user"]

    def test_assignment_type_detection(self, test_config, sample_student_data):
        """Test assignment type detection and template selection."""
        prompt_config = {
            "prompts": test_config["prompts"],
            "prompt_sections": test_config["prompt_sections"],
        }

        manager = PromptManager(prompt_config)

        # Test with explicit programming assignment type
        result = manager.build_grading_prompt(
            student_data=sample_student_data,
            assignment_spec="Programming assignment",
            rubric="Code quality",
            max_mark=100,
            assignment_type="programming",  # Explicitly specify programming type
        )

        # Should use programming template when assignment_type is specified
        assert "PROGRAMMING ASSIGNMENT:" in result["user"]

        # Test fallback to default when no assignment_type specified
        result_default = manager.build_grading_prompt(
            student_data=sample_student_data,
            assignment_spec="Programming assignment",
            rubric="Code quality",
            max_mark=100,
            # No assignment_type specified - should use default
        )

        # Should use default template
        assert "TEST ASSIGNMENT:" in result_default["user"]

    def test_wordpress_assignment_detection(self, test_config):
        """Test WordPress assignment type detection."""
        wordpress_data = {
            "student_id": "WP123",
            "content": {
                "wordpress_themes": {"files_found": ["style.css", "index.php"]},
                "wordpress_plugins": {"files_found": ["plugin1.php"]},
            },
        }

        # Add WordPress template to config
        test_config["prompts"]["wordpress"] = {
            "system": "You are a WordPress expert.",
            "template": "WORDPRESS SITE: {content_summary}",
        }

        prompt_config = {
            "prompts": test_config["prompts"],
            "prompt_sections": test_config["prompt_sections"],
        }

        manager = PromptManager(prompt_config)

        result = manager.build_grading_prompt(
            student_data=wordpress_data,
            assignment_spec="WordPress assignment",
            rubric="Theme and plugin quality",
            max_mark=100,
            assignment_type="wordpress",
        )

        assert result["system"] == "You are a WordPress expert."
        assert "WORDPRESS SITE:" in result["user"]

    def test_placeholder_substitution_completeness(
        self, test_config, sample_student_data
    ):
        """Test that all standard placeholders are properly substituted."""
        prompt_config = {
            "prompts": test_config["prompts"],
            "prompt_sections": test_config["prompt_sections"],
        }

        manager = PromptManager(prompt_config)

        result = manager.build_grading_prompt(
            student_data=sample_student_data,
            assignment_spec="Test assignment spec",
            rubric="Test rubric criteria",
            max_mark=85,
        )

        user_prompt = result["user"]

        # Check that all placeholders were substituted
        assert "{assignment_spec}" not in user_prompt
        assert "{rubric}" not in user_prompt
        assert "{student_id}" not in user_prompt
        assert "{content_summary}" not in user_prompt
        assert "{max_mark}" not in user_prompt
        assert "{output_format}" not in user_prompt

        # Check that values were properly inserted
        assert "Test assignment spec" in user_prompt
        assert "Test rubric criteria" in user_prompt
        assert "TEST123" in user_prompt
        assert "85" in user_prompt

    @patch("mark_mate.core.llm_provider.LLMProvider")
    def test_enhanced_grader_prompt_integration(
        self, mock_llm_provider, test_config, sample_student_data
    ):
        """Test that EnhancedGradingSystem properly uses PromptManager."""
        # Mock the LLM provider response
        mock_provider_instance = Mock()
        mock_provider_instance.get_available_providers.return_value = ["anthropic"]
        mock_provider_instance.grade_submission.return_value = {
            "success": True,
            "content": '{"mark": 85, "feedback": "Good work", "confidence": 0.9}',
            "usage": {
                "cost": 0.05,
                "response_time": 2.5,
                "input_tokens": 100,
                "output_tokens": 50,
            },
            "timestamp": "2025-01-01T10:00:00Z",
        }
        mock_llm_provider.return_value = mock_provider_instance

        # Mock the config manager to return our test config
        with patch(
            "mark_mate.config.grading_config.GradingConfigManager"
        ) as mock_config_manager:
            mock_manager = Mock()
            mock_manager.load_config.return_value = Mock()
            mock_manager.filter_graders_by_availability.return_value = Mock()
            mock_config_manager.return_value = mock_manager

            # Create the grading system (this tests the integration)
            grader = EnhancedGradingSystem()

            # Verify that the grader has a prompt manager
            assert hasattr(grader, "prompt_manager")
            assert grader.prompt_manager is not None

    def test_prompt_sections_composition(self, test_config):
        """Test that prompt sections are properly composed."""
        prompt_config = {
            "prompts": test_config["prompts"],
            "prompt_sections": test_config["prompt_sections"],
        }

        manager = PromptManager(prompt_config)

        # Test getting prompt sections for different assignment types
        sections = manager._get_prompt_sections("programming")
        assert "output_format" in sections
        assert (
            sections["output_format"]
            == 'Output Format: JSON with "mark", "feedback", "confidence" fields.'
        )

        sections = manager._get_prompt_sections("general")
        assert "additional_instructions" in sections

    def test_error_handling_invalid_template(self, test_config):
        """Test error handling with invalid template structure."""
        # Create config with invalid template (missing 'template' field)
        invalid_config = {
            "prompts": {
                "invalid": {
                    "system": "Test system",
                    # Missing 'template' field
                }
            },
            "prompt_sections": {},
        }

        with pytest.raises(ValueError, match="missing required 'template' field"):
            PromptManager(invalid_config)

    def test_fallback_to_default_prompt(self, test_config):
        """Test fallback behavior when requested prompt doesn't exist."""
        prompt_config = {
            "prompts": test_config["prompts"],
            "prompt_sections": test_config["prompt_sections"],
        }

        manager = PromptManager(prompt_config)

        # Request non-existent prompt
        template = manager.get_prompt_template("nonexistent")

        # Should fall back to default
        assert template.system == "You are a test grader."
