"""
IRH Theory Evolution System
===========================

An AI-guided framework for continuously improving the Intrinsic Resonance Holography (IRH)
theoretical predictions through systematic error analysis and synoptic refinement.

**Status:** Phase 4 Full System Operation + Gemini 3 Pro Integration - Ready

**Goal:** Enable the IRH framework to self-improve by learning from prediction errors and
automatically suggesting theoretical refinements based on topological and geometric principles.

Modules:
--------
- calculation_engine: Execute all IRH predictions with high precision
- experimental_database: Comprehensive database of CODATA, PDG, and Planck values
- validation_module: Compare theoretical predictions to experimental measurements
- error_analyzer: Identify systematic patterns in prediction errors
- ai_advisor: Generate topologically-motivated refinement suggestions
- gemini_integration: 🆕 Gemini 3 Pro AI-powered theory examination and refinement
- integration_system: Validate and integrate successful refinements (Phase 3)
- documentation_updater: Automatic documentation and changelog updates (Phase 3)
- evolution_cycle: Complete evolution cycle orchestration (Phase 4)

**Key Principle:** The system does NOT tune parameters to fit data. Instead, it suggests
*deeper topological structures* that could explain observed deviations.

Usage:
------
```python
from evolution_system import EvolutionCycle

# Run a complete evolution cycle (recommended)
cycle = EvolutionCycle()
result = cycle.run(max_refinements=5)
cycle.print_summary()

# Or run individual components
from evolution_system import (
    CalculationEngine, ValidationModule, ErrorAnalyzer, 
    AIAdvisor, GeminiTheoryAdvisor, IntegrationSystem, DocumentationUpdater
)

# Initialize components
engine = CalculationEngine()
validator = ValidationModule()
analyzer = ErrorAnalyzer()
advisor = AIAdvisor()
gemini = GeminiTheoryAdvisor()  # 🆕 Gemini 3 Pro integration
integrator = IntegrationSystem()
doc_updater = DocumentationUpdater()

# Run evolution cycle manually
predictions = engine.compute_all_predictions()
validation_report = validator.validate_all(predictions)
error_analysis = analyzer.analyze(validation_report)

# Get AI-powered improvement suggestions
suggestions = advisor.get_top_suggestions(error_analysis, n=5)

# 🆕 Use Gemini for deep theory examination
theory_text = open('README.md').read()
examination = gemini.self_examine(theory_text, ['hardcoded values', 'testability'])
refinements = gemini.suggest_refinements(theory_text, error_analysis.to_dict())

# Test and integrate refinements
for suggestion in suggestions:
    result = integrator.test_refinement(suggestion)
    if result.is_valid:
        integrator.integrate_refinement(suggestion, result)
        doc_updater.update_changelog(
            doc_updater.create_changelog_entry(result, suggestion)
        )
        print(f"Integrated: {suggestion.modification.name}")
```

Command-Line Interface:
-----------------------
```bash
# Run a single evolution cycle
python -m evolution_system.evolution_cycle

# Run 3 cycles with 10 refinements each
python -m evolution_system.evolution_cycle --cycles 3 --max-refinements 10

# Auto-integrate successful refinements
python -m evolution_system.evolution_cycle --auto-integrate

# 🆕 Use Gemini for theory examination
python scripts/gemini_theory_examiner.py --analysis-type self-examine
```

References:
-----------
- docs/THEORY_EVOLUTION_SYSTEM.md: Full design document
- docs/GEMINI_INTEGRATION.md: 🆕 Gemini 3 Pro integration guide
- notebooks/06_validation_suite.ipynb: Validation implementation
- verification/precision/constants.py: High-precision constant calculations
"""

__version__ = "0.5.0"  # 🆕 Added Gemini 3 Pro integration
__author__ = "IRH Computational Research Team"
__all__ = [
    # Calculation
    'CalculationEngine',
    'PredictionResult',
    # Database
    'ExperimentalDatabase', 
    # Validation
    'ValidationModule',
    'ValidationResult',
    # Error Analysis
    'ErrorAnalyzer',
    'ErrorPattern',
    # AI Advisor
    'AIAdvisor',
    'RefinementSuggestion',
    'TopologicalModification',
    # Gemini Integration (NEW)
    'GeminiTheoryAdvisor',
    # Integration System (Phase 3)
    'IntegrationSystem',
    'IntegrationResult',
    'IntegrationStatus',
    'RegressionTestResult',
    # Documentation Updater (Phase 3)
    'DocumentationUpdater',
    'ChangelogEntry',
    # Evolution Cycle (Phase 4)
    'EvolutionCycle',
    'CycleResult',
]

from .calculation_engine import CalculationEngine, PredictionResult
from .experimental_database import ExperimentalDatabase
from .validation_module import ValidationModule, ValidationResult
from .error_analyzer import ErrorAnalyzer, ErrorPattern
from .ai_advisor import AIAdvisor, RefinementSuggestion, TopologicalModification
from .gemini_integration import GeminiTheoryAdvisor  # 🆕 NEW
from .integration_system import (
    IntegrationSystem, 
    IntegrationResult, 
    IntegrationStatus,
    RegressionTestResult
)
from .documentation_updater import DocumentationUpdater, ChangelogEntry
from .evolution_cycle import EvolutionCycle, CycleResult
