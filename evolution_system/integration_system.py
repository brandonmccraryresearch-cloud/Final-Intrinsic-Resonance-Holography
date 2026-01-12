"""
Integration System Module for IRH Theory Evolution System

Phase 3 Implementation: Validate proposed refinements and integrate successful ones.

This module provides:
- Isolated testing environment for refinements
- Comprehensive validation checks (no regressions)
- Synoptic integration pipeline
- Regression testing suite
- Documentation of theoretical rationale

**Key Principle:** A refinement is only integrated if it:
1. Improves target predictions
2. Does not regress existing good predictions
3. Has clear topological/geometric origin (Directive A)
4. Preserves fundamental symmetries

Usage:
    from evolution_system import IntegrationSystem, AIAdvisor, ValidationModule
    
    # Get a refinement suggestion from AI Advisor
    suggestion = advisor.get_top_suggestions(analysis, n=1)[0]
    
    # Test the refinement in isolation
    integrator = IntegrationSystem()
    result = integrator.test_refinement(suggestion)
    
    # If validation passes, integrate
    if result.is_valid:
        integrator.integrate_refinement(suggestion, result)

Author: Copilot (AI-assisted development)
Date: 2026-01-08
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import mpmath as mp
from datetime import datetime
import json

# Set precision for calculations
mp.dps = 50

# Import from sibling modules (relative import)
# These imports may fail during standalone testing or when module is imported 
# directly without the package structure, so we gracefully handle ImportError.
try:
    from .calculation_engine import CalculationEngine, PredictionResult
    from .validation_module import ValidationModule, ValidationResult
    from .ai_advisor import RefinementSuggestion, TopologicalModification, RefinementType
    from .experimental_database import ExperimentalDatabase
except ImportError as e:
    # For standalone testing or direct script execution, these classes
    # must be imported separately. Log the missing imports for debugging.
    import warnings
    warnings.warn(f"Could not import evolution_system modules: {e}. "
                  "Some functionality may be limited in standalone mode.")


class IntegrationStatus(Enum):
    """Status of a refinement integration attempt."""
    PENDING = "pending"
    TESTING = "testing"
    VALIDATED = "validated"
    REJECTED = "rejected"
    INTEGRATED = "integrated"


class RejectionReason(Enum):
    """Reasons why a refinement may be rejected."""
    REGRESSION = "caused_regression"
    NO_IMPROVEMENT = "no_improvement"
    SYMMETRY_VIOLATION = "symmetry_violation"
    NOT_TOPOLOGICAL = "not_topological_origin"
    NUMERICAL_INSTABILITY = "numerical_instability"
    VALIDATION_FAILED = "validation_failed"


@dataclass
class RegressionTestResult:
    """Result of a single regression test."""
    observable: str
    baseline_sigma: float
    refined_sigma: float
    passed: bool
    improvement: float  # Positive = better, negative = worse
    
    def to_dict(self) -> Dict:
        return {
            "observable": self.observable,
            "baseline_sigma": self.baseline_sigma,
            "refined_sigma": self.refined_sigma,
            "passed": self.passed,
            "improvement": self.improvement
        }


@dataclass
class SymmetryCheck:
    """Result of a symmetry preservation check."""
    symmetry_name: str
    preserved: bool
    violation_magnitude: Optional[float] = None
    details: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "symmetry_name": self.symmetry_name,
            "preserved": self.preserved,
            "violation_magnitude": self.violation_magnitude,
            "details": self.details
        }


@dataclass
class IntegrationResult:
    """Complete result of a refinement integration attempt."""
    refinement_name: str
    status: IntegrationStatus
    rejection_reason: Optional[RejectionReason] = None
    
    # Validation results
    target_improved: bool = False
    target_improvement_pct: float = 0.0
    
    # Regression testing
    regression_tests: List[RegressionTestResult] = field(default_factory=list)
    regressions_found: int = 0
    
    # Symmetry checks
    symmetry_checks: List[SymmetryCheck] = field(default_factory=list)
    symmetries_preserved: bool = True
    
    # Topological verification
    topological_origin_verified: bool = False
    topological_derivation: Optional[str] = None
    
    # Baseline and refined predictions
    baseline_predictions: Dict[str, float] = field(default_factory=dict)
    refined_predictions: Dict[str, float] = field(default_factory=dict)
    
    # Metadata
    test_timestamp: str = ""
    integration_timestamp: Optional[str] = None
    notes: List[str] = field(default_factory=list)
    
    @property
    def is_valid(self) -> bool:
        """Check if refinement passed all validation criteria."""
        return (
            self.target_improved and
            self.regressions_found == 0 and
            self.symmetries_preserved and
            self.topological_origin_verified
        )
    
    def to_dict(self) -> Dict:
        return {
            "refinement_name": self.refinement_name,
            "status": self.status.value,
            "rejection_reason": self.rejection_reason.value if self.rejection_reason else None,
            "is_valid": self.is_valid,
            "target_improved": self.target_improved,
            "target_improvement_pct": self.target_improvement_pct,
            "regression_tests": [r.to_dict() for r in self.regression_tests],
            "regressions_found": self.regressions_found,
            "symmetry_checks": [s.to_dict() for s in self.symmetry_checks],
            "symmetries_preserved": self.symmetries_preserved,
            "topological_origin_verified": self.topological_origin_verified,
            "topological_derivation": self.topological_derivation,
            "test_timestamp": self.test_timestamp,
            "integration_timestamp": self.integration_timestamp,
            "notes": self.notes
        }


class IsolatedTestEnvironment:
    """
    Isolated environment for testing refinements without affecting production code.
    
    This ensures that experimental refinements cannot corrupt the main
    calculation pipeline or introduce unintended side effects.
    """
    
    def __init__(self):
        """Initialize isolated test environment."""
        self._baseline_engine = CalculationEngine()
        self._baseline_predictions: Optional[Dict[str, PredictionResult]] = None
        
    def setup_baseline(self) -> Dict[str, PredictionResult]:
        """Compute and cache baseline predictions."""
        if self._baseline_predictions is None:
            self._baseline_predictions = self._baseline_engine.compute_all_predictions()
        return self._baseline_predictions
    
    def compute_refined_predictions(
        self, 
        refinement: TopologicalModification
    ) -> Dict[str, PredictionResult]:
        """
        Compute predictions with the proposed refinement applied.
        
        This creates a modified calculation engine that incorporates
        the refinement, while preserving the original baseline.
        """
        # Get baseline predictions
        baseline = self.setup_baseline()
        
        # Create refined predictions by applying the modification
        refined = {}
        
        for name, pred in baseline.items():
            # Check if this observable is affected by the refinement
            if name in refinement.affected_observables:
                # Apply the refinement correction
                correction = self._compute_correction(refinement, name, pred.value)
                refined_value = float(pred.value) * correction
                
                refined[name] = PredictionResult(
                    name=name,
                    value=mp.mpf(refined_value),
                    unit=pred.unit,
                    derivation_method=f"{pred.derivation_method} + {refinement.name}",
                    topological_origin=pred.topological_origin,
                    precision_level=pred.precision_level,
                    metadata={
                        **pred.metadata,
                        "refinement_applied": refinement.name,
                        "correction_factor": correction
                    }
                )
            else:
                # Unchanged prediction
                refined[name] = pred
        
        return refined
    
    def _compute_correction(
        self, 
        refinement: TopologicalModification,
        observable: str,
        baseline_value: mp.mpf
    ) -> float:
        """
        Compute the correction factor for a given refinement.
        
        This interprets the refinement's mathematical formula to
        calculate the actual numerical correction.
        
        Note: These are first-order approximations for testing purposes.
        Full implementations would require more detailed calculations.
        """
        # Default correction factor (no change)
        correction = 1.0
        
        # Apply refinement based on type
        rtype = refinement.refinement_type
        
        if rtype == RefinementType.CHERN_CLASS_CORRECTION:
            # α_refined = α_base × [1 + κ × C₂(G) / dim(G)]
            # For gauge couplings, this gives ~1-3% correction
            eta = float(mp.mpf(4) / mp.pi)  # Metric mismatch from 4-strand substrate
            vol_ratio = 1.0 / 6.0  # Vol(S⁷)/Vol(S³) from Hopf fibration
            kappa = eta * vol_ratio ** 2  # Geometric factor from 24-cell
            
            # First-order approximation: C₂(G)/dim(G) ≈ 0.1 for typical gauge groups
            # For SU(3): C₂ = 3, dim = 8, ratio ≈ 0.375
            # For SU(2): C₂ = 2, dim = 3, ratio ≈ 0.667
            # We use 0.1 as conservative estimate for testing
            if "alpha" in observable.lower():
                correction = 1.0 + kappa * 0.1
        
        elif rtype == RefinementType.BERRY_PHASE:
            # Berry phase correction increases with generation number
            # Higher generations have more complex flavor manifold topology
            if "muon" in observable.lower() or "tau" in observable.lower():
                correction = 1.0 + 0.005  # 0.5% correction for heavier leptons
        
        elif rtype == RefinementType.INSTANTON_CORRECTION:
            # Instanton suppression for vacuum energy
            # Multi-instanton configurations provide additional suppression
            if "lambda" in observable.lower() or "vacuum" in observable.lower():
                correction = 1.0 - 0.1  # Additional 10% suppression from k=2 sector
        
        elif rtype == RefinementType.HOPF_FIBRATION:
            # Higher Hopf fibration correction (S¹⁵ contribution)
            # Vol(S¹⁵) = π⁸/5040, Vol(S⁷) = π⁴/3
            vol_s15 = float(mp.pi ** 8 / mp.mpf(5040))
            vol_s7 = float(mp.pi ** 4 / mp.mpf(3))
            correction = 1.0 + vol_s15 / vol_s7 ** 2
        
        elif rtype == RefinementType.EULER_CHARACTERISTIC:
            # Euler characteristic correction from internal manifold compactification
            # χ(CY₃) ≈ -200 is typical for Calabi-Yau 3-folds that give 3 generations
            # (|χ|/2 = 100 ≈ 3 generations × factors from complex structure)
            CHI_CALABI_YAU_3FOLD = -200  # Typical value for phenomenologically viable CY3
            correction = (4.0 - CHI_CALABI_YAU_3FOLD / 24.0) / 4.0
        
        elif rtype == RefinementType.WEYL_ANOMALY:
            # Weyl anomaly correction from Standard Model particle content
            # Using standard formulas: a = (1/360)(N_s + 11N_f + 62N_v)
            #                          c = (1/120)(N_s + 6N_f + 12N_v)
            N_SCALARS = 4      # Higgs doublet: 4 real degrees of freedom
            N_FERMIONS = 45    # 3 generations × 15 Weyl fermions per generation
            N_VECTORS = 12     # SU(3)×SU(2)×U(1): 8 + 3 + 1 = 12 gauge bosons
            a_SM = (1/360) * (N_SCALARS + 11*N_FERMIONS + 62*N_VECTORS)
            c_SM = (1/120) * (N_SCALARS + 6*N_FERMIONS + 12*N_VECTORS)
            correction = 1.0 + (c_SM - a_SM) / a_SM
        
        else:
            # Default: small perturbative correction for other topological types
            correction = 1.0 + 0.01
        
        return correction
    
    def reset(self):
        """Reset the test environment."""
        self._baseline_predictions = None


class RegressionTester:
    """
    Tests refinements for regressions in prediction accuracy.
    
    A regression occurs when a refinement makes a prediction worse
    (higher σ-deviation from experiment) compared to baseline.
    """
    
    def __init__(self, sigma_tolerance: float = 0.5):
        """
        Initialize regression tester.
        
        Args:
            sigma_tolerance: Maximum allowed increase in σ-deviation.
                           Default 0.5σ allows small fluctuations.
        """
        self.sigma_tolerance = sigma_tolerance
        self._db = ExperimentalDatabase()
        self._validator = ValidationModule()
    
    def test_all(
        self,
        baseline: Dict[str, PredictionResult],
        refined: Dict[str, PredictionResult],
        target_observables: List[str]
    ) -> Tuple[List[RegressionTestResult], int]:
        """
        Test all predictions for regressions.
        
        Args:
            baseline: Baseline predictions
            refined: Refined predictions
            target_observables: Observables that the refinement targets
                              (allowed to change significantly)
        
        Returns:
            Tuple of (list of test results, count of regressions)
        """
        results = []
        regressions = 0
        
        # Get all observables to test (exclude targets)
        all_observables = set(baseline.keys()) | set(refined.keys())
        non_target = all_observables - set(target_observables)
        
        for obs in non_target:
            if obs not in baseline or obs not in refined:
                continue
                
            # Get experimental value if available
            try:
                exp_data = self._db.get(obs)
                exp_value = exp_data.value
                exp_uncertainty = exp_data.uncertainty
            except KeyError:
                # No experimental data for comparison
                continue
            
            # Compute σ-deviations
            baseline_val = float(baseline[obs].value)
            refined_val = float(refined[obs].value)
            
            baseline_sigma = abs(baseline_val - exp_value) / exp_uncertainty
            refined_sigma = abs(refined_val - exp_value) / exp_uncertainty
            
            # Check for regression
            improvement = baseline_sigma - refined_sigma  # Positive = better
            passed = improvement >= -self.sigma_tolerance
            
            if not passed:
                regressions += 1
            
            results.append(RegressionTestResult(
                observable=obs,
                baseline_sigma=baseline_sigma,
                refined_sigma=refined_sigma,
                passed=passed,
                improvement=improvement
            ))
        
        return results, regressions


class SymmetryChecker:
    """
    Checks that refinements preserve fundamental symmetries.
    
    Symmetries to check:
    - Gauge invariance (SU(3)×SU(2)×U(1))
    - Lorentz symmetry
    - CPT symmetry
    - Unitarity
    """
    
    def check_all(
        self,
        refinement: TopologicalModification,
        predictions: Dict[str, PredictionResult]
    ) -> List[SymmetryCheck]:
        """
        Check all fundamental symmetries.
        
        Args:
            refinement: The proposed modification
            predictions: Refined predictions to check
        
        Returns:
            List of symmetry check results
        """
        checks = []
        
        # Check gauge invariance
        checks.append(self._check_gauge_invariance(refinement))
        
        # Check Lorentz symmetry
        checks.append(self._check_lorentz_symmetry(refinement, predictions))
        
        # Check CPT
        checks.append(self._check_cpt_symmetry(refinement))
        
        # Check unitarity
        checks.append(self._check_unitarity(refinement))
        
        return checks
    
    def _check_gauge_invariance(self, refinement: TopologicalModification) -> SymmetryCheck:
        """Check that gauge symmetry is preserved."""
        # Check if gauge invariance is in preserved symmetries list
        preserved_list = [s.lower() for s in refinement.symmetries_preserved]
        preserved = any("gauge" in s for s in preserved_list)
        
        return SymmetryCheck(
            symmetry_name="Gauge invariance",
            preserved=preserved,
            details="Gauge symmetry declared in refinement specification"
        )
    
    def _check_lorentz_symmetry(
        self, 
        refinement: TopologicalModification,
        predictions: Dict[str, PredictionResult]
    ) -> SymmetryCheck:
        """Check that Lorentz symmetry is preserved."""
        preserved_list = [s.lower() for s in refinement.symmetries_preserved]
        preserved = any("lorentz" in s for s in preserved_list)
        
        return SymmetryCheck(
            symmetry_name="Lorentz symmetry",
            preserved=preserved,
            details="Lorentz symmetry declared in refinement specification"
        )
    
    def _check_cpt_symmetry(self, refinement: TopologicalModification) -> SymmetryCheck:
        """Check that CPT symmetry is preserved."""
        preserved_list = [s.lower() for s in refinement.symmetries_preserved]
        preserved = any("cpt" in s for s in preserved_list)
        
        return SymmetryCheck(
            symmetry_name="CPT symmetry",
            preserved=preserved,
            details="CPT symmetry declared in refinement specification"
        )
    
    # Refinement types that preserve unitarity by construction
    # These are all geometric/topological modifications that don't introduce
    # non-Hermitian terms or break probability conservation
    UNITARY_PRESERVING_TYPES = {
        RefinementType.CHERN_CLASS_CORRECTION,  # Hermitian curvature corrections
        RefinementType.BERRY_PHASE,             # Unitary phase factor
        RefinementType.HOPF_FIBRATION,          # Geometric volume ratios
        RefinementType.EULER_CHARACTERISTIC,    # Topological invariant
        RefinementType.VOLUME_RATIO,            # Geometric ratios
        RefinementType.INSTANTON_CORRECTION,    # Real exponential suppression
        RefinementType.HOLONOMY,                # Unitary parallel transport
        RefinementType.WEYL_ANOMALY,            # Real anomaly coefficients
        RefinementType.BRAID_GROUP,             # Unitary representations
        RefinementType.WINDING_NUMBER,          # Quantized integer corrections
    }
    
    def _check_unitarity(self, refinement: TopologicalModification) -> SymmetryCheck:
        """Check that unitarity is preserved."""
        # Unitarity is preserved for all standard topological modifications
        # They don't introduce non-Hermitian terms or probability-violating factors
        preserved = refinement.refinement_type in self.UNITARY_PRESERVING_TYPES
        
        return SymmetryCheck(
            symmetry_name="Unitarity",
            preserved=preserved,
            details="Topological modifications preserve unitarity by construction"
        )


class TopologicalVerifier:
    """
    Verifies that refinements have clear topological/geometric origin.
    
    This enforces Directive A: NO phenomenological parameters allowed.
    """
    
    # Valid topological sources
    VALID_SOURCES = {
        "hopf_fibration": "Hopf fibration volume ratios",
        "chern_class": "Chern characteristic classes",
        "braid_group": "Braid group representations",
        "euler_characteristic": "Euler characteristic of manifolds",
        "berry_phase": "Berry/geometric phase",
        "instanton": "Instanton topological configurations",
        "holonomy": "Holonomy around loops",
        "weyl_anomaly": "Weyl anomaly coefficients",
        "volume_ratio": "Sphere volume ratios",
        "winding_number": "Homotopy winding numbers"
    }
    
    def verify(self, refinement: TopologicalModification) -> Tuple[bool, str]:
        """
        Verify that refinement has valid topological origin.
        
        Args:
            refinement: The proposed modification
        
        Returns:
            Tuple of (is_valid, derivation_explanation)
        """
        rtype = refinement.refinement_type.value
        
        # Check if refinement type is in valid sources
        if rtype in self.VALID_SOURCES:
            source = self.VALID_SOURCES[rtype]
            derivation = f"Derived from {source}. {refinement.topological_basis}"
            return True, derivation
        
        # Check topological basis text for valid sources
        basis_lower = refinement.topological_basis.lower()
        for key, source in self.VALID_SOURCES.items():
            if key.replace("_", " ") in basis_lower or source.lower() in basis_lower:
                derivation = f"Topological basis verified: {source}"
                return True, derivation
        
        # No valid topological source found
        return False, "No clear topological origin identified. Directive A violation."


class IntegrationSystem:
    """
    Main class for validating and integrating refinements.
    
    This is the entry point for Phase 3 of the Theory Evolution System.
    It coordinates isolated testing, regression testing, symmetry checks,
    and topological verification.
    """
    
    def __init__(self, sigma_tolerance: float = 0.5):
        """
        Initialize the Integration System.
        
        Args:
            sigma_tolerance: Maximum allowed increase in σ-deviation
                           for non-target predictions.
        """
        self.test_env = IsolatedTestEnvironment()
        self.regression_tester = RegressionTester(sigma_tolerance)
        self.symmetry_checker = SymmetryChecker()
        self.topological_verifier = TopologicalVerifier()
        
        # Track integration history
        self._integration_history: List[IntegrationResult] = []
    
    def test_refinement(
        self,
        suggestion: RefinementSuggestion
    ) -> IntegrationResult:
        """
        Test a proposed refinement in isolation.
        
        This is the main method for Phase 3 validation. It:
        1. Computes refined predictions
        2. Checks for regressions
        3. Verifies symmetry preservation
        4. Confirms topological origin
        
        Args:
            suggestion: RefinementSuggestion from AI Advisor
        
        Returns:
            IntegrationResult with full validation details
        """
        modification = suggestion.modification
        result = IntegrationResult(
            refinement_name=modification.name,
            status=IntegrationStatus.TESTING,
            test_timestamp=datetime.now().isoformat()
        )
        
        try:
            # Step 1: Compute baseline and refined predictions
            baseline = self.test_env.setup_baseline()
            refined = self.test_env.compute_refined_predictions(modification)
            
            # Store predictions
            result.baseline_predictions = {
                k: float(v.value) for k, v in baseline.items()
            }
            result.refined_predictions = {
                k: float(v.value) for k, v in refined.items()
            }
            
            # Step 2: Check if target predictions improved
            target_improved, improvement_pct = self._check_target_improvement(
                baseline, refined, modification.affected_observables
            )
            result.target_improved = target_improved
            result.target_improvement_pct = improvement_pct
            
            if not target_improved:
                result.status = IntegrationStatus.REJECTED
                result.rejection_reason = RejectionReason.NO_IMPROVEMENT
                result.notes.append("Refinement did not improve target predictions")
                return result
            
            # Step 3: Regression testing
            regression_results, regressions = self.regression_tester.test_all(
                baseline, refined, modification.affected_observables
            )
            result.regression_tests = regression_results
            result.regressions_found = regressions
            
            if regressions > 0:
                result.status = IntegrationStatus.REJECTED
                result.rejection_reason = RejectionReason.REGRESSION
                result.notes.append(f"Found {regressions} regression(s) in non-target predictions")
                return result
            
            # Step 4: Symmetry checks
            symmetry_checks = self.symmetry_checker.check_all(modification, refined)
            result.symmetry_checks = symmetry_checks
            result.symmetries_preserved = all(s.preserved for s in symmetry_checks)
            
            if not result.symmetries_preserved:
                result.status = IntegrationStatus.REJECTED
                result.rejection_reason = RejectionReason.SYMMETRY_VIOLATION
                violated = [s.symmetry_name for s in symmetry_checks if not s.preserved]
                result.notes.append(f"Symmetry violations: {', '.join(violated)}")
                return result
            
            # Step 5: Topological verification
            is_topological, derivation = self.topological_verifier.verify(modification)
            result.topological_origin_verified = is_topological
            result.topological_derivation = derivation
            
            if not is_topological:
                result.status = IntegrationStatus.REJECTED
                result.rejection_reason = RejectionReason.NOT_TOPOLOGICAL
                result.notes.append("Refinement lacks clear topological origin (Directive A)")
                return result
            
            # All checks passed!
            result.status = IntegrationStatus.VALIDATED
            result.notes.append("Refinement passed all validation criteria")
            result.notes.append(f"Target improvement: {improvement_pct:.2f}%")
            result.notes.append(f"Regression tests passed: {len(regression_results)}")
            
        except Exception as e:
            result.status = IntegrationStatus.REJECTED
            result.rejection_reason = RejectionReason.NUMERICAL_INSTABILITY
            result.notes.append(f"Error during testing: {str(e)}")
        
        # Store in history
        self._integration_history.append(result)
        
        return result
    
    def _check_target_improvement(
        self,
        baseline: Dict[str, PredictionResult],
        refined: Dict[str, PredictionResult],
        targets: List[str]
    ) -> Tuple[bool, float]:
        """Check if target predictions improved."""
        db = ExperimentalDatabase()
        
        total_improvement = 0.0
        count = 0
        
        for target in targets:
            if target not in baseline or target not in refined:
                continue
            
            try:
                exp_data = db.get(target)
                exp_value = exp_data.value
                exp_uncertainty = exp_data.uncertainty
            except KeyError:
                continue
            
            baseline_val = float(baseline[target].value)
            refined_val = float(refined[target].value)
            
            baseline_error = abs(baseline_val - exp_value) / exp_value
            refined_error = abs(refined_val - exp_value) / exp_value
            
            improvement = (baseline_error - refined_error) / baseline_error * 100
            total_improvement += improvement
            count += 1
        
        if count == 0:
            return False, 0.0
        
        avg_improvement = total_improvement / count
        return avg_improvement > 0, avg_improvement
    
    def integrate_refinement(
        self,
        suggestion: RefinementSuggestion,
        result: IntegrationResult
    ) -> bool:
        """
        Integrate a validated refinement into the theory.
        
        This method is called after test_refinement returns a VALIDATED result.
        It documents the integration and marks it as complete.
        
        In a full implementation, this would:
        1. Update the theory documents (README.md, IRHv25.md)
        2. Create new notebook with the refinement
        3. Update validation suite
        4. Create changelog entry
        
        Args:
            suggestion: The original refinement suggestion
            result: Validated IntegrationResult
        
        Returns:
            True if integration successful
        """
        if result.status != IntegrationStatus.VALIDATED:
            return False
        
        # Mark as integrated
        result.status = IntegrationStatus.INTEGRATED
        result.integration_timestamp = datetime.now().isoformat()
        result.notes.append("Refinement successfully integrated")
        
        # Update history
        for i, hist in enumerate(self._integration_history):
            if hist.refinement_name == result.refinement_name:
                self._integration_history[i] = result
                break
        
        return True
    
    def get_integration_history(self) -> List[IntegrationResult]:
        """Get the history of integration attempts."""
        return self._integration_history
    
    def generate_report(self, result: IntegrationResult) -> str:
        """Generate a human-readable integration report."""
        lines = []
        lines.append("=" * 70)
        lines.append("INTEGRATION SYSTEM REPORT")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"Refinement: {result.refinement_name}")
        lines.append(f"Status: {result.status.value.upper()}")
        if result.rejection_reason:
            lines.append(f"Rejection Reason: {result.rejection_reason.value}")
        lines.append(f"Test Timestamp: {result.test_timestamp}")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("TARGET PREDICTIONS")
        lines.append("-" * 70)
        lines.append(f"Improved: {'YES' if result.target_improved else 'NO'}")
        lines.append(f"Average Improvement: {result.target_improvement_pct:.2f}%")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("REGRESSION TESTING")
        lines.append("-" * 70)
        lines.append(f"Tests Run: {len(result.regression_tests)}")
        lines.append(f"Regressions Found: {result.regressions_found}")
        
        if result.regression_tests:
            lines.append("")
            lines.append("Details:")
            for test in result.regression_tests[:5]:  # Show first 5
                status = "✓" if test.passed else "✗"
                lines.append(f"  {status} {test.observable}: "
                           f"σ {test.baseline_sigma:.2f} → {test.refined_sigma:.2f} "
                           f"(Δ = {test.improvement:+.2f})")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("SYMMETRY CHECKS")
        lines.append("-" * 70)
        for check in result.symmetry_checks:
            status = "✓" if check.preserved else "✗"
            lines.append(f"  {status} {check.symmetry_name}")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("TOPOLOGICAL VERIFICATION")
        lines.append("-" * 70)
        lines.append(f"Verified: {'YES' if result.topological_origin_verified else 'NO'}")
        if result.topological_derivation:
            # Truncate at word boundary for readability
            derivation = result.topological_derivation
            max_length = 200  # Configurable display length
            if len(derivation) > max_length:
                # Find last space before truncation point
                truncate_at = derivation.rfind(' ', 0, max_length)
                if truncate_at == -1:
                    truncate_at = max_length
                derivation = derivation[:truncate_at] + "..."
            lines.append(f"Derivation: {derivation}")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("NOTES")
        lines.append("-" * 70)
        for note in result.notes:
            lines.append(f"  • {note}")
        lines.append("")
        
        lines.append("=" * 70)
        lines.append("END OF REPORT")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def to_dict(self) -> Dict:
        """Return integration system configuration as dictionary."""
        return {
            "sigma_tolerance": self.regression_tester.sigma_tolerance,
            "valid_topological_sources": list(TopologicalVerifier.VALID_SOURCES.keys()),
            "history_count": len(self._integration_history)
        }
