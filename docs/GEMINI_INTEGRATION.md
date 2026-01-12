# Gemini 3 Pro Integration for IRH Theory Development

This document describes the integration of Google's Gemini 3 Pro AI model into the IRH computational research framework for advanced theory analysis, self-examination, and refinement.

## Overview

The Gemini 3 Pro integration provides:

- **Self-Examination Modules**: Critical analysis of theory for potential issues
- **Theory Refinement**: AI-powered suggestions for improving predictions
- **Mathematical Validation**: Rigorous checking of derivations and consistency
- **Physical Interpretation**: Analysis of observables and testability
- **Novel Predictions**: Generation of new testable predictions

## Architecture

### Core Components

1. **`evolution_system/gemini_integration.py`**: Main integration module
   - `GeminiTheoryAdvisor` class for theory analysis
   - Streaming response handling
   - Multi-modal tool integration (code execution, search, URL context)

2. **`scripts/gemini_theory_examiner.py`**: Command-line interface
   - Easy-to-use script for running analyses
   - Multiple analysis modes
   - JSON result export

3. **System Instructions**: Embedded prime directives
   - Nobel-level intellectual rigor
   - Scientific method enforcement
   - Vibrational ontology terminology guidance

## Installation

### Prerequisites

```bash
# Install google-genai package
pip install google-genai

# Or use the conda environment
conda env create -f environment.yml
conda activate irh-compute
```

### API Key Setup

```bash
# Set your Gemini API key
export GEMINI_API_KEY="your_api_key_here"

# Or add to your shell profile
echo 'export GEMINI_API_KEY="your_key"' >> ~/.bashrc
source ~/.bashrc
```

## Usage

### Command-Line Interface

#### Self-Examination (Recommended)

```bash
# Critical self-examination of current theory
python scripts/gemini_theory_examiner.py --analysis-type self-examine

# With specific concerns
python scripts/gemini_theory_examiner.py \
    --analysis-type self-examine \
    --concerns "hardcoded values" "gauge terminology" "testable predictions"
```

#### Theory Analysis

```bash
# Comprehensive analysis
python scripts/gemini_theory_examiner.py --analysis-type comprehensive

# Mathematical rigor focus
python scripts/gemini_theory_examiner.py --analysis-type mathematical

# Physical content focus
python scripts/gemini_theory_examiner.py --analysis-type physical

# Internal consistency check
python scripts/gemini_theory_examiner.py --analysis-type consistency
```

#### Refinement Suggestions

```bash
# Generate refinement suggestions
python scripts/gemini_theory_examiner.py --refinements

# Save to custom output file
python scripts/gemini_theory_examiner.py \
    --refinements \
    --output refinement_suggestions.json
```

#### Custom Theory Files

```bash
# Analyze specific theory version
python scripts/gemini_theory_examiner.py \
    --theory-file docs/IRHv44.md \
    --analysis-type comprehensive
```

### Python API

#### Basic Usage

```python
from evolution_system.gemini_integration import GeminiTheoryAdvisor

# Initialize advisor
advisor = GeminiTheoryAdvisor()

# Load theory
with open('README.md', 'r') as f:
    theory_text = f.read()

# Perform self-examination
examination = advisor.self_examine(
    theory_text,
    specific_concerns=[
        "Hardcoded experimental values",
        "Mathematical rigor of derivations",
        "Testable predictions"
    ]
)

print(examination)
```

#### Advanced Analysis

```python
# Mathematical consistency analysis
math_analysis = advisor.analyze_theory(
    theory_text,
    analysis_type="mathematical"
)

# Generate refinement suggestions
refinements = advisor.suggest_refinements(
    theory_text,
    error_patterns={
        'fine_structure_constant': {'error': 0.0001, 'sigma': 0.5},
        'electron_mass': {'error': 0.02, 'sigma': 2.1}
    }
)
```

#### Custom Prompts

```python
# Direct prompt generation
response = advisor.generate_response(
    """Analyze how the 4-strand network topology constrains
    the fine-structure constant. Provide a detailed derivation
    showing each step from topological invariants to α."""
)
```

## Analysis Types

### 1. Comprehensive Analysis

**Purpose**: Full evaluation covering all aspects

**Covers**:
- Mathematical consistency and rigor
- Physical interpretability
- Derivation completeness
- Experimental testability
- Novel predictions
- Comparison with SM/GR
- Gaps and refinements

**Best For**: Initial theory evaluation, major revisions

### 2. Mathematical Analysis

**Purpose**: Rigorous mathematical validation

**Covers**:
- Axiomatic foundation
- Logical consistency
- Dimensional analysis
- Mathematical completeness
- Convergence behavior
- Topological/geometric rigor

**Best For**: Post-derivation validation, mathematical papers

### 3. Physical Analysis

**Purpose**: Physical content and testability

**Covers**:
- Observable definitions
- Correspondence to known physics
- Ontological clarity
- Experimental predictions
- Novel phenomena
- Data comparison

**Best For**: Experimental proposals, phenomenology

### 4. Consistency Check

**Purpose**: Internal consistency validation

**Covers**:
- Logical contradictions
- Ad hoc assumptions
- Incompatible hypotheses
- Dimensional inconsistencies
- Conservation law violations
- Gauge/symmetry issues

**Best For**: Pre-publication review, theory debugging

### 5. Self-Examination (Recommended)

**Purpose**: Critical self-assessment for improvement

**Covers**:
- Foundational issues
- Mathematical gaps
- Physical concerns
- Methodological issues
- Severity-rated problems
- Specific remediation steps

**Best For**: Continuous improvement, addressing feedback

## Features

### HIGH Thinking Level

Gemini 3 Pro is configured with `thinking_level="HIGH"` for deep reasoning:

- Extended contemplation time (30-60+ seconds)
- Multi-step logical chains
- Self-correction during generation
- Rigorous mathematical checking
- Cross-domain synthesis

### Integrated Tools

The integration enables Gemini to use:

1. **Code Execution**: Mathematical verification and numerical validation
2. **Google Search**: Cross-referencing literature and experimental data
3. **URL Context**: Accessing online physics resources

### Streaming Output

Real-time display of:
- Generated text
- Executable code
- Code execution results
- Tool usage

## System Instructions

The Gemini model is instructed with:

### Prime Directives

1. **NO SUMMARIZATION**: Complete, thorough responses
2. **Nobel-Level Rigor**: Exceptional intellectual depth
3. **Mathematical Precision**: Rigorous formal treatment
4. **Scientific Method**: Falsifiability and testability
5. **Vibrational Ontology**: Cymatic/resonance terminology

### Scientific Standards

- Explicit assumptions
- Falsifiable predictions
- Acknowledged uncertainties
- Empirical grounding
- Provisional truth

### Terminology Guidance

Preferred vibrational vocabulary:
- "Cymatic Resonance Network" (not "hypergraph")
- "Harmony Functional" (not "action")
- "Coherence Connections" (gauge fields)
- "Harmonic Crystallization" (phase transitions)

## Output Format

### JSON Results Structure

```json
{
  "timestamp": "2026-01-12T18:30:00.000Z",
  "theory_file": "README.md",
  "theory_length": 50000,
  "analysis_type": "self-examine",
  "status": "success",
  "results": {
    "self_examination": "... Gemini analysis output ..."
  }
}
```

### Severity Levels

- **CRITICAL**: Must fix before publication
- **MAJOR**: Should fix for theoretical rigor
- **MINOR**: Nice to have improvements
- **INFO**: Suggestions for future work

## Best Practices

### 1. Iterative Refinement

```bash
# 1. Initial self-examination
python scripts/gemini_theory_examiner.py --analysis-type self-examine

# 2. Address CRITICAL issues

# 3. Re-examine
python scripts/gemini_theory_examiner.py --analysis-type self-examine

# 4. Get refinement suggestions
python scripts/gemini_theory_examiner.py --refinements

# 5. Implement refinements

# 6. Final consistency check
python scripts/gemini_theory_examiner.py --analysis-type consistency
```

### 2. Focused Analysis

Use specific concerns for targeted examination:

```bash
python scripts/gemini_theory_examiner.py \
    --analysis-type self-examine \
    --concerns \
        "Derive α from pure topology (no experimental input)" \
        "Koide formula derivation from vibrational modes" \
        "Cosmological constant suppression mechanism"
```

### 3. Version Tracking

Save results for each theory version:

```bash
python scripts/gemini_theory_examiner.py \
    --theory-file IRHv57.md \
    --analysis-type comprehensive \
    --output results/gemini_analysis_v57.json
```

### 4. Pre-Publication Review

Before any publication or major announcement:

```bash
# Full battery of checks
python scripts/gemini_theory_examiner.py --analysis-type mathematical
python scripts/gemini_theory_examiner.py --analysis-type physical
python scripts/gemini_theory_examiner.py --analysis-type consistency
python scripts/gemini_theory_examiner.py --refinements
```

## Integration with Existing Systems

### Evolution System

The Gemini integration works alongside:

- `ai_advisor.py`: Template-based suggestions
- `error_analyzer.py`: Pattern detection
- `validation_module.py`: Experimental comparison
- `calculation_engine.py`: Numerical predictions

### Computational Notebooks (Future)

New notebooks will integrate Gemini for:

- Real-time derivation checking
- Alternative formulation suggestions
- Numerical method optimization
- Result interpretation

## Performance

### Response Times

- **Self-examination**: 30-90 seconds
- **Comprehensive analysis**: 60-120 seconds
- **Mathematical analysis**: 45-90 seconds
- **Refinement suggestions**: 60-120 seconds

Times vary with:
- Theory complexity
- Tool usage (code execution, search)
- Thinking depth required

### Rate Limits

Gemini API has rate limits:
- Check your quota at [Google AI Studio](https://aistudio.google.com)
- Implement exponential backoff for production use
- Consider batching analyses

## Troubleshooting

### Common Issues

**1. "Gemini client not initialized"**
```bash
# Check API key is set
echo $GEMINI_API_KEY

# Set if missing
export GEMINI_API_KEY="your_key_here"
```

**2. "google-genai not installed"**
```bash
pip install google-genai
# or
conda activate irh-compute
```

**3. Rate limit errors**
```bash
# Wait and retry with exponential backoff
# Or upgrade API quota
```

**4. Long response times**
```bash
# This is normal with HIGH thinking level
# Wait patiently for deep reasoning
```

**5. Incomplete responses**
```bash
# Reduce theory text size
python scripts/gemini_theory_examiner.py --max-chars 50000
```

## Security Considerations

- **API Key Protection**: Never commit API keys to git
- **Theory Privacy**: Gemini processes theory text in Google's cloud
- **Rate Limiting**: Implement backoff to avoid quota exhaustion
- **Result Sanitization**: Review AI suggestions before implementation

## Future Enhancements

Planned features:

1. **Multi-Turn Dialogue**: Interactive theory refinement sessions
2. **Automated Testing**: Generate test cases for predictions
3. **Literature Integration**: Automatic citation of relevant papers
4. **Visualization**: AI-generated diagrams and plots
5. **Collaborative Review**: Multi-agent consensus building

## Examples

### Example 1: Self-Examination

```bash
$ python scripts/gemini_theory_examiner.py --analysis-type self-examine

======================================================================
IRH Theory Self-Examination with Gemini 3 Pro
======================================================================

🚀 Initializing Gemini 3 Pro...
✅ Gemini 3 Pro ready

📖 Loading theory from: README.md
✅ Loaded 43527 characters

🔍 Performing critical self-examination...
   (This may take 1-2 minutes with HIGH thinking level)

======================================================================
GEMINI 3 PRO RESPONSE
======================================================================

[Detailed analysis output...]

✅ Analysis complete!

✅ Results saved to: gemini_analysis_results.json

======================================================================
ANALYSIS SUMMARY
======================================================================
Theory file: README.md
Analysis type: self-examine
Status: success
Response length: 15234 characters
Results saved: gemini_analysis_results.json
======================================================================
```

### Example 2: Mathematical Rigor Check

```bash
$ python scripts/gemini_theory_examiner.py --analysis-type mathematical --output math_check_v57.json
```

### Example 3: Generate Refinements

```bash
$ python scripts/gemini_theory_examiner.py --refinements
```

## Contributing

To extend the Gemini integration:

1. Add new analysis types in `GeminiTheoryAdvisor.analyze_theory()`
2. Create custom prompts for specific use cases
3. Implement result parsers for structured data extraction
4. Add integration with computational notebooks
5. Develop multi-agent collaboration protocols

## License

This integration follows the repository's MIT License. Gemini API usage is subject to Google's terms of service.

## Support

For issues or questions:

1. Check this documentation
2. Review Gemini API docs: https://ai.google.dev/
3. Open a GitHub issue
4. Contact: IRH Computational Research Team

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-12  
**Status**: Production Ready
