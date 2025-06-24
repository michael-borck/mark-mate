# MarkMate Quick Start Guide

Get up and running with MarkMate in minutes using either the GUI desktop application or CLI interface.

## Installation

### Option 1: GUI Desktop Application (Recommended)

```bash
# Install MarkMate with GUI support
pip install mark-mate

# Launch the desktop application
mark-mate-gui
```

### Option 2: CLI Only
```bash
# Install MarkMate for command-line use
pip install mark-mate

# Verify installation
mark-mate --help
```

## Quick Setup

### 1. Configure API Keys
MarkMate uses AI providers for grading. Set up at least one:

```bash
# Anthropic Claude (Recommended)
export ANTHROPIC_API_KEY="your_anthropic_key"

# OpenAI GPT
export OPENAI_API_KEY="your_openai_key"

# Google Gemini  
export GEMINI_API_KEY="your_gemini_key"
```

### 2. Prepare Test Data
Download sample submissions or use your own:
```bash
# Create a test directory
mkdir sample_submissions
cd sample_submissions

# Add some sample files
echo "print('Hello, World!')" > student_123_assignment.py
echo "# My Project\nThis is my assignment." > student_456_readme.md
```

## GUI Quick Start (5 Minutes)

### Step 1: Launch MarkMate GUI
```bash
mark-mate-gui
```

### Step 2: Consolidate Submissions
1. **Navigate to "Consolidate" page**
2. **Click "Browse"** and select your `sample_submissions` folder
3. **Click "Start Consolidation"**
4. **Wait for completion** - you'll see progress updates

### Step 3: Extract Content  
1. **Navigate to "Extract" page**
2. **Browse** and select the `processed_submissions` folder
3. **Click "Start Extraction"**
4. **Review results** - content is now ready for grading

### Step 4: Grade Submissions
1. **Navigate to "Grade" page**
2. **Select extracted content JSON** (auto-populated)
3. **Browse and select assignment specification** (create a simple .txt file with requirements)
4. **Click "Start AI Grading"**
5. **Review results** - grades and feedback are generated!

## CLI Quick Start (3 Minutes)

### Complete Workflow Example
```bash
# Step 1: Consolidate submissions
mark-mate consolidate sample_submissions/

# Step 2: Extract content
mark-mate extract processed_submissions/

# Step 3: Create assignment specification
echo "Grade this Python assignment. Look for correct syntax and functionality." > assignment.txt

# Step 4: Grade submissions
mark-mate grade extracted_content.json assignment.txt

# View results
cat grading_results.json
```

## First Grading Results

### Understanding Output
Your grading results will look like this:

```json
{
  "grading_session": {
    "timestamp": "2025-01-23T14:30:00",
    "total_students": 2,
    "providers": ["anthropic"]
  },
  "results": {
    "123": {
      "aggregate": {
        "mark": 85,
        "feedback": "Good basic Python implementation. The code runs correctly and produces the expected output. Consider adding comments for better documentation.",
        "confidence": 0.92
      }
    },
    "456": {
      "aggregate": {
        "mark": 75,
        "feedback": "Adequate documentation in README. The project description is clear but could benefit from more technical details and examples.",
        "confidence": 0.88
      }
    }
  }
}
```

## Common First-Run Issues

### Issue: "No API key found"
**Solution**: Set your API key environment variable
```bash
export ANTHROPIC_API_KEY="your_key_here"
# Restart your terminal or GUI application
```

### Issue: "No students found after consolidation"
**Solution**: Ensure filenames include student IDs
```bash
# Good filenames:
student_123_assignment.py
john_doe_456_project.zip
submission_789.pdf

# Bad filenames (no clear student ID):
assignment.py
final_project.zip
```

### Issue: "GUI won't start"
**Solution**: Check Flet installation
```bash
pip install --upgrade flet
mark-mate-gui
```

### Issue: "Empty extraction results"
**Solution**: Verify file formats are supported
- ✅ Supported: .py, .js, .html, .css, .pdf, .docx, .txt, .md
- ❌ Unsupported: .exe, .bin, .img, proprietary formats

## Next Steps

### 1. Try Advanced Features
- **GitHub Integration**: Add repository URLs for commit analysis
- **WordPress Projects**: Use `--wordpress` mode for theme/plugin assignments
- **Custom Configuration**: Generate grading configurations for better control

### 2. Explore Real Assignments
```bash
# Programming assignment with GitHub
mark-mate consolidate programming_submissions/
mark-mate scan processed_submissions/  # Find GitHub URLs
mark-mate extract processed_submissions/ --github-urls github_urls.txt
mark-mate grade extracted_content.json programming_assignment.txt

# WordPress assignment
mark-mate consolidate wordpress_submissions/ --wordpress
mark-mate extract processed_submissions/ --wordpress
mark-mate grade extracted_content.json wordpress_requirements.txt
```

### 3. Configure Multiple AI Providers
```bash
# Generate a configuration file
mark-mate generate-config --template full

# Use custom configuration
mark-mate grade extracted_content.json assignment.txt --config grading_config.yaml
```

## Sample Assignment Specifications

### Programming Assignment
```text
Python Programming Assignment - Grade out of 100

Requirements:
1. Code Functionality (40%):
   - Program runs without errors
   - Produces correct output
   - Handles edge cases appropriately

2. Code Quality (30%):
   - Clean, readable code
   - Proper variable naming
   - Appropriate comments

3. Algorithm Efficiency (20%):
   - Efficient problem-solving approach
   - Appropriate data structures
   - Optimization considerations

4. Documentation (10%):
   - Clear README file
   - Function documentation
   - Usage examples

Provide specific feedback for each criterion and suggest improvements.
```

### Web Development Assignment
```text
Web Development Project - Grade out of 100

Assessment Criteria:
1. Technical Implementation (35%):
   - Valid HTML/CSS
   - Functional JavaScript
   - Responsive design

2. User Experience (25%):
   - Intuitive navigation
   - Visual appeal
   - Accessibility features

3. Code Organization (25%):
   - Clean file structure
   - Consistent naming
   - Proper commenting

4. Innovation (15%):
   - Creative features
   - Problem-solving approach
   - Technical complexity

Focus on both functionality and presentation quality.
```

## Best Practices for New Users

### 1. Start Small
- Test with 2-3 submissions first
- Use simple assignment specifications
- Review results carefully before scaling up

### 2. Organize Submissions
- Use consistent naming: `studentID_assignment.ext`
- Group related files in folders
- Remove unnecessary system files

### 3. Create Clear Assignment Specs
- Define grading criteria explicitly
- Specify point distributions
- Include example expectations

### 4. Review AI Results
- Check scores for reasonableness
- Validate feedback quality
- Adjust configurations as needed

### 5. Iterate and Improve
- Refine assignment specifications
- Adjust grading configurations
- Incorporate feedback from actual use

## Getting Help

### Documentation
- **Full Documentation**: [docs/index.md](../index.md)
- **Workflow Guide**: [docs/workflow/overview.md](../workflow/overview.md)
- **Configuration**: [docs/configuration/grading-config.md](../configuration/grading-config.md)

### Community Support
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Share experiences and get help
- **Examples**: Check the `examples/` directory

### Troubleshooting
- **Common Issues**: [docs/advanced/troubleshooting.md](../advanced/troubleshooting.md)
- **CLI Reference**: [docs/technical/cli-reference.md](../technical/cli-reference.md)
- **API Documentation**: [docs/technical/api.md](../technical/api.md)

---

**Congratulations!** You've completed your first MarkMate grading workflow. You're now ready to process real assignments and explore advanced features.

**Next Recommended Reading**:
- [Complete Workflow Guide](../workflow/overview.md)
- [Configuration Management](../configuration/grading-config.md)
- [Programming Assignment Examples](../examples/programming.md)