# Gemini Integration Examples

This directory contains example scripts demonstrating how to use the Gemini 3 Pro integration for IRH theory development.

## Available Examples

### 1. `simple_gemini_example.py` - Basic Integration

**Purpose**: Demonstrates the core Gemini 3 Pro API integration exactly as specified in the project requirements.

**Features**:
- Direct API usage with system instructions
- HIGH thinking level for deep reasoning
- Integrated tools (code execution, search, URL context)
- Streaming response output

**Usage**:
```bash
export GEMINI_API_KEY="your_api_key_here"
python examples/simple_gemini_example.py
```

**What it does**:
- Analyzes IRH's fine-structure constant derivation
- Identifies mathematical gaps
- Suggests topological refinements
- Compares with experimental precision

### 2. `genai_advisor_example.py` - AI Advisor Integration

**Purpose**: Shows how to integrate Gemini with the existing evolution system AI advisor.

**Features**:
- Combines template-based and AI-enhanced suggestions
- Error pattern analysis
- Validation against experimental data
- Fallback to built-in templates if Gemini unavailable

**Usage**:
```bash
export GOOGLE_CLOUD_API_KEY="your_api_key_here"
python examples/genai_advisor_example.py
```

**What it does**:
- Computes theoretical predictions
- Validates against experiments
- Analyzes error patterns
- Generates both template-based and AI-enhanced suggestions

## Quick Start

### Installation

```bash
# Install dependencies
pip install google-genai

# Or use conda environment
conda env create -f ../environment.yml
conda activate irh-compute
```

### Get API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Set environment variable:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

### Run Examples

```bash
# Basic example
python examples/simple_gemini_example.py

# AI advisor example
export GOOGLE_CLOUD_API_KEY="$GEMINI_API_KEY"
python examples/genai_advisor_example.py
```

## Understanding the Output

### Streaming Response

Both examples use streaming output, showing:
- **Text**: Generated analysis in real-time
- **[EXECUTABLE CODE]**: Python code Gemini generates for validation
- **[CODE EXECUTION RESULT]**: Output from executed code

### Thinking Time

With `thinking_level="HIGH"`, expect:
- **30-60 seconds** initial delay for deep reasoning
- **Progressive output** as analysis develops
- **Self-correction** during generation

### Response Format

Typical response includes:
1. **Problem Analysis**: Understanding the question
2. **Mathematical Derivation**: Step-by-step calculations
3. **Code Validation**: Numerical verification
4. **Critical Assessment**: Identifying gaps
5. **Refinement Suggestions**: Specific improvements

## Customizing Examples

### Modify the Prompt

Edit `user_prompt` in `simple_gemini_example.py`:

```python
user_prompt = """
Your custom question or analysis request here.

Be specific about:
1. What aspect of theory to analyze
2. What depth of analysis needed
3. What output format desired
"""
```

### Adjust Thinking Level

Change thinking depth in `generate_content_config`:

```python
thinking_config=types.ThinkingConfig(
    thinking_level="MEDIUM",  # Options: LOW, MEDIUM, HIGH
)
```

- **LOW**: Fast, surface-level analysis (~10s)
- **MEDIUM**: Balanced reasoning (~30s)
- **HIGH**: Deep, rigorous analysis (~60s+)

### Enable/Disable Tools

Control which tools Gemini can use:

```python
tools = [
    types.Tool(code_execution=types.ToolCodeExecution),  # Mathematical validation
    types.Tool(googleSearch=types.GoogleSearch()),       # Literature search
    types.Tool(url_context=types.UrlContext()),          # Online resources
]
```

Remove tools you don't need for faster responses.

## Advanced Usage

### Batch Analysis

Analyze multiple theory versions:

```bash
for version in v25 v26 v44 v57; do
    python examples/simple_gemini_example.py \
        --theory-file "IRH${version}.md" \
        --output "analysis_${version}.json"
done
```

### Integration with Notebooks

Use in Jupyter notebooks:

```python
from evolution_system.gemini_integration import GeminiTheoryAdvisor

advisor = GeminiTheoryAdvisor()
result = advisor.analyze_theory(theory_text, "mathematical")
print(result)
```

### Custom System Instructions

Modify system instructions for domain-specific analysis:

```python
custom_instruction = """
Focus exclusively on:
1. Topological invariants
2. Gauge theory formalism
3. Experimental testability

Ignore:
- Philosophical interpretations
- Alternative formulations
"""

# Use in generate_content_config
```

## Example Output

### Sample Response

```
======================================================================
GEMINI 3 PRO - IRH THEORY ANALYSIS
======================================================================

Generating response with HIGH thinking level...
This may take 30-90 seconds for deep reasoning.

======================================================================

## Analysis of Fine-Structure Constant Derivation

The Intrinsic Resonance Holography framework proposes deriving α 
from Hopf fibration volume ratios. Let me analyze this rigorously:

### 1. Mathematical Framework

The proposed derivation starts with:
α⁻¹ = (Vol(S⁷)/Vol(S³)) × η

where η = 4/π is the metric mismatch factor.

[EXECUTABLE CODE]
import numpy as np

# Compute Hopf fibration volume ratios
vol_S7 = (np.pi**4) / 24
vol_S3 = 2 * np.pi**2
eta = 4 / np.pi

alpha_inv = (vol_S7 / vol_S3) * eta
print(f"Predicted α⁻¹ = {alpha_inv:.6f}")
print(f"Experimental α⁻¹ = 137.035999...")

[CODE EXECUTION RESULT]
Predicted α⁻¹ = 137.333333
Experimental α⁻¹ = 137.035999...

### 2. Critical Assessment

**Strengths:**
- Pure topological origin
- No free parameters
- Dimensionally consistent

**Gaps Identified:**
1. Missing higher-order corrections (Chern classes)
2. No renormalization group flow
3. Geometric berry phase not accounted for

### 3. Suggested Refinements

...
```

## Troubleshooting

### Common Issues

**"ImportError: No module named 'google'"**
```bash
pip install google-genai
```

**"API key not found"**
```bash
export GEMINI_API_KEY="your_key"
```

**"Rate limit exceeded"**
- Wait 60 seconds and retry
- Check quota at [AI Studio](https://aistudio.google.com)

**"Response timeout"**
- Normal with HIGH thinking level
- Wait patiently (up to 2 minutes)

**"No response generated"**
- Check API key is valid
- Verify internet connection
- Try simpler prompt

## Performance Tips

1. **Start with MEDIUM thinking**: Test prompts quickly
2. **Use HIGH for final analysis**: When you need rigor
3. **Limit theory text size**: <100k chars for best performance
4. **Cache repeated analyses**: Save results to files
5. **Batch overnight**: Long analyses during off-hours

## Next Steps

After running examples:

1. **Review output quality**: Does it meet your needs?
2. **Customize for your use case**: Modify prompts and settings
3. **Integrate into workflow**: Add to validation pipeline
4. **Create new examples**: Share with team
5. **Provide feedback**: Help improve the system

## Resources

- **Gemini API Docs**: https://ai.google.dev/
- **System Instructions**: See `evolution_system/gemini_integration.py`
- **Full Documentation**: See `docs/GEMINI_INTEGRATION.md`
- **Command-Line Tool**: See `scripts/gemini_theory_examiner.py`

## Contributing

To add new examples:

1. Create new script in `examples/`
2. Follow naming: `<purpose>_gemini_example.py`
3. Add documentation to this README
4. Include error handling and usage instructions
5. Test with and without API key set

---

**Last Updated**: 2026-01-12  
**Examples**: 2 scripts  
**Status**: Production Ready
