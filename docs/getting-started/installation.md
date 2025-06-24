# Installation Guide

This guide covers installation of MarkMate across different platforms and environments.

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Memory**: 4 GB RAM
- **Storage**: 500 MB free space
- **Network**: Internet connection for AI provider APIs

### Recommended Requirements
- **Python**: 3.10 or higher
- **Memory**: 8 GB RAM
- **Storage**: 2 GB free space (for large submission processing)
- **SSD**: For faster file processing

## Installation Methods

### Method 1: PyPI Installation (Recommended)

```bash
# Standard installation
pip install mark-mate

# Install with all optional dependencies
pip install mark-mate[all]

# Install specific components
pip install mark-mate[gui]     # GUI support only
pip install mark-mate[dev]     # Development dependencies
```

### Method 2: Development Installation

```bash
# Clone the repository
git clone https://github.com/michael-borck/mark-mate.git
cd mark-mate

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### Method 3: Pipx Installation (Isolated)

```bash
# Install pipx if not already installed
python -m pip install --user pipx
python -m pipx ensurepath

# Install MarkMate in isolated environment
pipx install mark-mate

# Install with GUI support
pipx install mark-mate[gui]
```

## Platform-Specific Instructions

### Windows

#### Using pip (Standard)
```powershell
# Open PowerShell or Command Prompt
pip install mark-mate

# Launch GUI
mark-mate-gui
```

#### Using Windows Subsystem for Linux (WSL)
```bash
# In WSL terminal
pip install mark-mate

# For GUI support, install X11 server on Windows
# Then run: mark-mate-gui
```

#### Common Windows Issues
**Issue**: `pip` not found
```powershell
# Install Python from python.org
# Or use Microsoft Store Python
# Ensure "Add Python to PATH" is checked
```

**Issue**: Permission errors
```powershell
# Use user installation
pip install --user mark-mate
```

### macOS

#### Using pip
```bash
# Install Python via Homebrew (recommended)
brew install python

# Install MarkMate
pip3 install mark-mate

# Launch GUI
mark-mate-gui
```

#### Using Homebrew (Future)
```bash
# Coming soon
brew install mark-mate
```

#### Common macOS Issues
**Issue**: SSL certificate errors
```bash
# Update certificates
/Applications/Python\ 3.x/Install\ Certificates.command
```

**Issue**: GUI won't start
```bash
# Install tkinter if missing
brew install python-tk
```

### Linux

#### Ubuntu/Debian
```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Install MarkMate
pip3 install mark-mate

# For GUI support, install additional packages
sudo apt install python3-tk

# Launch GUI
mark-mate-gui
```

#### CentOS/RHEL/Fedora
```bash
# Install dependencies
sudo dnf install python3 python3-pip

# Install MarkMate
pip3 install mark-mate
```

#### Arch Linux
```bash
# Install dependencies
sudo pacman -S python python-pip

# Install MarkMate
pip install mark-mate
```

## Virtual Environment Setup

### Why Use Virtual Environments?
- Isolate MarkMate dependencies
- Avoid conflicts with other Python packages
- Easy to remove or upgrade

### Standard Virtual Environment
```bash
# Create virtual environment
python -m venv markmate_env

# Activate (Linux/macOS)
source markmate_env/bin/activate

# Activate (Windows)
markmate_env\Scripts\activate

# Install MarkMate
pip install mark-mate

# Deactivate when done
deactivate
```

### Conda Environment
```bash
# Create conda environment
conda create -n markmate python=3.10
conda activate markmate

# Install MarkMate
pip install mark-mate

# Deactivate when done
conda deactivate
```

## API Key Configuration

### Required API Keys
You need at least one API key from these providers:

#### Anthropic Claude
```bash
# Get key from: https://console.anthropic.com/
export ANTHROPIC_API_KEY="your_anthropic_key"
```

#### OpenAI GPT
```bash
# Get key from: https://platform.openai.com/api-keys
export OPENAI_API_KEY="your_openai_key"
```

#### Google Gemini
```bash
# Get key from: https://makersuite.google.com/app/apikey
export GEMINI_API_KEY="your_gemini_key"
# Alternative variable name
export GOOGLE_API_KEY="your_gemini_key"
```

### Persistent API Key Setup

#### Linux/macOS
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export ANTHROPIC_API_KEY="your_key"' >> ~/.bashrc
source ~/.bashrc
```

#### Windows
```powershell
# Set system environment variable
setx ANTHROPIC_API_KEY "your_key"

# Or use Windows Settings:
# Settings > System > About > Advanced system settings
# > Environment Variables > New...
```

#### Python dotenv (All platforms)
```bash
# Create .env file in your project directory
echo "ANTHROPIC_API_KEY=your_key" > .env
echo "OPENAI_API_KEY=your_key" >> .env

# MarkMate will automatically load .env files
```

## Verification

### Test CLI Installation
```bash
# Check version
mark-mate --version

# Test basic command
mark-mate --help

# Test with sample data
mkdir test_submissions
echo "print('test')" > test_submissions/student_123_test.py
mark-mate consolidate test_submissions/
```

### Test GUI Installation
```bash
# Launch GUI
mark-mate-gui

# Should open desktop application window
# Test by navigating between pages
```

### Test API Integration
```bash
# Generate test configuration
mark-mate generate-config --template minimal

# Check API key detection
# Should show available providers based on your keys
```

## Upgrading MarkMate

### Standard Upgrade
```bash
# Upgrade to latest version
pip install --upgrade mark-mate

# Check new version
mark-mate --version
```

### Development Version
```bash
# Install latest development version
pip install --upgrade git+https://github.com/michael-borck/mark-mate.git
```

### Version-Specific Installation
```bash
# Install specific version
pip install mark-mate==0.2.0

# Downgrade if needed
pip install mark-mate==0.1.2
```

## Troubleshooting Installation

### Common Issues

#### Issue: ImportError for required packages
```bash
# Solution: Install missing dependencies
pip install --upgrade pip setuptools wheel
pip install mark-mate --force-reinstall
```

#### Issue: GUI dependencies missing
```bash
# Solution: Install GUI extras
pip install mark-mate[gui]

# Or install Flet separately
pip install flet>=0.21.0
```

#### Issue: Permission denied
```bash
# Solution: Use user installation
pip install --user mark-mate

# Or use virtual environment
python -m venv markmate_env
source markmate_env/bin/activate
pip install mark-mate
```

#### Issue: SSL/Network errors
```bash
# Solution: Upgrade pip and certificates
pip install --upgrade pip
pip install --trusted-host pypi.org --trusted-host pypi.python.org mark-mate
```

#### Issue: Python version too old
```bash
# Check Python version
python --version

# Install newer Python:
# - Windows: Download from python.org
# - macOS: brew install python@3.10
# - Linux: sudo apt install python3.10
```

### Platform-Specific Issues

#### Windows: Long path issues
```powershell
# Enable long paths in Windows
# Run as Administrator:
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

#### macOS: Command not found
```bash
# Add Python bin to PATH
echo 'export PATH="$HOME/Library/Python/3.x/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### Linux: GUI display issues
```bash
# Install display libraries
sudo apt install libgl1-mesa-glx libegl1-mesa libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6

# For WSL, install X11 server on Windows
```

## Docker Installation (Advanced)

### Dockerfile
```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install MarkMate
RUN pip install mark-mate

# Set working directory
WORKDIR /workspace

# Default command
CMD ["mark-mate", "--help"]
```

### Docker Usage
```bash
# Build image
docker build -t markmate .

# Run CLI
docker run -v $(pwd):/workspace markmate mark-mate consolidate submissions/

# With API keys
docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY -v $(pwd):/workspace markmate
```

## Next Steps

After successful installation:

1. **[Quick Start Guide](quickstart.md)**: Get up and running in 5 minutes
2. **[API Key Setup](api-keys.md)**: Configure AI provider access
3. **[GUI Tutorial](gui-tutorial.md)**: Learn the desktop interface
4. **[CLI Reference](../technical/cli-reference.md)**: Master command-line usage

## Getting Help

### Documentation
- **Installation Issues**: Check this guide's troubleshooting section
- **Usage Questions**: See [Quick Start Guide](quickstart.md)
- **Advanced Setup**: Read [Configuration Guide](../configuration/grading-config.md)

### Support Channels
- **GitHub Issues**: Report installation problems
- **Discussions**: Ask installation questions
- **Discord**: Real-time community help (coming soon)

---

**Installation Complete!** 🎉

You're ready to start using MarkMate. Continue with the [Quick Start Guide](quickstart.md) to process your first assignments.