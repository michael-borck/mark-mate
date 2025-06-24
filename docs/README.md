# MarkMate Documentation

**Comprehensive guide to MarkMate - Your AI Teaching Assistant for Assignments and Assessment**

## Table of Contents

### 🚀 Getting Started
- **[Installation Guide](getting-started/installation.md)** - Complete setup instructions for all platforms
- **[Quick Start Tutorial](getting-started/quickstart.md)** - Get up and running in 5 minutes
- **[GUI vs CLI Guide](getting-started/gui-vs-cli.md)** - Choose the right interface for you

### 📋 Core Workflow
- **[Workflow Overview](workflow/overview.md)** - Complete process from submissions to grades
- **[Step 1: Consolidate](workflow/consolidate.md)** - Organize and structure submissions
- **[Step 2: Scan](workflow/scan.md)** - Discover GitHub repository URLs
- **[Step 3: Extract](workflow/extract.md)** - Process multi-format content
- **[Step 4: Grade](workflow/grade.md)** - AI-powered assessment and feedback

### ⚙️ Configuration
- **[Grading Configuration](configuration/grading-config.md)** - Complete configuration reference
- **[System Settings](configuration/system-settings.md)** - Environment and performance tuning
- **[Template Management](configuration/templates.md)** - Pre-built configuration templates

### 🤖 AI & Prompts
- **[Prompt System Overview](ai-prompts/overview.md)** - How MarkMate generates AI prompts
- **[Custom Prompt Development](ai-prompts/custom-prompts.md)** - Create specialized prompts
- **[LLM Provider Configuration](ai-prompts/llm-providers.md)** - Setup Claude, GPT, Gemini

### 🏗️ Technical Documentation
- **[Architecture Overview](technical/architecture.md)** - System design and components
- **[GUI Framework Design](technical/gui-design.md)** - Desktop application architecture
- **[CLI Command Reference](technical/cli-reference.md)** - Complete command documentation
- **[API Documentation](technical/api.md)** - Python API reference

### 🎯 Use Cases & Examples
- **[Programming Assignments](examples/programming.md)** - Python, JavaScript, React projects
- **[WordPress Projects](examples/wordpress.md)** - Theme and plugin assessment
- **[International Student Support](examples/international.md)** - Multi-encoding handling
- **[Custom Workflows](examples/custom-workflows.md)** - Advanced usage patterns

### 🔧 Advanced Topics
- **[Extending MarkMate](advanced/extending.md)** - Add custom extractors and analyzers
- **[Custom Extractors](advanced/custom-extractors.md)** - Process new file formats
- **[Integration Guide](advanced/integration.md)** - LMS and platform integration
- **[Troubleshooting](advanced/troubleshooting.md)** - Common issues and solutions

## Quick Reference

### Essential Commands
```bash
# GUI Application
mark-mate-gui

# Basic CLI Workflow
mark-mate consolidate submissions/
mark-mate scan processed_submissions/
mark-mate extract processed_submissions/ --github-urls github_urls.txt
mark-mate grade extracted_content.json assignment.txt

# Configuration Management
mark-mate generate-config --template full
mark-mate grade extracted_content.json assignment.txt --config grading_config.yaml
```

### Key Features
- ✅ **Multi-format Processing**: PDF, DOCX, code files, Jupyter notebooks
- ✅ **GitHub Integration**: Repository analysis and commit history
- ✅ **AI-Powered Grading**: Claude, GPT-4o, Gemini with statistical aggregation
- ✅ **Cross-Platform GUI**: Desktop app for Windows, macOS, Linux
- ✅ **International Support**: 18+ text encodings for global students
- ✅ **WordPress Projects**: Theme, plugin, and site analysis

### Supported Assignment Types
- **Programming**: Python, JavaScript, React, TypeScript, HTML/CSS
- **Web Development**: Full-stack applications, responsive design
- **WordPress**: Theme development, plugin creation, site building
- **Documentation**: Research papers, reports, technical writing
- **Mixed Projects**: Multi-language, multi-format submissions

## Documentation Structure

This documentation is organized into logical sections:

1. **Getting Started**: Installation and initial setup
2. **Core Workflow**: The main MarkMate process
3. **Configuration**: Customizing behavior and AI settings
4. **AI & Prompts**: Understanding and customizing AI assessment
5. **Technical**: Architecture and development details
6. **Examples**: Real-world usage scenarios
7. **Advanced**: Extension and integration topics

## Documentation Conventions

### Code Examples
```bash
# CLI commands are shown with shell syntax
mark-mate command --option value

# Configuration examples use YAML
grading:
  runs_per_grader: 3
```

### File Paths
- **Relative paths**: `docs/workflow/overview.md`
- **Configuration files**: `grading_config.yaml`
- **Example directories**: `processed_submissions/`

### Notation
- **Required parameters**: `FOLDER_PATH`
- **Optional parameters**: `[OPTIONS]`
- **Environment variables**: `$ANTHROPIC_API_KEY`

## Getting Help

### Documentation Issues
- **Missing Information**: Submit issue with "documentation" label
- **Unclear Instructions**: Request clarification via GitHub
- **Examples Needed**: Suggest new examples in discussions

### Community Support
- **GitHub Discussions**: Ask questions and share experiences
- **GitHub Issues**: Report bugs and request features
- **Discord**: Real-time community chat (coming soon)

### Professional Support
- **Commercial Licensing**: Contact for enterprise deployments
- **Custom Development**: Integration and extension services
- **Training**: Institutional training and workshops

## Contributing to Documentation

### How to Contribute
1. **Fork the repository**
2. **Edit documentation files** in `docs/` directory
3. **Submit pull request** with clear description
4. **Review process** by maintainers

### Documentation Standards
- **Clear headings**: Use descriptive section titles
- **Code examples**: Include working examples
- **Cross-references**: Link to related documentation
- **Screenshots**: Add GUI screenshots where helpful

### File Organization
```
docs/
├── index.md                    # Main documentation index
├── getting-started/           # Installation and setup
├── workflow/                  # Core process documentation
├── configuration/             # Settings and customization
├── ai-prompts/               # AI and prompt engineering
├── technical/                # Architecture and development
├── examples/                 # Use cases and tutorials
└── advanced/                 # Extension and integration
```

## Version Information

- **Documentation Version**: 2.0
- **MarkMate Version**: 0.2.0+
- **Last Updated**: 2025-01-23
- **Status**: Actively maintained

## License

This documentation is released under the same MIT License as MarkMate. You are free to use, modify, and distribute these materials with proper attribution.

---

**Welcome to MarkMate!** 🎉

Start with the [Installation Guide](getting-started/installation.md) or jump straight to the [Quick Start Tutorial](getting-started/quickstart.md) to begin automating your assignment grading today.