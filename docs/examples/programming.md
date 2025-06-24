# Programming Assignment Examples

This guide demonstrates how to use MarkMate for various types of programming assignments, from simple Python scripts to complex multi-language projects.

## Basic Python Assignment

### Assignment Scenario
Students submit Python programs that solve algorithmic problems.

### Sample Assignment Specification
```text
Python Algorithm Assignment - Grade out of 100

Assignment: Implement a sorting algorithm and data analysis functions.

Requirements:
1. Sorting Implementation (40%):
   - Implement at least one sorting algorithm (bubble, merge, or quick sort)
   - Function should handle edge cases (empty lists, single elements)
   - Include proper error handling

2. Data Analysis (30%):
   - Calculate mean, median, and mode of a dataset
   - Handle missing or invalid data appropriately
   - Return results in a structured format

3. Code Quality (20%):
   - Clean, readable code with meaningful variable names
   - Proper function documentation with docstrings
   - Consistent code style (PEP 8 compliance)

4. Testing and Examples (10%):
   - Include test cases demonstrating functionality
   - Provide usage examples in comments or separate file
   - Handle edge cases in testing

Submission Format:
- Submit as .py file or .zip containing Python files
- Include README.md with usage instructions
- Optional: Include requirements.txt if using external libraries

Grading Focus:
- Correctness of algorithm implementation
- Code organization and readability
- Error handling and edge case management
- Documentation quality
```

### Sample Student Submission Structure
```
student_123_assignment/
├── sorting.py
├── data_analysis.py
├── test_cases.py
├── README.md
└── requirements.txt
```

### MarkMate Workflow
```bash
# 1. Consolidate submissions
mark-mate consolidate python_submissions/

# 2. Extract content (no GitHub URLs needed for simple assignments)
mark-mate extract processed_submissions/

# 3. Create assignment specification file
cat > assignment_spec.txt << 'EOF'
[Assignment specification text from above]
EOF

# 4. Grade submissions
mark-mate grade extracted_content.json assignment_spec.txt --output python_grades.json

# 5. Review results
head -20 python_grades.json
```

### Expected Output Analysis
MarkMate will analyze:
- **Code Structure**: Function definitions, class organization
- **Algorithm Implementation**: Correctness and efficiency
- **Documentation**: Docstrings, comments, README content
- **Error Handling**: Try-catch blocks, input validation
- **Code Style**: PEP 8 compliance, naming conventions

## Web Development Assignment

### Assignment Scenario
Students create responsive websites with HTML, CSS, and JavaScript.

### Sample Assignment Specification
```text
Responsive Web Portfolio - Grade out of 100

Assignment: Create a personal portfolio website showcasing web development skills.

Technical Requirements (50%):
1. HTML Structure (15%):
   - Semantic HTML5 elements
   - Valid markup (passes W3C validation)
   - Proper heading hierarchy
   - Accessible form elements

2. CSS Styling (20%):
   - Responsive design (mobile-first approach)
   - CSS Grid or Flexbox layout
   - Custom CSS animations/transitions
   - Cross-browser compatibility

3. JavaScript Functionality (15%):
   - Interactive elements (navigation, forms, galleries)
   - DOM manipulation
   - Event handling
   - No framework required, vanilla JS preferred

Content & Design (30%):
1. Visual Design (15%):
   - Professional appearance
   - Consistent color scheme and typography
   - Appropriate use of whitespace
   - High-quality images and media

2. Content Quality (15%):
   - Clear navigation structure
   - Engaging and relevant content
   - Contact information and social links
   - Portfolio showcasing previous work

User Experience (20%):
1. Usability (10%):
   - Intuitive navigation
   - Fast loading times
   - Error-free functionality
   - Mobile-friendly interface

2. Accessibility (10%):
   - Alt text for images
   - Proper contrast ratios
   - Keyboard navigation support
   - Screen reader compatibility

Submission Requirements:
- Submit as ZIP file containing all website files
- Include index.html as the main page
- Organize files in logical folder structure (css/, js/, images/)
- Include README.md with setup instructions and feature descriptions
```

### MarkMate Workflow with GitHub Integration
```bash
# 1. Consolidate submissions
mark-mate consolidate web_submissions/

# 2. Scan for GitHub URLs (many students host on GitHub Pages)
mark-mate scan processed_submissions/ --output github_urls.txt

# 3. Review and edit GitHub URLs
nano github_urls.txt

# 4. Extract content with GitHub integration
mark-mate extract processed_submissions/ --github-urls github_urls.txt

# 5. Grade with web-specific configuration
mark-mate grade extracted_content.json web_assignment_spec.txt --output web_grades.json
```

### Analysis Capabilities
MarkMate provides comprehensive web development analysis:

- **HTML Validation**: Structure, semantics, accessibility
- **CSS Analysis**: Properties used, responsive design patterns
- **JavaScript Evaluation**: Functionality, event handling, DOM manipulation
- **Web Standards**: Validation against W3C standards
- **Performance Metrics**: File sizes, loading optimization
- **GitHub Analysis**: Commit history, development progression

## React/JavaScript Project

### Assignment Scenario
Advanced students build React applications with modern JavaScript.

### Sample Assignment Specification
```text
React Task Management App - Grade out of 100

Assignment: Build a task management application using React with modern JavaScript features.

Core Functionality (40%):
1. Task Management (20%):
   - Add, edit, delete tasks
   - Mark tasks as complete/incomplete
   - Task categories or tags
   - Persistent storage (localStorage or API)

2. User Interface (20%):
   - Clean, intuitive design
   - Responsive layout
   - Real-time updates
   - Loading states and error handling

React Implementation (30%):
1. Component Architecture (15%):
   - Functional components with hooks
   - Proper component composition
   - Reusable components
   - Clear prop interfaces

2. State Management (15%):
   - Appropriate use of useState, useEffect
   - State lifting and prop drilling awareness
   - Optional: Context API or external state management

Code Quality (20%):
1. JavaScript Best Practices (10%):
   - ES6+ features (arrow functions, destructuring, modules)
   - Proper error handling
   - Code organization and modularity
   - Performance considerations

2. Development Setup (10%):
   - Proper package.json configuration
   - Build process setup
   - Code formatting and linting
   - Git commit history quality

Documentation & Testing (10%):
1. Documentation (5%):
   - Clear README with setup instructions
   - Component documentation
   - API documentation if applicable

2. Testing (5%):
   - Unit tests for key functionality
   - Integration tests for user flows
   - Test coverage considerations

Bonus Features (up to 10% extra credit):
- Advanced React patterns (custom hooks, render props)
- TypeScript implementation
- API integration
- Deployment to live URL
```

### Advanced MarkMate Configuration
```yaml
# react_grading_config.yaml
grading:
  runs_per_grader: 3
  averaging_method: "weighted_mean"

graders:
  - name: "claude-react"
    provider: "anthropic"
    model: "claude-3-5-sonnet"
    weight: 2.0
    primary_feedback: true
    specialization: "react"
    
  - name: "gpt4o-js"
    provider: "openai"
    model: "gpt-4o"
    weight: 1.5
    specialization: "javascript"

execution:
  max_cost_per_student: 1.00
  parallel_execution: true

prompts:
  system_prompt: |
    You are an expert React and JavaScript instructor with extensive experience 
    in modern web development. Evaluate React applications considering:
    - Component architecture and React best practices
    - Modern JavaScript usage and ES6+ features
    - Code organization and maintainability
    - User experience and interface design
    - Development workflow and tooling
  
  feedback_style: "comprehensive"
  include_code_suggestions: true
```

### MarkMate Workflow
```bash
# 1. Consolidate React projects
mark-mate consolidate react_submissions/

# 2. Scan for GitHub repositories (critical for React projects)
mark-mate scan processed_submissions/ --output react_github_urls.txt

# 3. Extract with React-specific analysis
mark-mate extract processed_submissions/ --github-urls react_github_urls.txt

# 4. Grade with custom React configuration
mark-mate grade extracted_content.json react_assignment_spec.txt \
  --config react_grading_config.yaml \
  --output react_grades.json
```

### React-Specific Analysis
MarkMate's React extractor provides:

- **Component Analysis**: Functional vs class components, hooks usage
- **Package.json Evaluation**: Dependencies, scripts, project setup
- **TypeScript Support**: Type definitions, interface usage
- **Build Configuration**: Webpack, Vite, or Create React App setup
- **Testing Framework**: Jest, Testing Library integration
- **Code Quality**: ESLint rules, Prettier configuration

## Multi-Language Project

### Assignment Scenario
Full-stack application with multiple programming languages.

### Sample Project Structure
```
student_456_fullstack/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.js
│   ├── package.json
│   └── README.md
├── backend/
│   ├── app.py
│   ├── models/
│   ├── routes/
│   └── requirements.txt
├── database/
│   ├── schema.sql
│   └── migrations/
├── docker-compose.yml
└── README.md
```

### Comprehensive Grading Configuration
```yaml
# fullstack_grading_config.yaml
grading:
  runs_per_grader: 2
  averaging_method: "weighted_mean"

graders:
  - name: "fullstack-expert"
    provider: "anthropic"
    model: "claude-3-5-sonnet"
    weight: 2.5
    specializations: ["fullstack", "architecture"]
    
  - name: "backend-specialist"
    provider: "openai"
    model: "gpt-4o"
    weight: 1.5
    specializations: ["python", "api-design"]
    
  - name: "frontend-specialist"
    provider: "gemini"
    model: "gemini-1.5-pro"
    weight: 1.5
    specializations: ["javascript", "react", "ui-ux"]

execution:
  max_cost_per_student: 1.50
  parallel_execution: true

assessment_weights:
  backend_implementation: 0.35
  frontend_implementation: 0.35
  database_design: 0.15
  integration_quality: 0.10
  documentation: 0.05

prompts:
  system_prompt: |
    You are evaluating a full-stack web application. Consider:
    
    Backend (35%):
    - API design and implementation
    - Database integration
    - Error handling and validation
    - Security considerations
    
    Frontend (35%):
    - User interface design
    - State management
    - API integration
    - Responsive design
    
    Architecture (15%):
    - Code organization
    - Separation of concerns
    - Scalability considerations
    
    Integration (10%):
    - Frontend-backend communication
    - Data flow consistency
    - End-to-end functionality
    
    Documentation (5%):
    - Setup instructions
    - API documentation
    - Code comments
```

## Assignment Type Detection

MarkMate automatically detects assignment types based on content:

```python
# Assignment type detection logic
def detect_assignment_type(content):
    if has_react_components(content):
        return "react"
    elif has_web_files(content):
        return "web_development"
    elif has_python_files(content):
        return "python_programming"
    elif has_multiple_languages(content):
        return "fullstack"
    else:
        return "general_programming"
```

## Best Practices for Programming Assignments

### 1. Clear Specifications
- Define specific technical requirements
- Include code quality expectations
- Specify submission format clearly
- Provide grading rubric

### 2. Consistent Naming
```bash
# Good submission naming
student_123_algorithm_assignment.py
team_456_web_project.zip
individual_789_react_app.zip

# Include student IDs for automatic processing
```

### 3. GitHub Integration
- Encourage students to use version control
- Provide GitHub repository submission option
- Value commit history and development process

### 4. Multiple Assessment Runs
```yaml
# Use multiple runs for programming assignments
grading:
  runs_per_grader: 3  # Higher for code evaluation
  averaging_method: "trimmed_mean"  # Remove outliers
```

### 5. Specialized Configurations
- Create assignment-type specific configurations
- Weight different aspects appropriately
- Use provider specializations

## Common Programming Assignment Patterns

### Pattern 1: Algorithm Implementation
- Focus on correctness and efficiency
- Emphasize code clarity and documentation
- Test edge cases and error handling

### Pattern 2: Project-Based Learning
- Evaluate overall architecture
- Consider user experience
- Assess development process through GitHub

### Pattern 3: Framework-Specific Assignments
- Use specialized prompt templates
- Configure appropriate analysis tools
- Weight framework-specific best practices

### Pattern 4: Collaborative Projects
- Analyze individual contributions via Git
- Evaluate team coordination
- Assess code integration quality

---

**Related Documentation**:
- [Web Development Examples](web-development.md)
- [GitHub Integration Guide](../workflow/scan.md)
- [Custom Configuration](../configuration/grading-config.md)