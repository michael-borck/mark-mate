#!/usr/bin/env python3
"""
Test script for enhanced MarkMate grading functionality.
"""

import os
import sys
import json
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_llm_provider():
    """Test the LiteLLM provider interface."""
    print("Testing LLM Provider...")
    
    try:
        from mark_mate.core.llm_provider import LLMProvider
        
        provider = LLMProvider()
        available = provider.get_available_providers()
        print(f"Available providers: {available}")
        
        # Test model configurations
        for provider_name in available:
            models = provider.get_provider_models(provider_name)
            print(f"{provider_name} models: {models}")
        
        print("✓ LLM Provider test passed")
        return True
        
    except Exception as e:
        print(f"✗ LLM Provider test failed: {e}")
        return False


def test_grading_config():
    """Test grading configuration management."""
    print("\nTesting Grading Configuration...")
    
    try:
        from mark_mate.config.grading_config import GradingConfigManager
        
        config_manager = GradingConfigManager()
        
        # Test default config
        config = config_manager.load_config()
        print(f"Default config loaded: {len(config.graders)} graders")
        
        # Test config from file
        config_file = Path(__file__).parent / "grading_config.yaml"
        if config_file.exists():
            config = config_manager.load_config(str(config_file))
            print(f"File config loaded: {len(config.graders)} graders")
        
        print("✓ Grading Configuration test passed")
        return True
        
    except Exception as e:
        print(f"✗ Grading Configuration test failed: {e}")
        return False


def test_enhanced_grader():
    """Test enhanced grading system initialization."""
    print("\nTesting Enhanced Grading System...")
    
    try:
        from mark_mate.core.enhanced_grader import EnhancedGradingSystem
        
        # Test with default config
        grader = EnhancedGradingSystem()
        print(f"Enhanced grader initialized with {len(grader.config.graders)} graders")
        
        # Test with file config
        config_file = Path(__file__).parent / "examples" / "simple_grading_config.yaml"
        if config_file.exists():
            grader = EnhancedGradingSystem(str(config_file))
            print(f"Enhanced grader initialized from file with {len(grader.config.graders)} graders")
        
        print("✓ Enhanced Grading System test passed")
        return True
        
    except Exception as e:
        print(f"✗ Enhanced Grading System test failed: {e}")
        return False


def test_imports():
    """Test package imports."""
    print("\nTesting Package Imports...")
    
    try:
        from mark_mate import (
            GradingSystem, 
            EnhancedGradingSystem, 
            LLMProvider, 
            GradingConfigManager
        )
        
        print("✓ All main classes imported successfully")
        return True
        
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False


def test_cli_help():
    """Test CLI help functionality."""
    print("\nTesting CLI Help...")
    
    try:
        from mark_mate.cli.main import create_parser
        
        parser = create_parser()
        help_text = parser.format_help()
        
        # Check for new features in help
        assert "gemini" in help_text.lower(), "Gemini provider not in help"
        assert "enhanced" in help_text.lower(), "Enhanced mode not in help"
        assert "config" in help_text.lower(), "Config option not in help"
        
        print("✓ CLI Help test passed")
        return True
        
    except Exception as e:
        print(f"✗ CLI Help test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("MarkMate Enhanced Grading Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_llm_provider,
        test_grading_config,
        test_enhanced_grader,
        test_cli_help,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced grading system is ready.")
        return 0
    else:
        print("❌ Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())