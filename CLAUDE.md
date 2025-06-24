# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Installation
```bash
# Preferred: Use uv for fast dependency management
make setup

# Alternative: Standard setup with pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev,docs]"
```

### Testing
```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run single test file
python -m pytest tests/test_specific_module.py -v

# Run specific test method
python -m pytest tests/test_module.py::TestClass::test_method -v
```

### Code Quality
```bash
# Run all quality checks
make check-all

# Individual checks
make lint          # ruff linting
make format        # ruff formatting
make typecheck     # basedpyright type checking
make format-check  # check formatting without fixing
```

### Documentation
```bash
# Build docs locally
make docs

# Serve docs with live reload
make docs-serve

# Deploy to GitHub Pages
make docs-deploy
```

### Package Management
```bash
# Build package
make build

# Clean build artifacts
make clean

# Clean everything including venv
make clean-all
```

## High-Level Architecture

### Core System Design

MarkMate follows a **pipeline architecture** with four main phases:

1. **Consolidate** (`cli/consolidate.py`) → Organizes raw submissions
2. **Scan** (`cli/scan.py`) → Discovers GitHub URLs  
3. **Extract** (`cli/extract.py`) → Processes content with multiple extractors
4. **Grade** (`cli/grade.py`) → AI-powered assessment with statistical aggregation

### Key Architectural Components

#### 1. Extractor System (`extractors/`)
**Plugin architecture** with specialized processors:
- `BaseExtractor` - Abstract interface for all extractors
- `CodeExtractor` - Python/JavaScript static analysis
- `WebExtractor` - HTML/CSS/JS validation and analysis  
- `OfficeExtractor` - PDF/DOCX/PowerPoint processing
- `ReactExtractor` - React/TypeScript component analysis
- `GitHubExtractor` - Repository analysis and commit history

**Pattern**: Each extractor implements `can_extract()` and `extract()` methods, with automatic file type detection routing content to appropriate processors.

#### 2. Enhanced Grading System (`core/enhanced_grader.py`)
**Multi-LLM statistical aggregation** with:
- **LiteLLM Integration**: Unified interface for Claude/GPT/Gemini
- **Statistical Methods**: mean, median, weighted_mean, trimmed_mean
- **Confidence Scoring**: Based on inter-grader agreement variance
- **Cost Controls**: Per-student budget limits and usage tracking
- **Auto-Configuration**: Optimal setup based on available API keys

#### 3. Configuration Management (`config/`)
**YAML-driven configuration** with:
- `grading_config.py` - Multi-provider grading configurations
- `defaults.py` - Auto-configuration based on available API keys
- `settings.py` - Application-wide settings management

#### 4. GUI System (`gui/`)
**Cross-platform desktop application** using Flet framework:
- `main.py` - Main application with navigation routing
- `pages/` - Individual workflow pages (consolidate, scan, extract, grade, config)
- `adapters/cli_adapter.py` - Bridge between GUI and CLI functionality
- `utils/async_runner.py` - Async operation management for GUI

### Data Flow Architecture

```
Raw Submissions → Consolidate → Scan (GitHub URLs) → Extract (Multi-format) → Grade (Multi-LLM)
                     ↓              ↓                    ↓                     ↓
               Organized Files → URL Mappings → Extracted Content JSON → Grading Results JSON
```

**Key Data Structures**:
- Extraction results use `ExtractionResult` model (`extractors/models.py`)
- Grading configuration uses Pydantic models (`config/grading_config.py`)
- CLI adapters provide unified interface between GUI and CLI operations

### Optional Dependency Architecture

**Critical Design Pattern**: MarkMate handles optional dependencies gracefully:
- Web libraries (BeautifulSoup, cssutils, html5lib) - for web extraction
- Office libraries (python-pptx, openpyxl, pandas) - for document processing  
- LiteLLM - for AI provider integration

**Implementation**: All extractors check for optional dependencies and provide fallback behavior when libraries are unavailable.

### Type Safety Architecture

The codebase maintains strong typing with documented workarounds:
- **235 total type workarounds** documented in `TYPE_SAFETY_DOCUMENTATION.md`
- **Modern typing**: Uses `dict[str, Any]` over `Dict[str, Any]`
- **Protocols**: Used for optional dependency interfaces
- **Type Guards**: BasedPyright for comprehensive type checking

## Important Development Patterns

### 1. Extractor Development
When creating new extractors:
```python
class MyExtractor(BaseExtractor):
    def can_extract(self, file_path: str) -> bool:
        return file_path.endswith('.myformat')
    
    def extract(self, file_path: str) -> ExtractionResult:
        # Implementation with proper error handling
        pass
```

### 2. Optional Dependency Handling
Follow the established pattern:
```python
try:
    from some_library import SomeClass
except ImportError:
    SomeClass = None  # type: ignore[misc,assignment]

# Later in code:
if SomeClass is None:
    return fallback_behavior()
```

### 3. GUI-CLI Bridge Pattern
GUI operations use CLI adapters:
```python
from ..adapters.cli_adapter import CLIAdapter

# In GUI page
result = await CLIAdapter.run_extract_async(
    submissions_folder=folder_path,
    output_file=output_file,
    progress_callback=self.update_progress
)
```

### 4. Configuration Auto-Detection
The system automatically configures based on available API keys:
```python
# Auto-configuration happens in GradingConfigManager
config_manager = GradingConfigManager()
config = config_manager.load_config()  # None = auto-configure
```

## API Keys and Environment

**Required for grading operations** - at least one of:
```bash
export ANTHROPIC_API_KEY="your_key"    # Claude 3.5 Sonnet
export OPENAI_API_KEY="your_key"       # GPT-4o/GPT-4o-mini  
export GEMINI_API_KEY="your_key"       # Google Gemini Pro
```

**Testing**: Use `.env` files in development - automatically loaded by MarkMate.

## Critical Considerations

### Type Safety Maintenance
- **Always document new type workarounds** in `TYPE_SAFETY_DOCUMENTATION.md`
- **Use BasedPyright** (not mypy) for type checking: `make typecheck`
- **Review high-risk type ignores** before production changes

### Performance Considerations
- **Parallel processing** is used extensively in extractors and grading
- **Memory management** for large submissions handled via streaming
- **Rate limiting** respects API provider limits automatically

### GUI Development
- **Flet framework** for cross-platform desktop applications
- **Async operations** required for file processing and API calls
- **Progress tracking** essential for user experience during long operations

### Testing Strategy
- **Integration tests** cover full workflows (consolidate → scan → extract → grade)
- **Unit tests** for individual extractors and analyzers
- **Mock API responses** for grading system tests
- **File encoding tests** for international student support

This architecture enables MarkMate to handle diverse student submissions while maintaining type safety, performance, and extensibility through its plugin-based extractor system and unified LLM interface.