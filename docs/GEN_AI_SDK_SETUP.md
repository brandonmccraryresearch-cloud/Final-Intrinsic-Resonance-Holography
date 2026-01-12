# Gen AI SDK Setup for IRH AI Advisor

This guide explains how to set up and use Google's Gen AI SDK with the IRH Theory Evolution System's AI Advisor module.

## Overview

The AI Advisor module can leverage Google's Gen AI SDK (specifically Gemini models) to enhance its capability in generating topologically-motivated theoretical refinements. This integration provides:

- Advanced pattern recognition in error analysis
- AI-powered suggestions for topological corrections
- Natural language explanations of refinement strategies
- Search-augmented suggestions using Google Search integration

## Prerequisites

- Python 3.11+
- IRH computational environment installed
- Google Cloud API key with Gen AI API access

## Installation

### 1. Install the Gen AI SDK

```bash
# Upgrade to the latest version
pip install --upgrade google-genai
```

### 2. Configure API Key

#### For Local Development:

```bash
# Set environment variable in your shell
export GOOGLE_CLOUD_API_KEY="your_api_key_here"

# To make it persistent, add to ~/.bashrc or ~/.zshrc:
echo 'export GOOGLE_CLOUD_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

#### For GitHub Actions:

1. Navigate to your repository settings
2. Go to **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `GOOGLE_CLOUD_API_KEY`
5. Value: Your Google Cloud API key
6. Click **Add secret**

**Using the secret in workflows:**

```yaml
name: Evolution Cycle with Gen AI

on:
  workflow_dispatch:

jobs:
  run-evolution:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install mpmath numpy scipy
          pip install --upgrade google-genai
          
      - name: Run evolution cycle with Gen AI
        env:
          GOOGLE_CLOUD_API_KEY: ${{ secrets.GOOGLE_CLOUD_API_KEY }}
        run: |
          python3 << 'EOF'
          from evolution_system import AIAdvisor, ErrorAnalyzer
          
          # The API key is automatically available via environment variable
          advisor = AIAdvisor()
          
          # Check if Gen AI is enabled
          if advisor._genai_client:
              print("✅ Gen AI is enabled and ready")
              # Generate AI suggestions
              suggestions = advisor.get_genai_suggestions(analysis_dict)
          else:
              print("⚠️ Gen AI not available, using templates")
          EOF
```

See `.github/workflows/evolution-with-genai.yml` for a complete working example.

## Usage

### Basic Integration

```python
from google import genai
from google.genai import types
import os

def generate_ai_refinement_suggestions(error_analysis):
    """
    Use Gen AI to generate topologically-motivated refinements.
    
    Args:
        error_analysis: Dict containing error patterns from ErrorAnalyzer
        
    Returns:
        AI-generated refinement suggestions
    """
    client = genai.Client(
        vertexai=True,
        api_key=os.environ.get("GOOGLE_CLOUD_API_KEY"),
    )

    # Prepare prompt with error analysis context
    prompt = f"""
    You are an expert in topological quantum field theory, gauge theory, 
    and differential geometry. Given the following error patterns in 
    theoretical physics predictions:
    
    {error_analysis}
    
    Suggest topologically-motivated corrections that:
    1. Have clear geometric/topological origin (NO phenomenological fitting)
    2. Preserve all fundamental symmetries (gauge, Lorentz, CPT)
    3. Are derived from characteristic classes, Chern numbers, or fiber bundle geometry
    4. Can be validated experimentally
    
    Focus on corrections from:
    - Chern class corrections
    - Berry phases
    - Instanton contributions
    - Hopf fibration volume ratios
    - Braid group representations
    - Weyl anomaly coefficients
    """

    model = "gemini-3-pro-preview"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=prompt)]
        )
    ]
    
    tools = [
        types.Tool(google_search=types.GoogleSearch()),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=65535,
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
            )
        ],
        tools=tools,
        thinking_config=types.ThinkingConfig(
            thinking_level="HIGH",
        ),
    )

    response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue
        response += chunk.text
    
    return response
```

### Integration with AIAdvisor

```python
from evolution_system import AIAdvisor, ErrorAnalyzer, ValidationModule

# Standard workflow
analyzer = ErrorAnalyzer()
analysis = analyzer.analyze(validation_report)

# Option 1: Use built-in templates (no API required)
advisor = AIAdvisor()
suggestions = advisor.get_top_suggestions(analysis.to_dict(), n=5)

# Option 2: Enhance with Gen AI (requires API key)
if os.environ.get("GOOGLE_CLOUD_API_KEY"):
    ai_response = generate_ai_refinement_suggestions(analysis.to_dict())
    print("AI-Enhanced Suggestions:")
    print(ai_response)
    
    # Parse AI response and combine with template-based suggestions
    # (implementation depends on desired integration level)
```

## Configuration Options

### Model Selection

The Gen AI SDK supports multiple models:

- `gemini-3-pro-preview` - Latest Gemini 3 Pro (recommended for theoretical physics)
- `gemini-2.0-flash-exp` - Faster but less capable
- `gemini-1.5-pro` - Stable production model

```python
model = "gemini-3-pro-preview"  # Change as needed
```

### Temperature and Sampling

```python
generate_content_config = types.GenerateContentConfig(
    temperature=1,        # Higher = more creative (0-2)
    top_p=0.95,          # Nucleus sampling threshold
    max_output_tokens=65535,  # Maximum response length
    # ... other settings
)
```

### Thinking Configuration

For complex theoretical reasoning:

```python
thinking_config=types.ThinkingConfig(
    thinking_level="HIGH",  # "LOW", "MEDIUM", or "HIGH"
)
```

Higher thinking levels provide more detailed reasoning chains but take longer.

### Google Search Integration

Enable web search for the most recent research:

```python
tools = [
    types.Tool(google_search=types.GoogleSearch()),
]
```

This allows the model to search for recent papers on arXiv, PRD, JHEP, etc.

## Best Practices

### 1. Directive A Compliance

Always verify that AI-generated suggestions maintain topological origin:

```python
def validate_topological_origin(suggestion):
    """Ensure suggestion has clear geometric/topological basis."""
    required_keywords = [
        "Chern", "topology", "characteristic class", 
        "fiber bundle", "homotopy", "manifold", "gauge"
    ]
    
    has_topological_basis = any(
        keyword.lower() in suggestion.lower() 
        for keyword in required_keywords
    )
    
    phenomenological_flags = [
        "fit", "tune", "adjust parameter", "calibrate"
    ]
    
    is_phenomenological = any(
        flag.lower() in suggestion.lower()
        for flag in phenomenological_flags
    )
    
    return has_topological_basis and not is_phenomenological
```

### 2. Prompt Engineering

Structure prompts to constrain the AI to topological suggestions:

```python
prompt = f"""
CRITICAL CONSTRAINTS (Directive A):
- ❌ NO parameter tuning to fit data
- ❌ NO arbitrary scaling factors
- ❌ NO phenomenological formulas
- ✅ ONLY topological/geometric refinements
- ✅ ONLY modifications with clear mathematical origin

Given error patterns: {error_analysis}

Suggest ONLY corrections from:
1. Characteristic classes (Chern, Pontryagin, Stiefel-Whitney)
2. Homotopy invariants (winding numbers, Hopf invariant)
3. Fiber bundle geometry (holonomy, parallel transport)
4. Gauge theory (instanton corrections, anomalies)
5. Representation theory (braid groups, Lie algebras)
"""
```

### 3. Error Handling

```python
def safe_ai_suggestions(error_analysis):
    """Safely call Gen AI with fallback to templates."""
    try:
        if not os.environ.get("GOOGLE_CLOUD_API_KEY"):
            print("No API key found. Using built-in templates.")
            return None
        
        return generate_ai_refinement_suggestions(error_analysis)
    
    except Exception as e:
        print(f"Gen AI error: {e}")
        print("Falling back to built-in templates.")
        return None
```

### 4. Cost Management

Gen AI API calls have usage costs. To minimize:

```python
# Cache results
import json
from pathlib import Path

def cached_ai_suggestions(error_analysis, cache_file="ai_suggestions_cache.json"):
    """Use cached suggestions if available."""
    cache_path = Path(cache_file)
    
    # Check cache
    if cache_path.exists():
        with open(cache_path) as f:
            cache = json.load(f)
            
        # Use cached result if error analysis matches
        if cache.get("error_analysis") == error_analysis:
            print("Using cached AI suggestions")
            return cache.get("suggestions")
    
    # Generate new suggestions
    suggestions = generate_ai_refinement_suggestions(error_analysis)
    
    # Update cache
    with open(cache_path, 'w') as f:
        json.dump({
            "error_analysis": error_analysis,
            "suggestions": suggestions
        }, f, indent=2)
    
    return suggestions
```

## Testing

### Verify API Access

```python
import os
from google import genai

def test_gen_ai_access():
    """Test Gen AI SDK setup."""
    try:
        api_key = os.environ.get("GOOGLE_CLOUD_API_KEY")
        if not api_key:
            print("❌ GOOGLE_CLOUD_API_KEY not set")
            return False
        
        print("✅ API key found")
        
        # Test connection
        client = genai.Client(
            vertexai=True,
            api_key=api_key,
        )
        
        print("✅ Client initialized")
        
        # Simple test query
        response = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents="Say 'API test successful' if you can read this."
        )
        
        print(f"✅ API response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_gen_ai_access()
```

## Troubleshooting

### API Key Not Found

**Error:** `GOOGLE_CLOUD_API_KEY environment variable not set`

**Solution:**
```bash
# Check if variable is set
echo $GOOGLE_CLOUD_API_KEY

# If empty, set it:
export GOOGLE_CLOUD_API_KEY="your_key_here"
```

### Import Error

**Error:** `ModuleNotFoundError: No module named 'google.genai'`

**Solution:**
```bash
pip install --upgrade google-genai
```

### API Permission Denied

**Error:** `Permission denied` or `Invalid API key`

**Solution:**
1. Verify your API key is correct
2. Check that Gen AI API is enabled in your Google Cloud project
3. Ensure billing is enabled (API usage requires billing account)

### Rate Limiting

**Error:** `429 Too Many Requests`

**Solution:**
- Implement caching (see Best Practices above)
- Add exponential backoff:

```python
import time

def call_with_retry(func, max_retries=3):
    """Call function with exponential backoff on rate limit."""
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "429" in str(e) and i < max_retries - 1:
                wait_time = 2 ** i  # Exponential backoff: 1s, 2s, 4s
                print(f"Rate limited. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

## Security Considerations

### 1. API Key Protection

- **Never** commit API keys to Git
- Use environment variables or secrets management
- Rotate keys periodically
- Use separate keys for development and production

### 2. GitHub Actions Security

When using in workflows:

```yaml
- name: Run AI Advisor with Gen AI
  env:
    GOOGLE_CLOUD_API_KEY: ${{ secrets.GOOGLE_CLOUD_API_KEY }}
  run: |
    python evolution_system/ai_advisor.py
```

The key is injected at runtime and never exposed in logs.

### 3. Safety Settings

The provided safety settings disable content filtering for scientific discourse:

```python
safety_settings=[
    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
    # ... other categories
]
```

This is necessary for physics discussions (e.g., "strange quark", "charm decay") but should be used responsibly.

## References

- [Google Gen AI SDK Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/python-sdk)
- [Gemini API Reference](https://ai.google.dev/api)
- [Evolution System README](../evolution_system/README.md)
- [AI Advisor Module](../evolution_system/ai_advisor.py)

## Support

For issues specific to:
- **Gen AI SDK**: See [Google's support](https://cloud.google.com/support)
- **IRH Integration**: Open an issue on GitHub
- **API Costs**: Check [Google Cloud Pricing](https://cloud.google.com/vertex-ai/pricing)

---

*Last updated: 2026-01-10*
