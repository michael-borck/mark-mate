# Grading Configuration Guide

MarkMate's grading system supports extensive configuration through YAML files, enabling precise control over AI assessment behavior, provider selection, and statistical aggregation.

## Configuration Overview

### Auto-Configuration vs Custom Configuration

**Auto-Configuration (Recommended for beginners)**:
- Automatically detects available API keys
- Creates optimal configuration based on available providers
- Uses sensible defaults for runs, weights, and cost limits

**Custom Configuration (Advanced users)**:
- Full control over all grading parameters
- Multi-provider setups with custom weights
- Advanced statistical aggregation methods
- Fine-tuned cost and performance optimization

## Configuration File Structure

### Complete Configuration Example
```yaml
# MarkMate Grading Configuration
# Version: 2.0

grading:
  runs_per_grader: 3
  averaging_method: "weighted_mean"  # Options: mean, median, weighted_mean, trimmed_mean
  parallel_execution: true
  confidence_threshold: 0.8
  
graders:
  - name: "claude-sonnet"
    provider: "anthropic"
    model: "claude-3-5-sonnet"
    weight: 2.0
    primary_feedback: true
    
  - name: "gpt4o"
    provider: "openai"
    model: "gpt-4o"
    weight: 1.5
    temperature: 0.3
    
  - name: "gemini-pro"
    provider: "gemini"
    model: "gemini-1.5-pro"
    weight: 1.0
    temperature: 0.4

execution:
  max_cost_per_student: 0.75
  retry_attempts: 3
  rate_limit_delay: 1.0
  timeout_seconds: 120
  
statistics:
  trim_percentage: 10.0  # For trimmed_mean
  outlier_detection: true
  variance_analysis: true
  
prompts:
  system_prompt: "You are an expert academic grader..."
  rubric_integration: "automatic"  # Options: automatic, manual, none
  feedback_style: "comprehensive"  # Options: brief, moderate, comprehensive
```

## Grader Configuration

### Provider-Specific Settings

#### Anthropic (Claude)
```yaml
- name: "claude-sonnet"
  provider: "anthropic"
  model: "claude-3-5-sonnet"  # or claude-3-sonnet, claude-3-haiku
  weight: 2.0
  max_tokens: 4000
  temperature: 0.2
  primary_feedback: true
```

#### OpenAI (GPT)
```yaml
- name: "gpt4o"
  provider: "openai" 
  model: "gpt-4o"  # or gpt-4o-mini, gpt-4, gpt-3.5-turbo
  weight: 1.5
  max_tokens: 3000
  temperature: 0.3
  top_p: 0.9
```

#### Google (Gemini)
```yaml
- name: "gemini-pro"
  provider: "gemini"
  model: "gemini-1.5-pro"  # or gemini-pro, gemini-2.0-flash
  weight: 1.0
  temperature: 0.4
  candidate_count: 1
```

### Weight Configuration

**Weight Interpretation**:
- **2.0**: High importance (primary grader)
- **1.5**: Moderate-high importance
- **1.0**: Standard importance
- **0.5**: Lower importance (experimental)

**Weight Strategy Examples**:
```yaml
# Conservative approach (trust Claude most)
graders:
  - name: "claude"
    weight: 3.0
  - name: "gpt4o"
    weight: 1.0
  - name: "gemini"
    weight: 1.0

# Balanced approach
graders:
  - name: "claude"
    weight: 1.5
  - name: "gpt4o"
    weight: 1.5
  - name: "gemini"
    weight: 1.0

# Experimental approach (equal weights)
graders:
  - name: "claude"
    weight: 1.0
  - name: "gpt4o"
    weight: 1.0
  - name: "gemini"
    weight: 1.0
```

## Statistical Aggregation Methods

### 1. Mean (Simple Average)
```yaml
grading:
  averaging_method: "mean"
```
**Use Case**: Equal trust in all graders
**Formula**: `(grade1 + grade2 + grade3) / 3`

### 2. Weighted Mean
```yaml
grading:
  averaging_method: "weighted_mean"
```
**Use Case**: Prefer certain graders (recommended)
**Formula**: `(grade1×weight1 + grade2×weight2 + grade3×weight3) / (weight1 + weight2 + weight3)`

### 3. Median
```yaml
grading:
  averaging_method: "median"
```
**Use Case**: Robust against outliers
**Formula**: Middle value of sorted grades

### 4. Trimmed Mean
```yaml
grading:
  averaging_method: "trimmed_mean"
statistics:
  trim_percentage: 10.0
```
**Use Case**: Remove extreme values
**Formula**: Average after removing top/bottom 10% of grades

## Configuration Templates

### Template 1: Single Provider (Beginner)
```yaml
grading:
  runs_per_grader: 3
  averaging_method: "mean"
  
graders:
  - name: "claude-primary"
    provider: "anthropic"
    model: "claude-3-5-sonnet"
    weight: 1.0
    
execution:
  max_cost_per_student: 0.50
```

### Template 2: Multi-Provider Balanced
```yaml
grading:
  runs_per_grader: 2
  averaging_method: "weighted_mean"
  
graders:
  - name: "claude"
    provider: "anthropic"
    model: "claude-3-5-sonnet"
    weight: 1.5
    primary_feedback: true
    
  - name: "gpt4o"
    provider: "openai"
    model: "gpt-4o"
    weight: 1.5
    
  - name: "gemini"
    provider: "gemini"
    model: "gemini-1.5-pro"
    weight: 1.0
    
execution:
  max_cost_per_student: 1.00
```

### Template 3: Cost-Optimized
```yaml
grading:
  runs_per_grader: 1
  averaging_method: "weighted_mean"
  
graders:
  - name: "claude-haiku"
    provider: "anthropic"
    model: "claude-3-haiku"
    weight: 2.0
    
  - name: "gpt-mini"
    provider: "openai"
    model: "gpt-4o-mini"
    weight: 1.0
    
execution:
  max_cost_per_student: 0.25
  parallel_execution: false
```

### Template 4: High-Accuracy Research
```yaml
grading:
  runs_per_grader: 5
  averaging_method: "trimmed_mean"
  confidence_threshold: 0.9
  
graders:
  - name: "claude-sonnet"
    provider: "anthropic"
    model: "claude-3-5-sonnet"
    weight: 2.0
    
  - name: "gpt4o"
    provider: "openai"
    model: "gpt-4o"
    weight: 2.0
    
  - name: "gemini-pro"
    provider: "gemini"
    model: "gemini-1.5-pro"
    weight: 1.5
    
execution:
  max_cost_per_student: 2.00
  
statistics:
  trim_percentage: 15.0
  variance_analysis: true
  outlier_detection: true
```

## Execution Configuration

### Cost Controls
```yaml
execution:
  max_cost_per_student: 0.75    # USD limit per student
  cost_estimation: true         # Show cost preview
  budget_alerts: true           # Warn before exceeding
```

### Performance Tuning
```yaml
execution:
  parallel_execution: true      # Run graders simultaneously
  retry_attempts: 3            # Retry failed API calls
  rate_limit_delay: 1.0        # Seconds between requests
  timeout_seconds: 120         # Request timeout
  batch_size: 5               # Students processed together
```

### Error Handling
```yaml
execution:
  retry_attempts: 3
  retry_delay: 2.0
  fallback_provider: "anthropic"
  graceful_degradation: true
```

## Prompt Configuration

### System Prompt Customization
```yaml
prompts:
  system_prompt: |
    You are an expert academic grader with extensive experience in computer science education.
    You evaluate student work fairly, consistently, and constructively.
    
    Guidelines:
    - Provide specific, actionable feedback
    - Consider both technical correctness and approach
    - Account for partial credit where appropriate
    - Maintain consistent standards across all submissions
    
  rubric_integration: "automatic"
  feedback_style: "comprehensive"
```

### Feedback Configuration
```yaml
prompts:
  feedback_style: "comprehensive"  # Options: brief, moderate, comprehensive
  include_suggestions: true
  highlight_strengths: true
  provide_examples: true
  reference_rubric: true
```

## Advanced Configuration

### Dynamic Weighting
```yaml
graders:
  - name: "claude"
    provider: "anthropic"
    model: "claude-3-5-sonnet"
    weight: 2.0
    subject_weights:
      programming: 2.5
      documentation: 1.8
      design: 2.0
```

### Conditional Execution
```yaml
execution:
  conditions:
    - if: "assignment_type == 'programming'"
      then:
        runs_per_grader: 3
        max_cost_per_student: 1.00
    - if: "assignment_type == 'essay'"
      then:
        runs_per_grader: 2
        max_cost_per_student: 0.50
```

### Provider Fallbacks
```yaml
graders:
  - name: "primary"
    provider: "anthropic"
    model: "claude-3-5-sonnet"
    fallback:
      provider: "openai"
      model: "gpt-4o"
```

## Configuration Generation

### CLI Generation Commands
```bash
# Generate default configuration
mark-mate generate-config

# Generate specific template
mark-mate generate-config --template minimal
mark-mate generate-config --template cost-optimized
mark-mate generate-config --template single-provider --provider anthropic

# Custom output location
mark-mate generate-config --output custom_config.yaml --force
```

### GUI Configuration Builder
The GUI provides an interactive configuration builder:

1. **Template Selection**: Choose from pre-built templates
2. **Provider Configuration**: Select and configure LLM providers
3. **Statistical Options**: Choose aggregation methods
4. **Cost Controls**: Set budget limits
5. **Export Configuration**: Save for future use

## Configuration Validation

### Validation Checklist
- [ ] **API Keys**: All configured providers have valid keys
- [ ] **Model Names**: All models are correctly specified
- [ ] **Weight Logic**: Weights sum to reasonable values
- [ ] **Cost Limits**: Budget limits are appropriate
- [ ] **Statistical Settings**: Aggregation method matches needs

### Common Configuration Errors

#### Error: Invalid Model Names
```yaml
# ❌ Incorrect
model: "gpt-4-turbo"  # Should be "gpt-4o"

# ✅ Correct
model: "gpt-4o"
```

#### Error: Inconsistent Weights
```yaml
# ❌ Problematic (too extreme)
graders:
  - weight: 10.0
  - weight: 0.1

# ✅ Better (balanced)
graders:
  - weight: 2.0
  - weight: 1.0
```

#### Error: Insufficient Runs
```yaml
# ❌ Not reliable
runs_per_grader: 1
averaging_method: "trimmed_mean"  # Needs multiple runs

# ✅ Appropriate
runs_per_grader: 5
averaging_method: "trimmed_mean"
```

## Performance Optimization

### Speed vs Accuracy Trade-offs
```yaml
# Fast (lower accuracy)
grading:
  runs_per_grader: 1
  averaging_method: "mean"
execution:
  parallel_execution: true

# Accurate (slower)
grading:
  runs_per_grader: 5
  averaging_method: "trimmed_mean"
execution:
  parallel_execution: false  # More stable
```

### Cost Optimization Strategies
1. **Use Efficient Models**: Claude Haiku, GPT-4o Mini for simpler tasks
2. **Reduce Runs**: Fewer runs per grader for budget constraints
3. **Smart Weighting**: High weight on one accurate, low-cost model
4. **Batch Processing**: Process students in groups

## Integration Examples

### Course Management Integration
```yaml
# Configuration for different course types
course_configs:
  cs101:
    template: "cost-optimized"
    max_cost_per_student: 0.25
  cs401:
    template: "high-accuracy"
    max_cost_per_student: 1.50
```

### Assignment-Specific Configuration
```yaml
# Different settings per assignment type
assignment_configs:
  programming:
    focus_areas: ["correctness", "style", "efficiency"]
    runs_per_grader: 3
  essays:
    focus_areas: ["content", "structure", "grammar"]
    runs_per_grader: 2
```

---

**Related Documentation**:
- [Template Management](templates.md)
- [LLM Provider Configuration](../ai-prompts/llm-providers.md)
- [Cost Optimization Guide](../advanced/cost-optimization.md)