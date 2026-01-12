"""
Error Analyzer for IRH Theory Evolution System
==============================================

Identifies systematic patterns in prediction errors.

**Features:**
- Statistical analysis of error distributions
- Pattern recognition across related observables
- Correlation analysis (e.g., do all quark masses have same sign error?)
- Dimensional analysis of discrepancies
- Topology-based error categorization

**Analysis Types:**
1. Systematic offset patterns (all predictions too high/low)
2. Scale-dependent errors (predictions improve at high energy)
3. Symmetry-related errors (unitarity violations, etc.)
4. Sector-specific patterns (leptons vs quarks vs gauge)

Usage:
------
```python
from evolution_system import ErrorAnalyzer, ValidationReport

# After validation
analyzer = ErrorAnalyzer()
patterns = analyzer.analyze(validation_report)

# Print analysis
analyzer.print_analysis(patterns)

# Get suggestions for refinements
suggestions = analyzer.suggest_refinements(patterns)
for s in suggestions:
    print(f"Suggestion: {s.description}")
    print(f"  Basis: {s.mathematical_basis}")
```

References:
-----------
- docs/THEORY_EVOLUTION_SYSTEM.md: Error Analyzer specification
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from collections import defaultdict

from .validation_module import ValidationReport, ValidationResult, AgreementStatus


class PatternType(Enum):
    """Types of systematic error patterns."""
    SYSTEMATIC_OFFSET = "systematic_offset"      # All predictions too high/low
    SCALE_DEPENDENT = "scale_dependent"          # Error varies with energy scale
    SYMMETRY_RELATED = "symmetry_related"        # Related to symmetry violations
    SECTOR_SPECIFIC = "sector_specific"          # Specific to a physics sector
    TOPOLOGICAL_CORRECTION = "topological_correction"  # Needs higher-order topology
    RADIATIVE_CORRECTION = "radiative_correction"      # Needs better QFT corrections
    UNKNOWN = "unknown"                          # Pattern not yet identified


class Severity(Enum):
    """Severity of the error pattern."""
    CRITICAL = "critical"    # σ > 5, must be addressed
    HIGH = "high"            # 3 < σ ≤ 5, should be addressed
    MEDIUM = "medium"        # 1 < σ ≤ 3, nice to address
    LOW = "low"              # σ ≤ 1, acceptable


@dataclass
class ErrorPattern:
    """
    A systematic error pattern identified in the predictions.
    """
    pattern_type: PatternType
    severity: Severity
    description: str
    
    # Affected predictions
    affected_predictions: List[str]
    affected_count: int
    
    # Pattern details
    mean_error_sign: Optional[float] = None  # Positive = predictions too high
    mean_sigma_deviation: Optional[float] = None
    correlation_coefficient: Optional[float] = None
    
    # Analysis results
    possible_causes: List[str] = field(default_factory=list)
    suggested_fix: Optional[str] = None
    mathematical_basis: Optional[str] = None
    
    # Impact assessment
    impact_on_theory: Optional[str] = None
    confidence: float = 0.0  # 0-1 confidence in the pattern
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'pattern_type': self.pattern_type.value,
            'severity': self.severity.value,
            'description': self.description,
            'affected_predictions': self.affected_predictions,
            'affected_count': self.affected_count,
            'mean_error_sign': self.mean_error_sign,
            'mean_sigma_deviation': self.mean_sigma_deviation,
            'correlation_coefficient': self.correlation_coefficient,
            'possible_causes': self.possible_causes,
            'suggested_fix': self.suggested_fix,
            'mathematical_basis': self.mathematical_basis,
            'impact_on_theory': self.impact_on_theory,
            'confidence': self.confidence,
        }


@dataclass 
class RefinementSuggestion:
    """
    A suggested theoretical refinement based on error patterns.
    
    **Key Principle:** Suggestions must be topologically motivated.
    NO phenomenological fitting or parameter tuning is allowed.
    """
    title: str
    description: str
    
    # Pattern that motivates this suggestion
    source_pattern: ErrorPattern
    
    # Mathematical details
    mathematical_basis: str
    
    # Expected impact
    expected_improvement: str
    
    # Optional fields with defaults
    formula_modification: Optional[str] = None
    predictions_affected: List[str] = field(default_factory=list)
    
    # Constraints (Directive A compliance)
    is_topologically_motivated: bool = True
    topological_origin: Optional[str] = None
    
    # Implementation notes
    implementation_difficulty: str = "medium"  # easy, medium, hard
    requires_new_derivation: bool = False
    reference_papers: List[str] = field(default_factory=list)
    
    # Priority
    priority: int = 1  # 1 = highest priority
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'title': self.title,
            'description': self.description,
            'source_pattern': self.source_pattern.to_dict(),
            'mathematical_basis': self.mathematical_basis,
            'formula_modification': self.formula_modification,
            'expected_improvement': self.expected_improvement,
            'predictions_affected': self.predictions_affected,
            'is_topologically_motivated': self.is_topologically_motivated,
            'topological_origin': self.topological_origin,
            'implementation_difficulty': self.implementation_difficulty,
            'requires_new_derivation': self.requires_new_derivation,
            'reference_papers': self.reference_papers,
            'priority': self.priority,
        }


@dataclass
class ErrorAnalysis:
    """
    Complete error analysis results.
    """
    patterns: List[ErrorPattern] = field(default_factory=list)
    suggestions: List[RefinementSuggestion] = field(default_factory=list)
    
    # Summary statistics
    total_errors_analyzed: int = 0
    critical_patterns: int = 0
    high_patterns: int = 0
    medium_patterns: int = 0
    low_patterns: int = 0
    
    # Overall assessment
    overall_status: str = "unknown"
    primary_concern: Optional[str] = None
    action_required: bool = False
    
    def get_critical(self) -> List[ErrorPattern]:
        """Get critical severity patterns."""
        return [p for p in self.patterns if p.severity == Severity.CRITICAL]
    
    def get_high_priority_suggestions(self, n: int = 5) -> List[RefinementSuggestion]:
        """Get top N highest priority suggestions."""
        sorted_suggestions = sorted(self.suggestions, key=lambda s: s.priority)
        return sorted_suggestions[:n]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'summary': {
                'total_errors_analyzed': self.total_errors_analyzed,
                'critical_patterns': self.critical_patterns,
                'high_patterns': self.high_patterns,
                'medium_patterns': self.medium_patterns,
                'low_patterns': self.low_patterns,
                'overall_status': self.overall_status,
                'primary_concern': self.primary_concern,
                'action_required': self.action_required,
            },
            'patterns': [p.to_dict() for p in self.patterns],
            'suggestions': [s.to_dict() for s in self.suggestions],
        }


class ErrorAnalyzer:
    """
    Error analyzer for IRH validation results.
    
    Identifies systematic patterns in prediction errors and suggests
    topologically-motivated refinements.
    
    **Directive A Compliance:** All suggestions must be derivable from
    topological/geometric principles. NO phenomenological fixes.
    """
    
    def __init__(self):
        """Initialize error analyzer."""
        self._analysis: Optional[ErrorAnalysis] = None
    
    def analyze(self, report: ValidationReport) -> ErrorAnalysis:
        """
        Analyze validation report for systematic error patterns.
        
        Args:
            report: ValidationReport from ValidationModule
        
        Returns:
            ErrorAnalysis with patterns and suggestions
        """
        analysis = ErrorAnalysis()
        analysis.total_errors_analyzed = report.compared_predictions
        
        # Extract results that have comparisons
        comparable_results = [
            (key, result) for key, result in report.results.items()
            if result.agreement_status != AgreementStatus.NO_COMPARISON
            and result.sigma_deviation is not None
        ]
        
        if not comparable_results:
            analysis.overall_status = "no_data"
            return analysis
        
        # Run pattern detection algorithms
        patterns = []
        
        # 1. Check for systematic offset
        offset_pattern = self._detect_systematic_offset(comparable_results)
        if offset_pattern:
            patterns.append(offset_pattern)
        
        # 2. Check for sector-specific patterns
        sector_patterns = self._detect_sector_patterns(comparable_results, report)
        patterns.extend(sector_patterns)
        
        # 3. Check for scale-dependent patterns
        scale_pattern = self._detect_scale_dependence(comparable_results)
        if scale_pattern:
            patterns.append(scale_pattern)
        
        # 4. Check for individual outliers
        outlier_patterns = self._detect_outliers(comparable_results)
        patterns.extend(outlier_patterns)
        
        # Count by severity
        for pattern in patterns:
            if pattern.severity == Severity.CRITICAL:
                analysis.critical_patterns += 1
            elif pattern.severity == Severity.HIGH:
                analysis.high_patterns += 1
            elif pattern.severity == Severity.MEDIUM:
                analysis.medium_patterns += 1
            else:
                analysis.low_patterns += 1
        
        analysis.patterns = patterns
        
        # Generate suggestions
        analysis.suggestions = self._generate_suggestions(patterns)
        
        # Overall assessment
        if analysis.critical_patterns > 0:
            analysis.overall_status = "critical_issues"
            analysis.action_required = True
            analysis.primary_concern = analysis.get_critical()[0].description
        elif analysis.high_patterns > 0:
            analysis.overall_status = "issues_present"
            analysis.action_required = True
        elif analysis.medium_patterns > 0:
            analysis.overall_status = "minor_issues"
            analysis.action_required = False
        else:
            analysis.overall_status = "good"
            analysis.action_required = False
        
        self._analysis = analysis
        return analysis
    
    def _detect_systematic_offset(
        self,
        results: List[Tuple[str, ValidationResult]]
    ) -> Optional[ErrorPattern]:
        """
        Detect if predictions are systematically too high or too low.
        
        Args:
            results: List of (key, ValidationResult) pairs
        
        Returns:
            ErrorPattern if systematic offset detected, else None
        """
        if len(results) < 3:
            return None
        
        # Compute signed errors
        signed_errors = []
        for key, result in results:
            if result.exp_value and result.exp_value != 0:
                signed_error = float(result.theory_value - result.exp_value) / float(result.exp_value)
                signed_errors.append((key, signed_error, result.sigma_deviation))
        
        if len(signed_errors) < 3:
            return None
        
        # Check if most errors have same sign
        positive_count = sum(1 for _, e, _ in signed_errors if e > 0)
        total = len(signed_errors)
        
        same_sign_fraction = max(positive_count, total - positive_count) / total
        
        # Need at least 75% same sign to call it systematic
        if same_sign_fraction < 0.75:
            return None
        
        # Compute mean signed error
        mean_error = sum(e for _, e, _ in signed_errors) / total
        mean_sigma = sum(s for _, _, s in signed_errors) / total
        
        # Determine severity
        if mean_sigma > 5:
            severity = Severity.CRITICAL
        elif mean_sigma > 3:
            severity = Severity.HIGH
        elif mean_sigma > 1:
            severity = Severity.MEDIUM
        else:
            severity = Severity.LOW
        
        direction = "high" if mean_error > 0 else "low"
        
        return ErrorPattern(
            pattern_type=PatternType.SYSTEMATIC_OFFSET,
            severity=severity,
            description=f"Systematic offset: predictions are {direction} by {abs(mean_error)*100:.1f}%",
            affected_predictions=[key for key, _, _ in signed_errors],
            affected_count=len(signed_errors),
            mean_error_sign=mean_error,
            mean_sigma_deviation=mean_sigma,
            possible_causes=[
                "Missing geometric correction term",
                "Incorrect normalization factor",
                "Missing radiative correction",
            ],
            suggested_fix=f"Add {'positive' if mean_error < 0 else 'negative'} correction "
                         f"of ~{abs(mean_error)*100:.1f}%",
            confidence=same_sign_fraction,
        )
    
    def _detect_sector_patterns(
        self,
        results: List[Tuple[str, ValidationResult]],
        report: ValidationReport
    ) -> List[ErrorPattern]:
        """
        Detect patterns specific to physics sectors.
        
        Args:
            results: List of (key, ValidationResult) pairs
            report: Full validation report
        
        Returns:
            List of sector-specific ErrorPatterns
        """
        patterns = []
        
        # Group by category based on key prefixes
        sectors = {
            'gauge': ['alpha_s', 'alpha_1', 'alpha_2', 'sin2_theta_W', 'M_GUT'],
            'cosmology': ['Omega_Lambda', 'Omega_DM', 'Omega_b', 'Lambda_suppression'],
            'fundamental': ['alpha_inv', 'eta', 'koide_Q'],
        }
        
        for sector_name, sector_keys in sectors.items():
            sector_results = [
                (key, result) for key, result in results
                if key in sector_keys
            ]
            
            if len(sector_results) < 2:
                continue
            
            # Compute sector statistics
            sigma_values = [result.sigma_deviation for _, result in sector_results]
            mean_sigma = sum(sigma_values) / len(sigma_values)
            
            # Check if sector has issues
            if mean_sigma > 3:
                severity = Severity.HIGH
            elif mean_sigma > 1:
                severity = Severity.MEDIUM
            else:
                continue  # Sector is fine
            
            patterns.append(ErrorPattern(
                pattern_type=PatternType.SECTOR_SPECIFIC,
                severity=severity,
                description=f"{sector_name.capitalize()} sector has elevated errors "
                           f"(mean σ = {mean_sigma:.1f})",
                affected_predictions=[key for key, _ in sector_results],
                affected_count=len(sector_results),
                mean_sigma_deviation=mean_sigma,
                possible_causes=[
                    f"Missing {sector_name}-specific correction",
                    f"Incomplete derivation in {sector_name} sector",
                ],
                confidence=0.7,
            ))
        
        return patterns
    
    def _detect_scale_dependence(
        self,
        results: List[Tuple[str, ValidationResult]]
    ) -> Optional[ErrorPattern]:
        """
        Detect if errors depend on energy scale.
        
        Args:
            results: List of (key, ValidationResult) pairs
        
        Returns:
            ErrorPattern if scale dependence detected
        """
        # Define energy scales for different predictions
        scale_mapping = {
            'alpha_inv': 0,      # Low energy (electron mass scale)
            'alpha_s': 91.2,    # Z mass scale
            'alpha_1': 91.2,
            'alpha_2': 91.2,
            'sin2_theta_W': 91.2,
            'M_GUT': 2e16,      # GUT scale
        }
        
        # Get results with known scales
        scaled_results = [
            (key, result, scale_mapping[key])
            for key, result in results
            if key in scale_mapping
        ]
        
        if len(scaled_results) < 3:
            return None
        
        # Sort by scale
        scaled_results.sort(key=lambda x: x[2])
        
        # Check for trend
        low_scale_sigma = [r.sigma_deviation for _, r, s in scaled_results if s < 100]
        high_scale_sigma = [r.sigma_deviation for _, r, s in scaled_results if s >= 100]
        
        if not low_scale_sigma or not high_scale_sigma:
            return None
        
        mean_low = sum(low_scale_sigma) / len(low_scale_sigma)
        mean_high = sum(high_scale_sigma) / len(high_scale_sigma)
        
        # Check if there's a significant difference
        if abs(mean_low - mean_high) < 1.0:
            return None
        
        if mean_high < mean_low:
            trend = "improving"
            possible_cause = "Missing low-energy corrections (e.g., hadronic effects)"
        else:
            trend = "worsening"
            possible_cause = "Missing high-energy corrections (e.g., threshold effects)"
        
        severity = Severity.MEDIUM if abs(mean_low - mean_high) < 2 else Severity.HIGH
        
        return ErrorPattern(
            pattern_type=PatternType.SCALE_DEPENDENT,
            severity=severity,
            description=f"Error {trend} at high energy scales "
                       f"(low: {mean_low:.1f}σ, high: {mean_high:.1f}σ)",
            affected_predictions=[key for key, _, _ in scaled_results],
            affected_count=len(scaled_results),
            mean_sigma_deviation=(mean_low + mean_high) / 2,
            possible_causes=[
                possible_cause,
                "RG running approximations",
                "Threshold corrections at mass scales",
            ],
            mathematical_basis="Renormalization group flow",
            confidence=0.6,
        )
    
    def _detect_outliers(
        self,
        results: List[Tuple[str, ValidationResult]]
    ) -> List[ErrorPattern]:
        """
        Detect individual outliers with high σ deviations.
        
        Args:
            results: List of (key, ValidationResult) pairs
        
        Returns:
            List of outlier patterns
        """
        patterns = []
        
        for key, result in results:
            if result.sigma_deviation is None:
                continue
            
            sigma = result.sigma_deviation
            
            if sigma < 3:
                continue  # Not an outlier
            
            if sigma >= 5:
                severity = Severity.CRITICAL
            else:
                severity = Severity.HIGH
            
            pattern = ErrorPattern(
                pattern_type=PatternType.UNKNOWN,
                severity=severity,
                description=f"Outlier: {result.prediction_name} has {sigma:.1f}σ deviation",
                affected_predictions=[key],
                affected_count=1,
                mean_sigma_deviation=sigma,
                possible_causes=[
                    "Missing correction specific to this observable",
                    "Approximation breakdown for this quantity",
                    "Potential error in derivation",
                ],
                confidence=0.9,  # High confidence - it's definitely discrepant
            )
            
            patterns.append(pattern)
        
        return patterns
    
    def _generate_suggestions(
        self,
        patterns: List[ErrorPattern]
    ) -> List[RefinementSuggestion]:
        """
        Generate refinement suggestions based on error patterns.
        
        **Directive A Compliance:** All suggestions must have topological origin.
        
        Args:
            patterns: List of detected error patterns
        
        Returns:
            List of RefinementSuggestions
        """
        suggestions = []
        priority = 1
        
        for pattern in patterns:
            if pattern.pattern_type == PatternType.SYSTEMATIC_OFFSET:
                # Suggest correction factor from topology
                sign = "positive" if pattern.mean_error_sign and pattern.mean_error_sign < 0 else "negative"
                magnitude = abs(pattern.mean_error_sign or 0) * 100
                
                suggestion = RefinementSuggestion(
                    title="Higher Chern Class Correction",
                    description=f"Add {sign} correction of ~{magnitude:.1f}% from "
                               f"second Chern class C₂(G)",
                    source_pattern=pattern,
                    mathematical_basis=(
                        "Current theory uses first Chern class C₁(G). "
                        "Including C₂ adds curvature-squared terms:\n"
                        "α_refined = α_base × [1 + η₂ × C₂(G) / C₁(G)]"
                    ),
                    formula_modification="α → α × [1 + η₂ × C₂/C₁]",
                    expected_improvement=f"Should reduce mean error by ~{magnitude:.1f}%",
                    predictions_affected=pattern.affected_predictions,
                    is_topologically_motivated=True,
                    topological_origin="Second Chern class of gauge bundle",
                    implementation_difficulty="medium",
                    requires_new_derivation=True,
                    priority=priority,
                )
                suggestions.append(suggestion)
                priority += 1
            
            elif pattern.pattern_type == PatternType.SCALE_DEPENDENT:
                suggestion = RefinementSuggestion(
                    title="Threshold Corrections at Mass Scales",
                    description="Include threshold corrections for heavy particle decoupling",
                    source_pattern=pattern,
                    mathematical_basis=(
                        "When energy crosses a particle threshold, coupling evolution changes. "
                        "RG equations should include step functions:\n"
                        "β_i(μ) = β_i^(nf)(μ) × θ(μ - m_f)"
                    ),
                    formula_modification="Add threshold corrections at m_t, m_Z, m_H",
                    expected_improvement="Should reduce scale-dependent errors",
                    predictions_affected=pattern.affected_predictions,
                    is_topologically_motivated=True,
                    topological_origin="Particle spectrum from braid group representations",
                    implementation_difficulty="hard",
                    requires_new_derivation=True,
                    priority=priority,
                )
                suggestions.append(suggestion)
                priority += 1
            
            elif pattern.pattern_type == PatternType.SECTOR_SPECIFIC:
                sector = pattern.description.split()[0].lower()
                
                if "gauge" in sector:
                    suggestion = RefinementSuggestion(
                        title="Refined GUT-Scale Matching",
                        description="Improve GUT unification conditions from 24-cell geometry",
                        source_pattern=pattern,
                        mathematical_basis=(
                            "GUT matching conditions include threshold corrections:\n"
                            "α_i⁻¹(M_GUT) = α_GUT⁻¹ + Δ_i(threshold)"
                        ),
                        expected_improvement="Better gauge coupling predictions",
                        predictions_affected=pattern.affected_predictions,
                        is_topologically_motivated=True,
                        topological_origin="24-cell symmetry structure",
                        implementation_difficulty="hard",
                        priority=priority,
                    )
                    suggestions.append(suggestion)
                    priority += 1
                
                elif "cosmology" in sector or "cosmological" in sector:
                    suggestion = RefinementSuggestion(
                        title="Multi-Instanton Contributions",
                        description="Include higher-order instantonic suppression terms",
                        source_pattern=pattern,
                        mathematical_basis=(
                            "Current theory includes only leading instanton term.\n"
                            "Add: Λ_refined = Λ_base × [1 - ε₂ × e^(-S_inst/2)]"
                        ),
                        expected_improvement="Better cosmological constant prediction",
                        predictions_affected=pattern.affected_predictions,
                        is_topologically_motivated=True,
                        topological_origin="Instanton moduli space on S³ × S¹",
                        implementation_difficulty="medium",
                        priority=priority,
                    )
                    suggestions.append(suggestion)
                    priority += 1
            
            elif pattern.severity in [Severity.CRITICAL, Severity.HIGH]:
                # Generic suggestion for outliers
                suggestion = RefinementSuggestion(
                    title=f"Review {pattern.affected_predictions[0]} Derivation",
                    description=f"Significant discrepancy ({pattern.mean_sigma_deviation:.1f}σ) "
                               f"requires derivation review",
                    source_pattern=pattern,
                    mathematical_basis="Check for missing terms or calculation errors",
                    expected_improvement="Reduce σ-deviation",
                    predictions_affected=pattern.affected_predictions,
                    is_topologically_motivated=True,
                    implementation_difficulty="unknown",
                    requires_new_derivation=True,
                    priority=priority,
                )
                suggestions.append(suggestion)
                priority += 1
        
        return suggestions
    
    def suggest_refinements(
        self,
        patterns: Optional[List[ErrorPattern]] = None
    ) -> List[RefinementSuggestion]:
        """
        Generate refinement suggestions.
        
        Args:
            patterns: Error patterns (uses last analysis if None)
        
        Returns:
            List of suggestions
        """
        if patterns is None:
            if self._analysis is None:
                raise ValueError("No analysis available. Run analyze() first.")
            patterns = self._analysis.patterns
        
        return self._generate_suggestions(patterns)
    
    def print_analysis(self, analysis: Optional[ErrorAnalysis] = None):
        """
        Print human-readable error analysis.
        
        Args:
            analysis: ErrorAnalysis (uses last if None)
        """
        if analysis is None:
            if self._analysis is None:
                raise ValueError("No analysis available. Run analyze() first.")
            analysis = self._analysis
        
        print("=" * 80)
        print("IRH ERROR PATTERN ANALYSIS")
        print("=" * 80)
        print()
        
        # Summary
        print("SUMMARY")
        print("-" * 80)
        print(f"Predictions analyzed:     {analysis.total_errors_analyzed}")
        print(f"Patterns detected:        {len(analysis.patterns)}")
        print(f"  - Critical:             {analysis.critical_patterns}")
        print(f"  - High:                 {analysis.high_patterns}")
        print(f"  - Medium:               {analysis.medium_patterns}")
        print(f"  - Low:                  {analysis.low_patterns}")
        print(f"Overall status:           {analysis.overall_status}")
        print(f"Action required:          {'Yes' if analysis.action_required else 'No'}")
        
        if analysis.primary_concern:
            print(f"Primary concern:          {analysis.primary_concern}")
        print()
        
        # Patterns
        if analysis.patterns:
            print("DETECTED PATTERNS")
            print("-" * 80)
            
            for i, pattern in enumerate(analysis.patterns, 1):
                severity_symbol = {
                    Severity.CRITICAL: "🔴",
                    Severity.HIGH: "🟠",
                    Severity.MEDIUM: "🟡",
                    Severity.LOW: "🟢",
                }[pattern.severity]
                
                print(f"\n{i}. {severity_symbol} {pattern.description}")
                print(f"   Type: {pattern.pattern_type.value}")
                print(f"   Affected: {', '.join(pattern.affected_predictions)}")
                print(f"   Confidence: {pattern.confidence*100:.0f}%")
                
                if pattern.possible_causes:
                    print(f"   Possible causes:")
                    for cause in pattern.possible_causes[:3]:
                        print(f"     - {cause}")
        print()
        
        # Suggestions
        if analysis.suggestions:
            print("REFINEMENT SUGGESTIONS")
            print("-" * 80)
            
            for i, suggestion in enumerate(analysis.suggestions[:5], 1):
                print(f"\n{i}. {suggestion.title} (Priority {suggestion.priority})")
                print(f"   {suggestion.description}")
                print(f"   Difficulty: {suggestion.implementation_difficulty}")
                print(f"   Topological origin: {suggestion.topological_origin or 'N/A'}")
                
                if suggestion.mathematical_basis:
                    # Show first line of basis
                    basis_first_line = suggestion.mathematical_basis.split('\n')[0]
                    print(f"   Basis: {basis_first_line}")
        
        print()
        print("=" * 80)


if __name__ == '__main__':
    # Demo usage
    from .calculation_engine import CalculationEngine
    from .validation_module import ValidationModule
    
    # Compute and validate
    engine = CalculationEngine()
    predictions = engine.compute_all_predictions()
    
    validator = ValidationModule()
    report = validator.validate_all(predictions)
    
    # Analyze errors
    analyzer = ErrorAnalyzer()
    analysis = analyzer.analyze(report)
    
    # Print analysis
    analyzer.print_analysis(analysis)
    
    # Export to JSON
    import json
    
    output = analysis.to_dict()
    with open('error_analysis.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\nAnalysis exported to error_analysis.json")
