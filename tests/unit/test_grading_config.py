"""Tests for grading configuration management."""

import tempfile
from pathlib import Path

import pytest
import yaml

from mark_mate.config.grading_config import (
    GraderConfig,
    GradingConfig,
    GradingConfigManager,
)


class TestGraderConfig:
    """Test GraderConfig dataclass."""

    def test_grader_config_defaults(self):
        """Test GraderConfig with default values."""
        config = GraderConfig(
            name="test-grader",
            provider="anthropic",
            model="claude-3-sonnet",
        )

        assert config.name == "test-grader"
        assert config.provider == "anthropic"
        assert config.model == "claude-3-sonnet"
        assert config.weight == 1.0
        assert config.primary_feedback is False
        assert config.temperature == 0.1
        assert config.max_tokens == 2000

    def test_grader_config_custom_values(self):
        """Test GraderConfig with custom values."""
        config = GraderConfig(
            name="custom-grader",
            provider="openai",
            model="gpt-4",
            weight=2.5,
            primary_feedback=True,
            temperature=0.2,
            max_tokens=1500,
        )

        assert config.weight == 2.5
        assert config.primary_feedback is True
        assert config.temperature == 0.2
        assert config.max_tokens == 1500


class TestGradingConfig:
    """Test GradingConfig dataclass."""

    def test_grading_config_defaults(self):
        """Test GradingConfig with default values."""
        config = GradingConfig()

        assert config.runs_per_grader == 1
        assert config.averaging_method == "mean"
        assert config.parallel_execution is True
        assert config.max_cost_per_student == 1.0
        assert config.timeout_per_run == 60
        assert config.retry_attempts == 3
        assert config.show_progress is True
        assert len(config.graders) == 0
        assert isinstance(config.prompts, dict)
        assert isinstance(config.prompt_sections, dict)


class TestGradingConfigManager:
    """Test GradingConfigManager functionality."""

    @pytest.fixture
    def config_manager(self):
        """Create a GradingConfigManager instance."""
        return GradingConfigManager()

    @pytest.fixture
    def sample_config_dict(self):
        """Sample configuration dictionary."""
        return {
            "grading": {
                "runs_per_grader": 2,
                "averaging_method": "weighted_mean",
                "parallel_execution": True,
            },
            "graders": [
                {
                    "name": "claude-test",
                    "provider": "anthropic",
                    "model": "claude-3-sonnet",
                    "weight": 2.0,
                    "primary_feedback": True,
                },
                {
                    "name": "gpt-test",
                    "provider": "openai",
                    "model": "gpt-4",
                    "weight": 1.0,
                },
            ],
            "execution": {
                "max_cost_per_student": 0.75,
                "timeout_per_run": 45,
                "retry_attempts": 2,
            },
            "prompts": {
                "default": {
                    "system": "Test system prompt",
                    "template": "Test template with {placeholder}",
                }
            },
            "prompt_sections": {
                "test_section": "Test section content",
            },
        }

    def test_load_default_config(self, config_manager):
        """Test loading default configuration."""
        config = config_manager.load_config()

        assert isinstance(config, GradingConfig)
        assert len(config.graders) > 0
        assert "default" in config.prompts

    def test_load_config_from_dict(self, config_manager, sample_config_dict):
        """Test parsing configuration from dictionary."""
        config = config_manager._parse_config(sample_config_dict)

        assert config.runs_per_grader == 2
        assert config.averaging_method == "weighted_mean"
        assert len(config.graders) == 2
        assert config.graders[0].name == "claude-test"
        assert config.graders[0].weight == 2.0
        assert config.graders[0].primary_feedback is True
        assert config.graders[1].name == "gpt-test"
        assert config.graders[1].weight == 1.0
        assert config.max_cost_per_student == 0.75

    def test_load_config_from_file(self, config_manager, sample_config_dict):
        """Test loading configuration from YAML file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(sample_config_dict, f)
            temp_path = f.name

        try:
            config = config_manager.load_config(temp_path)
            assert config.runs_per_grader == 2
            assert len(config.graders) == 2
        finally:
            Path(temp_path).unlink()

    def test_load_config_nonexistent_file(self, config_manager):
        """Test loading configuration from nonexistent file."""
        config = config_manager.load_config("nonexistent.yaml")
        # Should fall back to defaults
        assert isinstance(config, GradingConfig)

    def test_validate_config_valid(self, config_manager, sample_config_dict):
        """Test configuration validation with valid config."""
        config = config_manager._parse_config(sample_config_dict)
        # Should not raise an exception
        config_manager._validate_config(config)

    def test_validate_config_no_graders(self, config_manager):
        """Test configuration validation with no graders."""
        config_dict = {
            "grading": {"runs_per_grader": 1},
            "graders": [],
            "execution": {},
        }

        with pytest.raises(ValueError, match="At least one grader must be configured"):
            config = config_manager._parse_config(config_dict)
            config_manager._validate_config(config)

    def test_validate_config_invalid_averaging_method(self, config_manager):
        """Test configuration validation with invalid averaging method."""
        config_dict = {
            "grading": {
                "runs_per_grader": 1,
                "averaging_method": "invalid_method",
            },
            "graders": [
                {
                    "name": "test",
                    "provider": "anthropic",
                    "model": "claude-3-sonnet",
                }
            ],
            "execution": {},
        }

        with pytest.raises(ValueError, match="Invalid averaging_method"):
            config = config_manager._parse_config(config_dict)
            config_manager._validate_config(config)

    def test_validate_config_invalid_provider(self, config_manager):
        """Test configuration validation with invalid provider."""
        config_dict = {
            "grading": {"runs_per_grader": 1},
            "graders": [
                {
                    "name": "test",
                    "provider": "invalid_provider",
                    "model": "some-model",
                }
            ],
            "execution": {},
        }

        with pytest.raises(ValueError, match="Invalid provider"):
            config = config_manager._parse_config(config_dict)
            config_manager._validate_config(config)

    def test_validate_config_multiple_primary_feedback(self, config_manager):
        """Test configuration validation with multiple primary feedback graders."""
        config_dict = {
            "grading": {"runs_per_grader": 1},
            "graders": [
                {
                    "name": "grader1",
                    "provider": "anthropic",
                    "model": "claude-3-sonnet",
                    "primary_feedback": True,
                },
                {
                    "name": "grader2",
                    "provider": "openai",
                    "model": "gpt-4",
                    "primary_feedback": True,
                },
            ],
            "execution": {},
        }

        with pytest.raises(
            ValueError, match="Only one grader can be marked as primary_feedback"
        ):
            config = config_manager._parse_config(config_dict)
            config_manager._validate_config(config)

    def test_filter_graders_by_availability(self, config_manager, sample_config_dict):
        """Test filtering graders by available providers."""
        config = config_manager._parse_config(sample_config_dict)
        available_providers = ["anthropic"]  # Only Anthropic available

        filtered_config = config_manager.filter_graders_by_availability(
            config, available_providers
        )

        assert len(filtered_config.graders) == 1
        assert filtered_config.graders[0].provider == "anthropic"

    def test_filter_graders_no_available_providers(
        self, config_manager, sample_config_dict
    ):
        """Test filtering graders with no available providers."""
        config = config_manager._parse_config(sample_config_dict)
        available_providers = []  # No providers available

        with pytest.raises(ValueError, match="No graders available"):
            config_manager.filter_graders_by_availability(config, available_providers)

    def test_get_providers_from_config(self, config_manager, sample_config_dict):
        """Test extracting providers from configuration."""
        config = config_manager._parse_config(sample_config_dict)
        providers = config_manager.get_providers_from_config(config)

        assert "anthropic" in providers
        assert "openai" in providers
        assert len(providers) == 2
