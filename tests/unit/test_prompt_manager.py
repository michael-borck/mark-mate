"""Tests for the PromptManager class."""

import pytest

from mark_mate.core.prompt_manager import PromptManager, PromptTemplate


class TestPromptManager:
    """Test suite for PromptManager functionality."""

    @pytest.fixture
    def sample_prompt_config(self):
        """Sample prompt configuration for testing."""
        return {
            "prompts": {
                "default": {
                    "system": "You are an expert grader.",
                    "template": "Grade this: {assignment_spec}\nStudent: {student_id}\n{content_summary}",
                },
                "programming": {
                    "system": "You are a programming instructor.",
                    "template": "Code review: {assignment_spec}\nCode: {content_summary}",
                },
            },
            "prompt_sections": {
                "output_format": "Please provide JSON output.",
                "additional_instructions": {
                    "programming": "Focus on code quality.",
                    "general": "Focus on content quality.",
                },
            },
        }

    @pytest.fixture
    def prompt_manager(self, sample_prompt_config):
        """Create a PromptManager instance with sample config."""
        return PromptManager(sample_prompt_config)

    def test_init_with_valid_config(self, prompt_manager):
        """Test PromptManager initialization with valid config."""
        assert prompt_manager.prompts is not None
        assert prompt_manager.prompt_sections is not None
        assert "default" in prompt_manager.prompts

    def test_init_with_empty_config(self):
        """Test PromptManager initialization with empty config."""
        manager = PromptManager({})
        assert "default" in manager.prompts  # Should create fallback

    def test_get_prompt_template_default(self, prompt_manager):
        """Test getting default prompt template."""
        template = prompt_manager.get_prompt_template()
        assert isinstance(template, PromptTemplate)
        assert template.system == "You are an expert grader."
        assert "{assignment_spec}" in template.template

    def test_get_prompt_template_by_name(self, prompt_manager):
        """Test getting specific prompt template by name."""
        template = prompt_manager.get_prompt_template("programming")
        assert isinstance(template, PromptTemplate)
        assert template.system == "You are a programming instructor."
        assert "Code review:" in template.template

    def test_get_prompt_template_with_assignment_type(self, prompt_manager):
        """Test getting prompt template with assignment type preference."""
        template = prompt_manager.get_prompt_template(assignment_type="programming")
        assert template.system == "You are a programming instructor."

    def test_build_grading_prompt(self, prompt_manager):
        """Test building a complete grading prompt."""
        student_data = {
            "student_id": "123",
            "content": {
                "documents": [{"filename": "test.txt", "text": "Sample content"}]
            },
        }

        result = prompt_manager.build_grading_prompt(
            student_data=student_data,
            assignment_spec="Test assignment",
            rubric="Grade on accuracy",
            max_mark=100,
        )

        assert "system" in result
        assert "user" in result
        assert "Test assignment" in result["user"]
        assert "123" in result["user"]

    def test_placeholder_substitution_missing_values(self, prompt_manager):
        """Test placeholder substitution with missing values."""
        template = "Test {missing_placeholder} here"
        context = {"available": "value"}

        result = prompt_manager._substitute_placeholders(template, context)
        assert "[missing_placeholder not available]" in result

    def test_content_summary_generation(self, prompt_manager):
        """Test content summary generation."""
        content = {
            "documents": [
                {"filename": "doc1.txt", "text": "First document content"},
                {"filename": "doc2.txt", "text": "Second document content"},
            ],
            "code": [
                {
                    "filename": "script.py",
                    "content": "print('hello')",
                    "language": "python",
                }
            ],
        }

        summary = prompt_manager._generate_content_summary(content)
        assert "DOCUMENTS: 2 files" in summary
        assert "CODE FILES: 1 files" in summary
        assert "doc1.txt" in summary
        assert "script.py" in summary

    def test_list_available_prompts(self, prompt_manager):
        """Test listing available prompt templates."""
        prompts = prompt_manager.list_available_prompts()
        assert "default" in prompts
        assert "programming" in prompts
        assert len(prompts) == 2

    def test_validate_template(self, prompt_manager):
        """Test template validation."""
        assert prompt_manager.validate_template("default") is True
        assert prompt_manager.validate_template("programming") is True
        assert prompt_manager.validate_template("nonexistent") is False
