# IRH Theory Evolution System

An AI-guided framework for continuously improving the Intrinsic Resonance Holography (IRH) theoretical predictions through systematic error analysis and synoptic refinement.

## Overview

The Theory Evolution System enables the IRH framework to self-improve by:
1. Computing all theoretical predictions from topological invariants
2. Validating predictions against experimental measurements
3. Analyzing error patterns to identify systematic discrepancies
4. Suggesting topologically-motivated refinements (no phenomenological fitting)
5. Testing and integrating successful refinements
6. Automatically documenting all changes

## Installation

### Core Dependencies

```bash
# From repository root
pip install -e .

# Or install dependencies manually
pip install mpmath numpy
```

### Gen AI SDK (for AI Advisor)

The AI Advisor module can optionally use Google's Gen AI SDK for enhanced AI-powered theoretical refinement suggestions.

**Installation:**

```bash
# Install the Gen AI SDK
pip install --upgrade google-genai
```

**Configuration:**

Set your Google Cloud API key as an environment variable:

```bash
export GOOGLE_CLOUD_API_KEY="YOUR_API_KEY"
```

For GitHub Actions workflows, add `GOOGLE_CLOUD_API_KEY` as a repository secret.

**Example Usage:**

```python
from google import genai
from google.genai import types
import os

def generate_refinement_suggestions():
    """Use Gen AI to generate topologically-motivated refinements."""
    client = genai.Client(
        vertexai=True,
        api_key=os.environ.get("GOOGLE_CLOUD_API_KEY"),
    )

    model = "gemini-3-pro-preview"
    contents = [
        types.Content(
            role="user",
            parts=[
                # Add your prompt here for refinement suggestions
            ]
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

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue
        print(chunk.text, end="")

# Use in AI Advisor
generate_refinement_suggestions()
```

**Note:** The Gen AI integration is optional. The AI Advisor can function using built-in topological modification templates without requiring external API access.

**Example:** See [examples/genai_advisor_example.py](../examples/genai_advisor_example.py) for a complete demonstration of Gen AI SDK integration.

**GitHub Actions:** To run evolution cycles with Gen AI in CI/CD:
1. Add your `GOOGLE_CLOUD_API_KEY` as a repository secret
2. Use the workflow at `.github/workflows/evolution-with-genai.yml`
3. Trigger manually via "Actions" tab or on schedule (weekly)
4. Results are saved as artifacts and displayed in job summary

## Quick Start

### Option 1: Run Complete Evolution Cycle (Recommended)

```python
from evolution_system import EvolutionCycle

# Run a complete evolution cycle
cycle = EvolutionCycle()
result = cycle.run(max_refinements=5)

# Print summary
print(f"Cycle completed: {result.status}")
print(f"Refinements tested: {result.refinements_tested}")
print(f"Refinements integrated: {result.refinements_integrated}")
```

### Option 2: Command-Line Interface

```bash
# Run single cycle with default settings
python -m evolution_system.evolution_cycle

# Run 3 cycles with 10 refinements each
python -m evolution_system.evolution_cycle --cycles 3 --max-refinements 10

# Auto-integrate successful refinements
python -m evolution_system.evolution_cycle --auto-integrate

# Export results to custom path
python -m evolution_system.evolution_cycle --output results/cycle.json
```

### Option 3: Run Components Individually

```python
from evolution_system import (
    CalculationEngine,
    ExperimentalDatabase,
    ValidationModule,
    ErrorAnalyzer,
    AIAdvisor,
    IntegrationSystem,
    DocumentationUpdater
)

# 1. Load experimental database
db = ExperimentalDatabase()
print(f"Loaded {db.count()} experimental constants")

# 2. Compute all theoretical predictions
engine = CalculationEngine()
predictions = engine.compute_all_predictions()
engine.print_summary()

# 3. Validate against experiments
validator = ValidationModule(db)
report = validator.validate_all(predictions)
validator.print_validation_report(report)

# 4. Analyze error patterns
analyzer = ErrorAnalyzer()
analysis = analyzer.analyze(report)
analyzer.print_analysis(analysis)

# 5. Get refinement suggestions
advisor = AIAdvisor()
suggestions = advisor.get_top_suggestions(analysis.to_dict(), n=5)

# 6. Test and integrate refinements
integrator = IntegrationSystem()
doc_updater = DocumentationUpdater()

for suggestion in suggestions:
    result = integrator.test_refinement(suggestion)
    if result.is_valid:
        integrator.integrate_refinement(suggestion, result)
        doc_updater.update_changelog(
            doc_updater.create_changelog_entry(result, suggestion)
        )
        print(f"Integrated: {suggestion.modification.name}")
```

## Modules

### ExperimentalDatabase

Comprehensive database of experimental values from:
- **CODATA 2022**: Fundamental physical constants
- **PDG 2022**: Particle physics properties
- **Planck 2018**: Cosmological parameters

```python
from evolution_system import ExperimentalDatabase

db = ExperimentalDatabase()

# Get specific constant
alpha = db.get('alpha_inv')
print(f"α⁻¹ = {alpha.value} ± {alpha.uncertainty}")

# Get by tier
tier1 = db.get_tier(1)  # Core parameters

# Get by category
leptons = db.get_category('lepton_masses')
```

**Important:** All experimental values are marked "FOR VALIDATION ONLY" per Directive A.

### CalculationEngine

Computes theoretical predictions from topological invariants.

```python
from evolution_system import CalculationEngine

engine = CalculationEngine()

# Compute individual predictions
alpha = engine.compute_fine_structure_constant()
eta = engine.compute_metric_mismatch()
koide = engine.compute_koide_formula()

# Compute all predictions
predictions = engine.compute_all_predictions()
```

**Current Predictions:**
- α⁻¹ (fine-structure constant)
- η (metric mismatch = 4/π)
- Q (Koide ratio = 2/3)
- α_s, α₁, α₂ (gauge couplings)
- sin²θ_W (weak mixing angle)
- M_X (GUT scale)
- ΩΛ, ΩDM, Ωb (cosmological ratios)

### ValidationModule

Compares theoretical predictions to experimental measurements.

```python
from evolution_system import ValidationModule, CalculationEngine

engine = CalculationEngine()
predictions = engine.compute_all_predictions()

validator = ValidationModule()
report = validator.validate_all(predictions)

# Check results
print(f"Excellent: {report.excellent_count}")  # Within 1σ
print(f"Good: {report.good_count}")            # 1-3σ
print(f"Fair: {report.fair_count}")            # 3-5σ
print(f"Poor: {report.poor_count}")            # >5σ

# Get discrepant predictions
discrepant = report.get_discrepant(sigma_threshold=3.0)
```

### ErrorAnalyzer

Identifies systematic error patterns and suggests refinements.

```python
from evolution_system import ErrorAnalyzer

analyzer = ErrorAnalyzer()
analysis = analyzer.analyze(report)

# View patterns
for pattern in analysis.patterns:
    print(f"{pattern.severity.value}: {pattern.description}")

# Get suggestions
for suggestion in analysis.suggestions:
    print(f"Suggestion: {suggestion.title}")
    print(f"  Topological origin: {suggestion.topological_origin}")
```

**Pattern Types:**
- Systematic offset (predictions all too high/low)
- Scale-dependent (errors vary with energy)
- Sector-specific (e.g., gauge sector issues)
- Individual outliers (>3σ discrepancies)

## Directive Compliance

This system strictly adheres to IRH Directives:

### Directive A: No-Tuning Constraint
- All constants derived from topological invariants
- Experimental values ONLY for validation, never as inputs
- No phenomenological fitting or parameter adjustment

### Directive B: CODATA Precision
- All calculations use arbitrary precision (mpmath)
- Comparisons include σ-deviations and relative errors
- Results compared to latest CODATA 2022 values

### Directive C: Rigorous Formalism
- Forces described as "curvature in connections"
- Particles as "B₃ resonant modes"
- Standard gauge theory terminology

## Tests

Run the test suite:

```bash
cd /path/to/IRHV24
python -m pytest tests/test_evolution_system.py -v
```

## Documentation

- **Design Document**: [docs/THEORY_EVOLUTION_SYSTEM.md](../docs/THEORY_EVOLUTION_SYSTEM.md) - Full design specification
- **Gen AI SDK Setup**: [docs/GEN_AI_SDK_SETUP.md](../docs/GEN_AI_SDK_SETUP.md) - Detailed guide for AI Advisor integration

## Status

**Phase 1: Infrastructure** - Complete ✅
- [x] Experimental database
- [x] Calculation engine
- [x] Validation module
- [x] Error analyzer
- [ ] Full Standard Model coverage

**Phase 2: AI Advisor Development** - Complete ✅
- [x] Topological modification templates
- [x] Suggestion ranking algorithms
- [x] Directive A compliance filtering

**Phase 3: Integration System** - Complete ✅
- [x] Isolated testing environment
- [x] Regression testing suite
- [x] Symmetry preservation checks
- [x] Topological origin verification
- [x] Automated documentation updates
- [x] Changelog generation

**Phase 4: Full System Operation** - Complete ✅
- [x] Evolution cycle orchestrator
- [x] Command-line interface
- [x] Multi-cycle execution
- [x] Progress tracking and reporting
- [x] Results export to JSON
- [ ] First production evolution cycle (ready to run)
