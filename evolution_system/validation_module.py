"""
Validation Module for IRH Theory Evolution System
=================================================

Compares theoretical predictions to experimental measurements.

**Features:**
- Loads experimental values from ExperimentalDatabase
- Computes relative errors: ε = |theory - exp| / exp
- Calculates σ-deviations: σ = |theory - exp| / uncertainty
- Categorizes predictions: excellent (<1σ), good (1-3σ), discrepant (>3σ)
- Generates comprehensive validation reports

**Validation Tiers:**
- Tier 1: Core parameters (α, gauge couplings, lepton masses)
- Tier 2: Derived quantities (Higgs VEV, W/Z masses, CKM)
- Tier 3: Cosmological (Λ, ΩΛ, ΩDM, Ωb)
- Tier 4: Precision tests (g-2, EDMs, CP violation)

Usage:
------
```python
from evolution_system import ValidationModule, CalculationEngine

engine = CalculationEngine()
predictions = engine.compute_all_predictions()

validator = ValidationModule()
report = validator.validate_all(predictions)

# Print summary
validator.print_validation_report(report)

# Get discrepant predictions
discrepant = report.get_discrepant(sigma_threshold=3.0)
for item in discrepant:
    print(f"{item.prediction_name}: {item.sigma_deviation:.2f}σ")
```

References:
-----------
- docs/THEORY_EVOLUTION_SYSTEM.md: Validation Module specification
- notebooks/06_validation_suite.ipynb: Validation implementation
"""

import mpmath as mp
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from enum import Enum

from .experimental_database import ExperimentalDatabase, ExperimentalConstant, ValidationTier
from .calculation_engine import PredictionResult

# Set high precision
mp.dps = 50


class AgreementStatus(Enum):
    """Agreement status between theory and experiment."""
    EXCELLENT = "excellent"  # Within 1σ
    GOOD = "good"            # Within 1-3σ
    FAIR = "fair"            # Within 3-5σ
    POOR = "poor"            # Beyond 5σ
    NO_COMPARISON = "no_comparison"  # No experimental value available


@dataclass
class ValidationResult:
    """
    Result of validating a single prediction against experiment.
    """
    prediction_name: str
    prediction_symbol: str
    
    # Values
    theory_value: mp.mpf
    exp_value: Optional[mp.mpf]
    exp_uncertainty: Optional[mp.mpf]
    
    # Comparison metrics
    absolute_error: Optional[mp.mpf] = None
    relative_error: Optional[mp.mpf] = None
    relative_error_percent: Optional[float] = None
    sigma_deviation: Optional[float] = None
    
    # Status
    agreement_status: AgreementStatus = AgreementStatus.NO_COMPARISON
    tier: Optional[ValidationTier] = None
    
    # Metadata
    experimental_source: Optional[str] = None
    theory_reference: Optional[str] = None
    requires_attention: bool = False
    notes: Optional[str] = None
    
    def __post_init__(self):
        """Ensure mpf types."""
        if not isinstance(self.theory_value, mp.mpf):
            self.theory_value = mp.mpf(str(self.theory_value))
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'prediction_name': self.prediction_name,
            'prediction_symbol': self.prediction_symbol,
            'theory_value': float(self.theory_value),
            'exp_value': float(self.exp_value) if self.exp_value else None,
            'exp_uncertainty': float(self.exp_uncertainty) if self.exp_uncertainty else None,
            'absolute_error': float(self.absolute_error) if self.absolute_error else None,
            'relative_error': float(self.relative_error) if self.relative_error else None,
            'relative_error_percent': self.relative_error_percent,
            'sigma_deviation': self.sigma_deviation,
            'agreement_status': self.agreement_status.value,
            'tier': self.tier.value if self.tier else None,
            'experimental_source': self.experimental_source,
            'theory_reference': self.theory_reference,
            'requires_attention': self.requires_attention,
            'notes': self.notes,
        }


@dataclass
class ValidationReport:
    """
    Complete validation report for all predictions.
    """
    results: Dict[str, ValidationResult] = field(default_factory=dict)
    
    # Summary statistics
    total_predictions: int = 0
    compared_predictions: int = 0
    excellent_count: int = 0
    good_count: int = 0
    fair_count: int = 0
    poor_count: int = 0
    
    # By tier
    tier_summaries: Dict[str, Dict] = field(default_factory=dict)
    
    # Overall metrics
    mean_sigma_deviation: Optional[float] = None
    max_sigma_deviation: Optional[float] = None
    worst_prediction: Optional[str] = None
    best_prediction: Optional[str] = None
    
    # Pass/fail
    tier1_pass_rate: Optional[float] = None
    overall_pass_rate: Optional[float] = None
    
    def get_excellent(self) -> List[ValidationResult]:
        """Get all excellent (<1σ) results."""
        return [r for r in self.results.values() 
                if r.agreement_status == AgreementStatus.EXCELLENT]
    
    def get_good(self) -> List[ValidationResult]:
        """Get all good (1-3σ) results."""
        return [r for r in self.results.values() 
                if r.agreement_status == AgreementStatus.GOOD]
    
    def get_fair(self) -> List[ValidationResult]:
        """Get all fair (3-5σ) results."""
        return [r for r in self.results.values() 
                if r.agreement_status == AgreementStatus.FAIR]
    
    def get_poor(self) -> List[ValidationResult]:
        """Get all poor (>5σ) results."""
        return [r for r in self.results.values() 
                if r.agreement_status == AgreementStatus.POOR]
    
    def get_discrepant(self, sigma_threshold: float = 3.0) -> List[ValidationResult]:
        """Get all results with σ > threshold."""
        return [r for r in self.results.values()
                if r.sigma_deviation is not None 
                and r.sigma_deviation > sigma_threshold]
    
    def get_tier(self, tier: Union[int, ValidationTier]) -> List[ValidationResult]:
        """Get all results in a specific tier."""
        if isinstance(tier, int):
            tier = ValidationTier(tier)
        return [r for r in self.results.values() if r.tier == tier]
    
    def get_requiring_attention(self) -> List[ValidationResult]:
        """Get all results flagged as requiring attention."""
        return [r for r in self.results.values() if r.requires_attention]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'summary': {
                'total_predictions': self.total_predictions,
                'compared_predictions': self.compared_predictions,
                'excellent_count': self.excellent_count,
                'good_count': self.good_count,
                'fair_count': self.fair_count,
                'poor_count': self.poor_count,
                'mean_sigma_deviation': self.mean_sigma_deviation,
                'max_sigma_deviation': self.max_sigma_deviation,
                'worst_prediction': self.worst_prediction,
                'best_prediction': self.best_prediction,
                'tier1_pass_rate': self.tier1_pass_rate,
                'overall_pass_rate': self.overall_pass_rate,
            },
            'tier_summaries': self.tier_summaries,
            'results': {
                key: result.to_dict()
                for key, result in self.results.items()
            },
        }


class ValidationModule:
    """
    Validation module for comparing IRH predictions to experiments.
    
    Compares theoretical predictions from the CalculationEngine to
    experimental measurements from the ExperimentalDatabase.
    
    **Validation Categories:**
    - EXCELLENT: σ < 1.0 (within 1σ of experiment)
    - GOOD: 1.0 ≤ σ < 3.0 (within 3σ)
    - FAIR: 3.0 ≤ σ < 5.0 (within 5σ)
    - POOR: σ ≥ 5.0 (significant discrepancy)
    """
    
    # Mapping from prediction keys to experimental database keys
    PREDICTION_TO_EXPERIMENT_MAP = {
        'alpha_inv': 'alpha_inv',
        'eta': None,  # No direct experimental comparison (derived quantity)
        'koide_Q': None,  # Computed from lepton masses
        'alpha_s': 'alpha_s',
        'alpha_1': 'g1',  # Need to convert
        'alpha_2': 'g2',  # Need to convert
        'sin2_theta_W': 'sin2_theta_w',
        'M_GUT': None,  # No direct measurement
        'Lambda_suppression': None,  # Not directly measurable
        'Omega_Lambda': 'Omega_Lambda',
        'Omega_DM': 'Omega_DM',
        'Omega_b': 'Omega_b',
    }
    
    def __init__(self, experimental_db: Optional[ExperimentalDatabase] = None):
        """
        Initialize validation module.
        
        Args:
            experimental_db: Database of experimental values (optional)
        """
        self.exp_db = experimental_db or ExperimentalDatabase()
    
    def validate_single(
        self,
        prediction: PredictionResult,
        exp_key: Optional[str] = None
    ) -> ValidationResult:
        """
        Validate a single prediction against experiment.
        
        Args:
            prediction: Theoretical prediction
            exp_key: Key in experimental database (auto-detected if None)
        
        Returns:
            ValidationResult with comparison metrics
        """
        theory_value = prediction.value
        
        # Try to find matching experimental value
        exp_const: Optional[ExperimentalConstant] = None
        if exp_key:
            try:
                exp_const = self.exp_db.get(exp_key)
            except KeyError:
                # Intentional: if the experimental key is not found, we leave
                # exp_const as None and fall back to "no experimental comparison"
                pass
        
        # Create base result
        result = ValidationResult(
            prediction_name=prediction.name,
            prediction_symbol=prediction.symbol,
            theory_value=theory_value,
            exp_value=None,
            exp_uncertainty=None,
            theory_reference=prediction.theory_reference,
        )
        
        if exp_const is None:
            # No experimental comparison available
            result.agreement_status = AgreementStatus.NO_COMPARISON
            result.notes = "No experimental value available for comparison"
            return result
        
        # Extract experimental values
        exp_value = exp_const.value
        exp_uncertainty = exp_const.uncertainty
        
        result.exp_value = exp_value
        result.exp_uncertainty = exp_uncertainty
        result.experimental_source = exp_const.source
        result.tier = exp_const.tier
        
        # Compute comparison metrics
        if exp_uncertainty > 0:
            result.absolute_error = abs(theory_value - exp_value)
            
            if exp_value != 0:
                result.relative_error = abs(theory_value - exp_value) / abs(exp_value)
                result.relative_error_percent = float(result.relative_error * 100)
            
            result.sigma_deviation = float(abs(theory_value - exp_value) / exp_uncertainty)
            
            # Determine agreement status
            sigma = result.sigma_deviation
            if sigma < 1.0:
                result.agreement_status = AgreementStatus.EXCELLENT
            elif sigma < 3.0:
                result.agreement_status = AgreementStatus.GOOD
            elif sigma < 5.0:
                result.agreement_status = AgreementStatus.FAIR
                result.requires_attention = True
            else:
                result.agreement_status = AgreementStatus.POOR
                result.requires_attention = True
                result.notes = f"Significant discrepancy: {sigma:.1f}σ from experiment"
        else:
            # Exact value (like c or ℏ), just check if they match
            if theory_value == exp_value:
                result.agreement_status = AgreementStatus.EXCELLENT
                result.sigma_deviation = 0.0
            else:
                result.absolute_error = abs(theory_value - exp_value)
                if exp_value != 0:
                    result.relative_error = abs(theory_value - exp_value) / abs(exp_value)
                    result.relative_error_percent = float(result.relative_error * 100)
                result.agreement_status = AgreementStatus.POOR
                result.requires_attention = True
                result.notes = "Does not match exact value"
        
        return result
    
    def validate_koide_formula(self, prediction: PredictionResult) -> ValidationResult:
        """
        Special validation for Koide formula using lepton masses.
        
        Computes Q from experimental lepton masses and compares
        to theoretical Q = 2/3.
        
        Args:
            prediction: Koide Q prediction (should be 2/3)
        
        Returns:
            ValidationResult for Koide formula
        """
        # Get experimental lepton masses
        m_e = self.exp_db.get('m_electron').value
        m_mu = self.exp_db.get('m_muon').value
        m_tau = self.exp_db.get('m_tau').value
        
        # Compute experimental Koide ratio
        # Q = (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)²
        numerator = m_e + m_mu + m_tau
        denominator = (mp.sqrt(m_e) + mp.sqrt(m_mu) + mp.sqrt(m_tau)) ** 2
        Q_exp = numerator / denominator
        
        # Uncertainty estimation (from mass uncertainties, simplified)
        # δQ/Q ~ Σ(δm_i/m_i) ~ 0.01%
        Q_uncertainty = mp.mpf('0.0001')  # Conservative estimate
        
        theory_value = prediction.value
        
        result = ValidationResult(
            prediction_name=prediction.name,
            prediction_symbol=prediction.symbol,
            theory_value=theory_value,
            exp_value=Q_exp,
            exp_uncertainty=Q_uncertainty,
            experimental_source="Derived from CODATA 2022 lepton masses",
            tier=ValidationTier.TIER_1,
            theory_reference=prediction.theory_reference,
        )
        
        # Compute comparison metrics
        result.absolute_error = abs(theory_value - Q_exp)
        result.relative_error = abs(theory_value - Q_exp) / abs(Q_exp)
        result.relative_error_percent = float(result.relative_error * 100)
        result.sigma_deviation = float(abs(theory_value - Q_exp) / Q_uncertainty)
        
        # Determine agreement status
        sigma = result.sigma_deviation
        if sigma < 1.0:
            result.agreement_status = AgreementStatus.EXCELLENT
        elif sigma < 3.0:
            result.agreement_status = AgreementStatus.GOOD
        elif sigma < 5.0:
            result.agreement_status = AgreementStatus.FAIR
            result.requires_attention = True
        else:
            result.agreement_status = AgreementStatus.POOR
            result.requires_attention = True
        
        return result
    
    def validate_all(
        self,
        predictions: Dict[str, PredictionResult]
    ) -> ValidationReport:
        """
        Validate all predictions against experimental values.
        
        Args:
            predictions: Dictionary of predictions from CalculationEngine
        
        Returns:
            ValidationReport with all comparison results
        """
        report = ValidationReport()
        report.total_predictions = len(predictions)
        
        sigma_deviations = []
        
        for key, prediction in predictions.items():
            # Special handling for Koide formula
            if key == 'koide_Q':
                result = self.validate_koide_formula(prediction)
            else:
                # Look up experimental key
                exp_key = self.PREDICTION_TO_EXPERIMENT_MAP.get(key)
                result = self.validate_single(prediction, exp_key)
            
            report.results[key] = result
            
            # Update counts
            if result.agreement_status != AgreementStatus.NO_COMPARISON:
                report.compared_predictions += 1
                
                if result.sigma_deviation is not None:
                    sigma_deviations.append((key, result.sigma_deviation))
                
                if result.agreement_status == AgreementStatus.EXCELLENT:
                    report.excellent_count += 1
                elif result.agreement_status == AgreementStatus.GOOD:
                    report.good_count += 1
                elif result.agreement_status == AgreementStatus.FAIR:
                    report.fair_count += 1
                else:
                    report.poor_count += 1
        
        # Compute summary statistics
        if sigma_deviations:
            sigmas = [s for _, s in sigma_deviations]
            report.mean_sigma_deviation = sum(sigmas) / len(sigmas)
            
            # Find worst and best
            sorted_by_sigma = sorted(sigma_deviations, key=lambda x: x[1])
            report.best_prediction = sorted_by_sigma[0][0]
            report.worst_prediction = sorted_by_sigma[-1][0]
            report.max_sigma_deviation = sorted_by_sigma[-1][1]
        
        # Tier 1 pass rate (within 3σ)
        tier1_results = [r for r in report.results.values() 
                        if r.tier == ValidationTier.TIER_1 
                        and r.agreement_status != AgreementStatus.NO_COMPARISON]
        if tier1_results:
            tier1_passes = sum(1 for r in tier1_results 
                              if r.sigma_deviation is not None and r.sigma_deviation < 3.0)
            report.tier1_pass_rate = tier1_passes / len(tier1_results)
        
        # Overall pass rate
        if report.compared_predictions > 0:
            passes = report.excellent_count + report.good_count
            report.overall_pass_rate = passes / report.compared_predictions
        
        # Tier summaries
        for tier in ValidationTier:
            tier_results = report.get_tier(tier)
            if tier_results:
                tier_compared = [r for r in tier_results 
                               if r.agreement_status != AgreementStatus.NO_COMPARISON]
                if tier_compared:
                    tier_pass = sum(1 for r in tier_compared 
                                   if r.sigma_deviation and r.sigma_deviation < 3.0)
                    report.tier_summaries[tier.name] = {
                        'total': len(tier_results),
                        'compared': len(tier_compared),
                        'passing': tier_pass,
                        'pass_rate': tier_pass / len(tier_compared) if tier_compared else 0,
                    }
        
        return report
    
    def print_validation_report(self, report: ValidationReport):
        """
        Print a human-readable validation report.
        
        Args:
            report: ValidationReport from validate_all()
        """
        print("=" * 80)
        print("IRH THEORY VALIDATION REPORT")
        print("=" * 80)
        print()
        
        # Summary
        print("SUMMARY")
        print("-" * 80)
        print(f"Total predictions:    {report.total_predictions}")
        print(f"Compared to exp:      {report.compared_predictions}")
        print()
        
        print("Agreement Status:")
        print(f"  ✓ EXCELLENT (<1σ):  {report.excellent_count}")
        print(f"  ○ GOOD (1-3σ):      {report.good_count}")
        print(f"  △ FAIR (3-5σ):      {report.fair_count}")
        print(f"  ✗ POOR (>5σ):       {report.poor_count}")
        print()
        
        if report.mean_sigma_deviation is not None:
            print(f"Mean σ deviation:     {report.mean_sigma_deviation:.3f}")
            print(f"Max σ deviation:      {report.max_sigma_deviation:.3f} ({report.worst_prediction})")
            print(f"Best prediction:      {report.best_prediction}")
        print()
        
        if report.tier1_pass_rate is not None:
            print(f"Tier 1 pass rate:     {report.tier1_pass_rate*100:.1f}%")
        if report.overall_pass_rate is not None:
            print(f"Overall pass rate:    {report.overall_pass_rate*100:.1f}%")
        print()
        
        # Detailed results by tier
        print("DETAILED RESULTS BY TIER")
        print("-" * 80)
        
        for tier in ValidationTier:
            tier_results = report.get_tier(tier)
            if not tier_results:
                continue
            
            print(f"\n{tier.name}:")
            print("-" * 40)
            
            for result in tier_results:
                status_symbol = {
                    AgreementStatus.EXCELLENT: "✓",
                    AgreementStatus.GOOD: "○",
                    AgreementStatus.FAIR: "△",
                    AgreementStatus.POOR: "✗",
                    AgreementStatus.NO_COMPARISON: "-",
                }[result.agreement_status]
                
                if result.sigma_deviation is not None:
                    sigma_str = f"{result.sigma_deviation:.2f}σ"
                else:
                    sigma_str = "N/A"
                
                print(f"  {status_symbol} {result.prediction_symbol:15} "
                      f"Theory: {float(result.theory_value):12.6g}  "
                      f"Exp: {float(result.exp_value) if result.exp_value else 'N/A':>12}  "
                      f"σ: {sigma_str:>8}")
        
        # Predictions requiring attention
        attention = report.get_requiring_attention()
        if attention:
            print()
            print("PREDICTIONS REQUIRING ATTENTION")
            print("-" * 80)
            for result in attention:
                print(f"  ⚠ {result.prediction_name}")
                if result.notes:
                    print(f"    {result.notes}")
                if result.sigma_deviation:
                    print(f"    σ-deviation: {result.sigma_deviation:.2f}")
        
        print()
        print("=" * 80)
        print("⚠️  Experimental values used FOR VALIDATION ONLY - Per Directive A")
        print("=" * 80)


# Convenience function
def validate_predictions(
    predictions: Dict[str, PredictionResult],
    print_report: bool = True
) -> ValidationReport:
    """
    Convenience function to validate predictions.
    
    Args:
        predictions: Predictions from CalculationEngine
        print_report: Whether to print the report
    
    Returns:
        ValidationReport
    """
    validator = ValidationModule()
    report = validator.validate_all(predictions)
    
    if print_report:
        validator.print_validation_report(report)
    
    return report


if __name__ == '__main__':
    # Demo usage
    from .calculation_engine import CalculationEngine
    
    # Compute predictions
    engine = CalculationEngine()
    predictions = engine.compute_all_predictions()
    
    # Validate
    report = validate_predictions(predictions, print_report=True)
    
    # Export to JSON
    import json
    
    output = report.to_dict()
    with open('validation_report.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\nReport exported to validation_report.json")
