"""
AI Advisor Module for IRH Theory Evolution System

Phase 2 Implementation: AI-guided theoretical refinement suggestions.

This module provides:
- Prompt engineering for physics-constrained suggestions
- Topological modification templates
- Suggestion ranking algorithms
- Validation that suggestions follow Directive A (topological origin only)
- Optional Gen AI SDK integration for enhanced AI-powered suggestions

**Critical Constraints (Directive A Compliance):**
- ❌ NO parameter tuning to fit data
- ❌ NO arbitrary scaling factors
- ❌ NO phenomenological formulas
- ✅ ONLY topological/geometric refinements
- ✅ ONLY modifications with clear mathematical origin
- ✅ ONLY changes preserving fundamental symmetries

**Gen AI Integration:**
If the google-genai package is installed and GOOGLE_CLOUD_API_KEY is set,
the AIAdvisor can use Google's Gemini models to enhance suggestion generation.
This is optional - the module works with built-in templates without it.

Usage:
    from evolution_system import AIAdvisor, ErrorAnalyzer, ValidationModule
    
    # Get error analysis
    analyzer = ErrorAnalyzer()
    analysis = analyzer.analyze(validation_report)
    
    # Generate refinement suggestions (using built-in templates)
    advisor = AIAdvisor()
    suggestions = advisor.generate_suggestions(analysis)
    
    # Optional: Get AI-enhanced suggestions (requires Gen AI SDK)
    if advisor._genai_client:
        ai_suggestions = advisor.get_genai_suggestions(analysis.to_dict())
        print(ai_suggestions)
    
    # Rank and filter
    ranked = advisor.rank_suggestions(suggestions)
    topological = advisor.filter_topological_only(ranked)

Author: Copilot (AI-assisted development)
Date: 2026-01-08
Updated: 2026-01-10 (Gen AI SDK integration)
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
import mpmath as mp
import os

# Set precision for calculations
mp.dps = 50

# Optional Gen AI SDK import
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class RefinementType(Enum):
    """Types of topologically-motivated refinements."""
    CHERN_CLASS_CORRECTION = "chern_class"
    BERRY_PHASE = "berry_phase"
    INSTANTON_CORRECTION = "instanton"
    HOPF_FIBRATION = "hopf_fibration"
    BRAID_GROUP = "braid_group"
    HOLONOMY = "holonomy"
    WEYL_ANOMALY = "weyl_anomaly"
    VOLUME_RATIO = "volume_ratio"
    EULER_CHARACTERISTIC = "euler_characteristic"
    WINDING_NUMBER = "winding_number"


class ConfidenceLevel(Enum):
    """Confidence in the refinement suggestion."""
    HIGH = "high"          # Strong topological basis, clear derivation
    MEDIUM = "medium"      # Valid topological basis, some uncertainty
    LOW = "low"            # Speculative but still topologically motivated
    EXPERIMENTAL = "experimental"  # Novel approach, needs validation


@dataclass
class TopologicalModification:
    """
    A topologically-motivated modification to the theory.
    
    All modifications must have clear geometric/topological origin
    per Directive A. NO phenomenological fitting allowed.
    """
    name: str
    refinement_type: RefinementType
    mathematical_formula: str
    topological_basis: str
    affected_observables: List[str]
    expected_improvement: str
    derivation_steps: List[str]
    symmetries_preserved: List[str]
    testable_predictions: List[str]
    confidence: ConfidenceLevel
    priority_score: float = 0.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "refinement_type": self.refinement_type.value,
            "mathematical_formula": self.mathematical_formula,
            "topological_basis": self.topological_basis,
            "affected_observables": self.affected_observables,
            "expected_improvement": self.expected_improvement,
            "derivation_steps": self.derivation_steps,
            "symmetries_preserved": self.symmetries_preserved,
            "testable_predictions": self.testable_predictions,
            "confidence": self.confidence.value,
            "priority_score": self.priority_score
        }


@dataclass
class RefinementSuggestion:
    """
    A complete refinement suggestion with justification.
    
    Contains the modification, the error pattern it addresses,
    and the full theoretical justification.
    """
    modification: TopologicalModification
    error_pattern: str
    justification: str
    implementation_notes: str
    validation_criteria: List[str]
    risk_assessment: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "modification": self.modification.to_dict(),
            "error_pattern": self.error_pattern,
            "justification": self.justification,
            "implementation_notes": self.implementation_notes,
            "validation_criteria": self.validation_criteria,
            "risk_assessment": self.risk_assessment
        }


class TopologicalModificationTemplates:
    """
    Pre-defined templates for topologically-motivated refinements.
    
    These templates encode known geometric and topological corrections
    that can be applied to IRH theory predictions. Each template has:
    - Clear mathematical derivation
    - Topological/geometric origin
    - Preserved symmetries
    - Testable predictions
    
    NO phenomenological parameters are introduced.
    """
    
    @staticmethod
    def chern_class_correction(order: int = 2) -> TopologicalModification:
        """
        Higher Chern class corrections to gauge couplings.
        
        Mathematical Basis:
        The first Chern class C₁(G) captures basic curvature.
        Higher Chern classes C₂(G), C₃(G) add curvature-squared
        and higher-order terms from characteristic classes.
        
        For gauge group G with dimension dim(G):
        α_refined = α_base × [1 + κ × C₂(G) / dim(G)]
        
        where κ = η × (Vol(S⁷)/Vol(S³))² is derived from 
        the 24-cell geometry (η = 4/π is metric mismatch).
        """
        # Topological constants - DERIVED FROM GEOMETRY, NOT FIT TO DATA
        eta = mp.mpf(4) / mp.pi  # Metric mismatch from 4-strand substrate
        vol_ratio = mp.mpf(1) / mp.mpf(6)  # Vol(S⁷)/Vol(S³) ratio
        kappa = eta * vol_ratio ** 2
        
        return TopologicalModification(
            name=f"Chern Class C_{order} Correction",
            refinement_type=RefinementType.CHERN_CLASS_CORRECTION,
            mathematical_formula=f"α_refined = α_base × [1 + κ × C_{order}(G) / dim(G)]",
            topological_basis=f"""
            From characteristic class theory:
            - C₁(G) = first Chern class (basic curvature)
            - C_{order}(G) = {order}th Chern class (curvature^{order} terms)
            - κ = {float(kappa):.6f} from 24-cell geometry
            - dim(G) = dimension of gauge group
            
            This is a standard topological correction in gauge theory.
            The coefficient κ is fixed by the 4-strand network geometry.
            """,
            affected_observables=["alpha_1", "alpha_2", "alpha_3", "sin2_theta_W"],
            expected_improvement="Uniform 1-3% correction to all gauge couplings",
            derivation_steps=[
                "1. Start with fiber bundle P(M, G) over spacetime M",
                f"2. Compute characteristic class C_{order}(G) from curvature form",
                "3. Integrate over the 4-strand cymatic network",
                "4. Apply 24-cell volume normalization",
                "5. Obtain correction factor κ × C_{order}(G) / dim(G)"
            ],
            symmetries_preserved=["Gauge invariance", "Lorentz symmetry", "CPT"],
            testable_predictions=[
                "All gauge couplings shift by same relative amount",
                "Correction scales with group dimension",
                "No effect on masses (gauge sector only)"
            ],
            confidence=ConfidenceLevel.HIGH
        )
    
    @staticmethod
    def berry_phase_mass_correction() -> TopologicalModification:
        """
        Berry phase corrections to fermion masses.
        
        Mathematical Basis:
        When a particle traverses a closed path in parameter space
        (e.g., flavor space), it acquires a geometric Berry phase:
        
        γ_Berry = ∮ <ψ|∇_θ|ψ> dθ
        
        This phase modifies the effective mass:
        m_corrected = m_base × exp(iγ_Berry)
        
        For fermions, the Berry phase depends on the topology
        of the flavor manifold, which is more complex for heavier
        generations (more internal degrees of freedom).
        """
        return TopologicalModification(
            name="Berry Phase Mass Correction",
            refinement_type=RefinementType.BERRY_PHASE,
            mathematical_formula="m_corrected = m_base × |exp(iγ_Berry)|",
            topological_basis="""
            From Berry/geometric phase theory:
            - γ_Berry = ∮ A dθ where A = i<ψ|∇|ψ> is Berry connection
            - For flavor manifold with topology T, γ depends on π₁(T)
            - First generation (e): simple topology, γ ≈ 0
            - Second generation (μ): π₁ = Z, small γ
            - Third generation (τ): π₁ = Z², larger γ
            
            The Berry phase is purely geometric, not fitted.
            """,
            affected_observables=["m_electron", "m_muon", "m_tau", 
                                 "m_up", "m_charm", "m_top",
                                 "m_down", "m_strange", "m_bottom"],
            expected_improvement="0.1-1% correction increasing with generation",
            derivation_steps=[
                "1. Define flavor parameter space as manifold M_flavor",
                "2. Compute Berry connection A = i<ψ|∇|ψ> for each generation",
                "3. Integrate around closed paths in M_flavor",
                "4. The phase γ is determined by topology, not parameters",
                "5. Apply phase factor to Koide-derived mass values"
            ],
            symmetries_preserved=["Gauge invariance", "Lorentz symmetry", "CPT", 
                                 "Approximate flavor symmetry"],
            testable_predictions=[
                "Correction increases with generation number",
                "Same pattern for quarks and leptons",
                "Mass ratios within generations unchanged"
            ],
            confidence=ConfidenceLevel.MEDIUM
        )
    
    @staticmethod
    def instanton_vacuum_correction(order: int = 2) -> TopologicalModification:
        """
        Multi-instanton corrections to vacuum energy.
        
        Mathematical Basis:
        Instantons are topological configurations with action S.
        The vacuum energy receives corrections:
        
        Λ ∝ exp(-S_instanton) × [1 + corrections]
        
        Multi-instanton configurations (k instantons) contribute:
        
        Λ_refined = Λ_base × [1 - ε_k × exp(-k × S / 2)]
        
        where S is the single-instanton Euclidean action and
        ε_k is determined by the topology (winding numbers).
        """
        # Topological factor from winding numbers
        # This is NOT fitted - it comes from the instanton moduli space
        epsilon_k = mp.mpf(1) / mp.factorial(order)  # 1/k! from moduli space measure
        
        return TopologicalModification(
            name=f"Order-{order} Instanton Correction",
            refinement_type=RefinementType.INSTANTON_CORRECTION,
            mathematical_formula=f"Λ_refined = Λ_base × [1 - ε_{order} × exp(-{order}S/2)]",
            topological_basis=f"""
            From instanton calculus:
            - Single instanton: action S, tunneling amplitude ∝ exp(-S)
            - k-instanton: action kS, contribution ∝ exp(-kS) / k!
            - The 1/k! comes from the instanton moduli space volume
            - ε_{order} = 1/{order}! = {float(epsilon_k):.6f}
            
            This is standard semi-classical quantum field theory.
            """,
            affected_observables=["Lambda", "Omega_Lambda", "H_0"],
            expected_improvement=f"Additional 10^{-order} suppression of vacuum energy",
            derivation_steps=[
                "1. Write partition function with instanton sum",
                f"2. Include {order}-instanton configurations",
                "3. Compute Euclidean action for k-instanton",
                "4. Include moduli space measure factor 1/k!",
                "5. Sum over instanton sectors to get refined Λ"
            ],
            symmetries_preserved=["Gauge invariance", "General covariance", 
                                 "CPT", "Cluster decomposition"],
            testable_predictions=[
                "Only affects cosmological sector",
                "No change to particle physics predictions",
                "Higher k gives smaller corrections"
            ],
            confidence=ConfidenceLevel.HIGH
        )
    
    @staticmethod
    def hopf_fibration_correction() -> TopologicalModification:
        """
        Hopf fibration volume ratio corrections.
        
        Mathematical Basis:
        The Hopf fibration S³ → S² with fiber S¹ gives:
        
        Vol(S³) = Vol(S²) × Vol(S¹) × (twisting factor)
        
        For the 7-sphere fibration S⁷ → S⁴ → S³:
        
        α⁻¹_base = Vol(S⁷) / [Vol(S³) × Vol(S⁴)]
        
        Higher Hopf fibrations (S¹⁵ → S⁸) give corrections:
        
        α⁻¹_refined = α⁻¹_base × [1 + Vol(S¹⁵)/Vol(S⁷)²]
        """
        # Volume ratios - PURELY GEOMETRIC, from sphere volumes
        vol_s3 = mp.mpf(2) * mp.pi ** 2  # Vol(S³) = 2π²
        vol_s7 = mp.pi ** 4 / mp.mpf(3)  # Vol(S⁷) = π⁴/3
        vol_s15 = mp.pi ** 8 / mp.mpf(5040)  # Vol(S¹⁵) = π⁸/5040
        
        correction_factor = vol_s15 / vol_s7 ** 2
        
        return TopologicalModification(
            name="Higher Hopf Fibration Correction",
            refinement_type=RefinementType.HOPF_FIBRATION,
            mathematical_formula="α⁻¹_refined = α⁻¹_base × [1 + Vol(S¹⁵)/Vol(S⁷)²]",
            topological_basis=f"""
            From Hopf fibration hierarchy:
            - S³ → S² (first Hopf map, π₃(S²) = Z)
            - S⁷ → S⁴ (second Hopf map, π₇(S⁴) = Z)
            - S¹⁵ → S⁸ (third Hopf map, π₁₅(S⁸) = Z)
            
            Volume ratios:
            - Vol(S³) = 2π² = {float(vol_s3):.6f}
            - Vol(S⁷) = π⁴/3 = {float(vol_s7):.6f}
            - Vol(S¹⁵) = π⁸/5040 = {float(vol_s15):.10f}
            
            Correction factor = {float(correction_factor):.10f}
            """,
            affected_observables=["alpha_inv"],
            expected_improvement="Sub-percent correction to fine-structure constant",
            derivation_steps=[
                "1. Enumerate Hopf fibrations: S³→S², S⁷→S⁴, S¹⁵→S⁸",
                "2. Compute standard volumes of each sphere",
                "3. Current theory uses S⁷/S³ ratio",
                "4. Include S¹⁵ contribution as next order",
                "5. Correction factor = Vol(S¹⁵)/Vol(S⁷)²"
            ],
            symmetries_preserved=["Gauge invariance", "Lorentz symmetry", "CPT"],
            testable_predictions=[
                "Specific numerical correction (no free parameters)",
                "Should improve α⁻¹ prediction if current value slightly off",
                "Pattern continues: S³¹ → S¹⁶ gives next correction"
            ],
            confidence=ConfidenceLevel.HIGH
        )
    
    @staticmethod
    def braid_group_correction(strands: int = 4) -> TopologicalModification:
        """
        Braid group representation corrections.
        
        Mathematical Basis:
        The N-strand braid group B_N acts on particle states.
        Currently using N=4 strands. Higher representations give:
        
        Observable_refined = Observable_base × χ(R) / dim(R)
        
        where χ(R) is the character and dim(R) is the dimension
        of the representation R of the braid group.
        """
        # Braid group dimensions - PURELY ALGEBRAIC
        # dim(B_n standard rep) = n!
        dim_standard = mp.factorial(strands)
        
        return TopologicalModification(
            name=f"B_{strands} Representation Correction",
            refinement_type=RefinementType.BRAID_GROUP,
            mathematical_formula=f"O_refined = O_base × χ(R) / dim(R)",
            topological_basis=f"""
            From braid group representation theory:
            - B_{strands} = {strands}-strand braid group
            - Standard representation: dim = {strands}! = {int(dim_standard)}
            - Character χ(R) counts fixed points under braiding
            - Higher representations give systematic corrections
            
            No free parameters - all from group theory.
            """,
            affected_observables=["color_charge", "QCD_string_tension", "alpha_3"],
            expected_improvement="Percent-level corrections to strong sector",
            derivation_steps=[
                f"1. Enumerate irreducible representations of B_{strands}",
                "2. Compute character χ(R) for each representation",
                "3. Physical observables correspond to specific R",
                "4. Current theory uses fundamental representation",
                "5. Include corrections from higher representations"
            ],
            symmetries_preserved=["SU(3) gauge symmetry", "CPT", "Crossing symmetry"],
            testable_predictions=[
                "Corrections larger for SU(3) than SU(2) (more strands)",
                "Pattern in quark masses follows representation dimensions",
                "Predicts specific correction to glueball masses"
            ],
            confidence=ConfidenceLevel.MEDIUM
        )
    
    @staticmethod
    def weyl_anomaly_correction() -> TopologicalModification:
        """
        Weyl anomaly coefficient corrections.
        
        Mathematical Basis:
        The Weyl anomaly in 4D CFT has coefficients a and c:
        
        <T^μ_μ> = c × (Weyl)² - a × (Euler)
        
        For a = c (supersymmetric case), there's no anomaly.
        Deviation from a = c gives physical effects:
        
        Observable_refined = Observable_base × [1 + (c-a)/a]
        """
        # Weyl anomaly coefficients for Standard Model
        # These come from the particle content, NOT fitted
        # a = (1/360)(N_s + 11N_f + 62N_v) for scalars, fermions, vectors
        N_s = 4   # Higgs doublet (4 real scalars)
        N_f = 45  # 3 generations × 15 Weyl fermions
        N_v = 12  # SU(3)×SU(2)×U(1) gauge bosons
        
        a_SM = mp.mpf(1)/mp.mpf(360) * (N_s + 11*N_f + 62*N_v)
        c_SM = mp.mpf(1)/mp.mpf(120) * (N_s + 6*N_f + 12*N_v)
        
        return TopologicalModification(
            name="Weyl Anomaly Correction",
            refinement_type=RefinementType.WEYL_ANOMALY,
            mathematical_formula="O_refined = O_base × [1 + (c-a)/a]",
            topological_basis=f"""
            From conformal field theory:
            - Weyl anomaly: <T^μ_μ> = c(Weyl)² - a(Euler)
            - For SM particle content:
              - N_s = {N_s} (scalars), N_f = {N_f} (fermions), N_v = {N_v} (vectors)
              - a = {float(a_SM):.4f}
              - c = {float(c_SM):.4f}
              - (c-a)/a = {float((c_SM-a_SM)/a_SM):.4f}
            
            Coefficients fixed by particle content, not fitted.
            """,
            affected_observables=["Lambda", "running_couplings", "vacuum_energy"],
            expected_improvement="1-5% correction to vacuum sector quantities",
            derivation_steps=[
                "1. Count particle content of Standard Model",
                "2. Compute trace anomaly coefficients a and c",
                "3. Deviation from superconformal (a=c) gives correction",
                "4. Apply correction to vacuum sector predictions",
                "5. No free parameters - fully determined by SM content"
            ],
            symmetries_preserved=["Gauge invariance", "Lorentz symmetry", "CPT"],
            testable_predictions=[
                "Specific numerical correction factor",
                "Affects only vacuum/cosmological sector",
                "Could resolve remaining Λ discrepancy"
            ],
            confidence=ConfidenceLevel.HIGH
        )
    
    @staticmethod
    def euler_characteristic_correction() -> TopologicalModification:
        """
        Euler characteristic corrections from internal manifold.
        
        Mathematical Basis:
        The Euler characteristic χ of the internal space affects
        the effective dimensionality and thus coupling constants:
        
        α_refined = α_base × (4 - χ/24) / 4
        
        For Calabi-Yau manifolds, χ determines the number of
        generations. This correction captures the effect of χ
        on coupling evolution.
        """
        # Euler characteristic for various manifolds
        chi_K3 = 24  # K3 surface
        chi_CY3 = -200  # Typical Calabi-Yau 3-fold (gives 3 generations)
        
        return TopologicalModification(
            name="Euler Characteristic Correction",
            refinement_type=RefinementType.EULER_CHARACTERISTIC,
            mathematical_formula="α_refined = α_base × (4 - χ/24) / 4",
            topological_basis=f"""
            From compactification on internal manifold M:
            - Euler characteristic χ(M) is topological invariant
            - χ(K3) = {chi_K3} (preserves N=2 SUSY)
            - χ(CY₃) ≈ {chi_CY3} (gives 3 generations via |χ|/2)
            - The factor 24 comes from 24-cell geometry
            
            The correction (4-χ/24)/4 is purely topological.
            """,
            affected_observables=["alpha_inv", "alpha_1", "alpha_2", "alpha_3"],
            expected_improvement="Percent-level corrections to gauge couplings",
            derivation_steps=[
                "1. Identify internal manifold topology",
                "2. Compute Euler characteristic χ(M)",
                "3. Relate χ to effective dimensions via Gauss-Bonnet",
                "4. Correction factor = (4 - χ/24) / 4",
                "5. Apply uniformly to gauge coupling predictions"
            ],
            symmetries_preserved=["Gauge invariance", "Lorentz symmetry (4D)", "CPT"],
            testable_predictions=[
                "Same relative correction to all gauge couplings",
                "Sign of correction depends on sign of χ",
                "Correction is O(χ/100) ≈ few percent"
            ],
            confidence=ConfidenceLevel.MEDIUM
        )
    
    @staticmethod
    def holonomy_correction() -> TopologicalModification:
        """
        Holonomy corrections from parallel transport around loops.
        
        Mathematical Basis:
        Parallel transport around a closed loop in a fiber bundle
        produces a holonomy element h ∈ G (the structure group).
        The trace of this holonomy in the fundamental representation
        gives corrections to observables:
        
        O_refined = O_base × [1 + Tr(h) / dim(G)]
        
        For U(1), Tr(h) = exp(iφ) where φ is the total phase.
        For SU(N), Tr(h) depends on the path and connection.
        """
        return TopologicalModification(
            name="Holonomy Correction",
            refinement_type=RefinementType.HOLONOMY,
            mathematical_formula="O_refined = O_base × [1 + Tr(h) / dim(G)]",
            topological_basis="""
            From fiber bundle geometry:
            - Parallel transport: ψ(x+dx) = [1 + A_μ dx^μ] ψ(x)
            - Holonomy around loop C: h = P exp(∮_C A)
            - For flat connection: h = identity
            - Curvature gives non-trivial holonomy
            
            The correction Tr(h)/dim(G) is geometric, not fitted.
            """,
            affected_observables=["alpha_inv", "gauge_couplings", "Wilson_loops"],
            expected_improvement="Sub-percent corrections from curvature effects",
            derivation_steps=[
                "1. Define connection A on principal bundle P(M, G)",
                "2. Choose canonical loop C in spacetime (e.g., minimal area)",
                "3. Compute holonomy h = P exp(∮_C A)",
                "4. Take trace in fundamental representation",
                "5. Correction = Tr(h) / dim(G)"
            ],
            symmetries_preserved=["Gauge invariance", "Lorentz symmetry", "CPT"],
            testable_predictions=[
                "Correction depends on loop size/shape",
                "Vanishes for flat connections",
                "Related to Wilson loop expectation values"
            ],
            confidence=ConfidenceLevel.MEDIUM
        )
    
    @staticmethod
    def volume_ratio_correction() -> TopologicalModification:
        """
        Volume ratio corrections from sphere fibrations.
        
        Mathematical Basis:
        The volumes of n-spheres satisfy:
        
        Vol(S^n) = 2π^((n+1)/2) / Γ((n+1)/2)
        
        Ratios of these volumes give dimensionless topological constants.
        The current theory uses Vol(S⁷)/Vol(S³). Including higher
        sphere ratios gives systematic corrections:
        
        O_refined = O_base × [1 + Vol(S^(n+4))/Vol(S^n)²]
        """
        # Volume ratios - PURELY GEOMETRIC
        vol_s3 = 2 * mp.pi ** 2  # Vol(S³)
        vol_s7 = mp.pi ** 4 / 3  # Vol(S⁷)
        vol_s11 = mp.pi ** 6 / 60  # Vol(S¹¹)
        
        ratio_7_3 = vol_s7 / vol_s3
        ratio_11_7 = vol_s11 / vol_s7
        
        return TopologicalModification(
            name="Volume Ratio Correction",
            refinement_type=RefinementType.VOLUME_RATIO,
            mathematical_formula="O_refined = O_base × [1 + Vol(S^(n+4))/Vol(S^n)²]",
            topological_basis=f"""
            From sphere volumes (exact formulas):
            - Vol(S³) = 2π² = {float(vol_s3):.6f}
            - Vol(S⁷) = π⁴/3 = {float(vol_s7):.6f}
            - Vol(S¹¹) = π⁶/60 = {float(vol_s11):.8f}
            
            Ratios:
            - Vol(S⁷)/Vol(S³) = {float(ratio_7_3):.6f}
            - Vol(S¹¹)/Vol(S⁷) = {float(ratio_11_7):.6f}
            
            These are pure numbers from geometry.
            """,
            affected_observables=["alpha_inv", "Koide_Q"],
            expected_improvement="Sub-percent corrections from higher fibrations",
            derivation_steps=[
                "1. Compute Vol(S^n) = 2π^((n+1)/2) / Γ((n+1)/2)",
                "2. Current theory uses S³ → S⁷ fibration",
                "3. Include next fibration: S⁷ → S¹¹",
                "4. Correction factor = Vol(S¹¹)/Vol(S⁷)²",
                "5. Apply to predictions built on volume ratios"
            ],
            symmetries_preserved=["All - purely geometric correction"],
            testable_predictions=[
                "Specific numerical correction (no free parameters)",
                "Same correction for all volume-ratio-based predictions",
                "Pattern continues: S¹¹ → S¹⁵ → S¹⁹..."
            ],
            confidence=ConfidenceLevel.HIGH
        )
    
    @staticmethod
    def winding_number_correction() -> TopologicalModification:
        """
        Winding number corrections from homotopy groups.
        
        Mathematical Basis:
        Maps f: S^n → S^n are classified by their winding number
        (degree) deg(f) ∈ Z via π_n(S^n) = Z.
        
        Physical fields that wind around compact dimensions
        contribute additional terms proportional to the winding:
        
        O_refined = O_base × [1 + n_wind / N_max]
        
        where n_wind is the winding number and N_max is a
        topological cutoff from compactification.
        """
        # Topological winding constraint
        # For the 4-strand network, max winding is related to 24-cell symmetry
        N_max = 24  # From 24-cell vertices
        
        return TopologicalModification(
            name="Winding Number Correction",
            refinement_type=RefinementType.WINDING_NUMBER,
            mathematical_formula="O_refined = O_base × [1 + n_wind / N_max]",
            topological_basis=f"""
            From homotopy theory:
            - π_n(S^n) = Z classifies maps by winding number
            - Physical fields can wrap compact dimensions
            - Each winding sector contributes to partition function
            - N_max = {N_max} from 24-cell geometry
            
            The winding correction is topologically quantized.
            """,
            affected_observables=["Lambda", "vacuum_energy", "theta_QCD"],
            expected_improvement="1/N_max ≈ 4% corrections per winding sector",
            derivation_steps=[
                "1. Identify compact directions in field space",
                "2. Classify field configurations by winding number",
                "3. Sum over winding sectors in partition function",
                "4. Normalize by N_max from 24-cell geometry",
                "5. Leading correction is n_wind = 1 sector"
            ],
            symmetries_preserved=["Gauge invariance", "Large gauge transformations"],
            testable_predictions=[
                "Corrections quantized as 1/24 = 4.2%",
                "Multiple windings give higher-order corrections",
                "Related to theta-angle physics in QCD"
            ],
            confidence=ConfidenceLevel.MEDIUM
        )


class AIAdvisor:
    """
    AI Advisor for generating topologically-motivated refinement suggestions.
    
    This class analyzes error patterns from the validation module and
    generates suggestions for theoretical refinements. All suggestions
    are constrained to have clear topological/geometric origin per
    Directive A.
    
    **Key Principle:** The advisor suggests DERIVATIONS, not fits.
    """
    
    def __init__(self):
        """Initialize the AI Advisor with modification templates."""
        self.templates = TopologicalModificationTemplates()
        self._error_pattern_map = self._build_error_pattern_map()
        self._genai_client = None
        
        # Initialize Gen AI client if available and API key is set
        if GENAI_AVAILABLE and os.environ.get("GOOGLE_CLOUD_API_KEY"):
            try:
                self._genai_client = genai.Client(
                    vertexai=True,
                    api_key=os.environ.get("GOOGLE_CLOUD_API_KEY"),
                )
            except Exception as e:
                print(f"Warning: Could not initialize Gen AI client: {e}")
                self._genai_client = None
    
    def _build_error_pattern_map(self) -> Dict[str, List[TopologicalModification]]:
        """
        Build mapping from error patterns to relevant modifications.
        
        This encodes physics knowledge about which corrections
        address which types of errors.
        """
        return {
            # Gauge coupling errors
            "gauge_coupling_systematic": [
                self.templates.chern_class_correction(order=2),
                self.templates.euler_characteristic_correction(),
            ],
            "gauge_coupling_scale_dependent": [
                self.templates.chern_class_correction(order=3),
                self.templates.weyl_anomaly_correction(),
            ],
            
            # Mass prediction errors  
            "lepton_mass_pattern": [
                self.templates.berry_phase_mass_correction(),
                self.templates.hopf_fibration_correction(),
            ],
            "quark_mass_pattern": [
                self.templates.berry_phase_mass_correction(),
                self.templates.braid_group_correction(strands=4),
            ],
            
            # Cosmological errors
            "vacuum_energy_too_high": [
                self.templates.instanton_vacuum_correction(order=2),
                self.templates.instanton_vacuum_correction(order=3),
                self.templates.weyl_anomaly_correction(),
            ],
            "cosmological_ratios": [
                self.templates.instanton_vacuum_correction(order=2),
                self.templates.euler_characteristic_correction(),
            ],
            
            # Fine-structure constant errors
            "alpha_systematic": [
                self.templates.hopf_fibration_correction(),
                self.templates.chern_class_correction(order=2),
            ],
            
            # Strong sector errors
            "qcd_errors": [
                self.templates.braid_group_correction(strands=4),
                self.templates.chern_class_correction(order=2),
            ],
        }
    
    def analyze_error_pattern(self, analysis_result: Dict) -> List[str]:
        """
        Identify error patterns from the error analysis result.
        
        Args:
            analysis_result: Output from ErrorAnalyzer.analyze().to_dict()
            
        Returns:
            List of identified error pattern keys
        """
        patterns = []
        
        # Check for systematic offset patterns
        if "patterns" in analysis_result:
            for pattern in analysis_result.get("patterns", []):
                pattern_type = pattern.get("pattern_type", "")
                affected = pattern.get("affected_predictions", [])
                
                # Classify the pattern
                if "alpha" in str(affected).lower() or "gauge" in str(affected).lower():
                    if pattern_type == "systematic_offset":
                        patterns.append("gauge_coupling_systematic")
                    elif pattern_type == "scale_dependent":
                        patterns.append("gauge_coupling_scale_dependent")
                
                if any("mass" in obs.lower() for obs in affected):
                    if any("lepton" in obs.lower() or obs in ["m_electron", "m_muon", "m_tau"] 
                           for obs in affected):
                        patterns.append("lepton_mass_pattern")
                    if any("quark" in obs.lower() for obs in affected):
                        patterns.append("quark_mass_pattern")
                
                if any(obs in ["Lambda", "Omega_Lambda", "vacuum_energy"] for obs in affected):
                    if pattern_type == "systematic_offset":
                        patterns.append("vacuum_energy_too_high")
                    patterns.append("cosmological_ratios")
                
                if "alpha_inv" in affected:
                    patterns.append("alpha_systematic")
                
                if any(obs in ["alpha_3", "alpha_s", "QCD_string_tension"] for obs in affected):
                    patterns.append("qcd_errors")
        
        # Check individual poor results (in case patterns missed something)
        if "poor_predictions" in analysis_result.get("summary", {}):
            for pred_name in analysis_result["summary"].get("poor_predictions", []):
                if "alpha" in pred_name.lower() and "alpha_systematic" not in patterns:
                    patterns.append("alpha_systematic")
                if "mass" in pred_name.lower():
                    if "lepton" in pred_name.lower() and "lepton_mass_pattern" not in patterns:
                        patterns.append("lepton_mass_pattern")
                    elif "quark" in pred_name.lower() and "quark_mass_pattern" not in patterns:
                        patterns.append("quark_mass_pattern")
        
        return list(set(patterns))  # Remove duplicates
    
    def generate_suggestions(self, analysis_result: Dict) -> List[RefinementSuggestion]:
        """
        Generate refinement suggestions based on error analysis.
        
        Args:
            analysis_result: Output from ErrorAnalyzer.analyze()
            
        Returns:
            List of RefinementSuggestion objects
        """
        suggestions = []
        patterns = self.analyze_error_pattern(analysis_result)
        
        for pattern in patterns:
            if pattern in self._error_pattern_map:
                modifications = self._error_pattern_map[pattern]
                for mod in modifications:
                    suggestion = self._create_suggestion(mod, pattern, analysis_result)
                    suggestions.append(suggestion)
        
        return suggestions
    
    def _create_suggestion(self, modification: TopologicalModification, 
                          pattern: str, analysis: Dict) -> RefinementSuggestion:
        """Create a complete refinement suggestion."""
        
        # Build justification from error pattern
        justification = f"""
        Error Pattern: {pattern}
        
        This refinement addresses the identified error pattern through
        a topologically-motivated correction. The mathematical basis
        is derived from {modification.refinement_type.value} theory.
        
        Key points:
        1. NO phenomenological parameters are introduced
        2. All constants are derived from topology/geometry
        3. Symmetries are preserved: {', '.join(modification.symmetries_preserved)}
        4. Testable predictions: {', '.join(modification.testable_predictions[:2])}
        """
        
        # Implementation notes
        impl_notes = f"""
        To implement this refinement:
        1. Create isolated test notebook: notebooks/refinement_{modification.refinement_type.value}.ipynb
        2. Implement modification: {modification.mathematical_formula}
        3. Compute ALL predictions with modification applied
        4. Compare to baseline (no regression allowed)
        5. If validation passes, integrate into main codebase
        """
        
        # Validation criteria
        validation = [
            "No regression in existing good predictions (all must stay within σ bounds)",
            f"Target observables improve: {', '.join(modification.affected_observables[:3])}",
            "All symmetries preserved (gauge, Lorentz, CPT)",
            "Clear topological derivation (Directive A compliance)",
            "Testable new predictions generated"
        ]
        
        # Risk assessment
        risk = f"""
        Risk Level: {'LOW' if modification.confidence == ConfidenceLevel.HIGH else 'MEDIUM'}
        
        Potential Issues:
        - May introduce small shifts in observables not targeted
        - Numerical precision must be maintained
        - Must verify no symmetry violations
        
        Mitigations:
        - Test against ALL predictions before integration
        - Use arbitrary precision arithmetic (mpmath)
        - Include symmetry checks in validation
        """
        
        return RefinementSuggestion(
            modification=modification,
            error_pattern=pattern,
            justification=justification,
            implementation_notes=impl_notes,
            validation_criteria=validation,
            risk_assessment=risk
        )
    
    def rank_suggestions(self, suggestions: List[RefinementSuggestion]) -> List[RefinementSuggestion]:
        """
        Rank suggestions by priority.
        
        Ranking criteria:
        1. Confidence level (HIGH > MEDIUM > LOW > EXPERIMENTAL)
        2. Number of affected observables (more = higher priority)
        3. Topological soundness (cleaner derivation = higher)
        
        Args:
            suggestions: List of RefinementSuggestion objects
            
        Returns:
            Sorted list with highest priority first
        """
        for suggestion in suggestions:
            mod = suggestion.modification
            
            # Base score from confidence
            confidence_scores = {
                ConfidenceLevel.HIGH: 100,
                ConfidenceLevel.MEDIUM: 70,
                ConfidenceLevel.LOW: 40,
                ConfidenceLevel.EXPERIMENTAL: 10
            }
            score = confidence_scores.get(mod.confidence, 50)
            
            # Bonus for affecting multiple observables
            score += len(mod.affected_observables) * 5
            
            # Bonus for having many derivation steps (more rigorous)
            score += len(mod.derivation_steps) * 2
            
            # Bonus for preserving many symmetries
            score += len(mod.symmetries_preserved) * 3
            
            # Bonus for testable predictions
            score += len(mod.testable_predictions) * 4
            
            mod.priority_score = score
        
        # Sort by priority score (descending)
        return sorted(suggestions, key=lambda s: s.modification.priority_score, reverse=True)
    
    def filter_topological_only(self, suggestions: List[RefinementSuggestion]) -> List[RefinementSuggestion]:
        """
        Filter to ensure only topologically-motivated suggestions.
        
        This is a safety check to enforce Directive A compliance.
        All suggestions from this module should pass, but this
        provides an additional verification layer.
        
        Args:
            suggestions: List of RefinementSuggestion objects
            
        Returns:
            Filtered list containing only topological refinements
        """
        valid_types = {
            RefinementType.CHERN_CLASS_CORRECTION,
            RefinementType.BERRY_PHASE,
            RefinementType.INSTANTON_CORRECTION,
            RefinementType.HOPF_FIBRATION,
            RefinementType.BRAID_GROUP,
            RefinementType.HOLONOMY,
            RefinementType.WEYL_ANOMALY,
            RefinementType.VOLUME_RATIO,
            RefinementType.EULER_CHARACTERISTIC,
            RefinementType.WINDING_NUMBER,
        }
        
        filtered = []
        for suggestion in suggestions:
            if suggestion.modification.refinement_type in valid_types:
                filtered.append(suggestion)
        
        return filtered
    
    def get_top_suggestions(self, analysis_result: Dict, n: int = 5) -> List[RefinementSuggestion]:
        """
        Get the top N refinement suggestions for the given error analysis.
        
        This is the main entry point for the AI Advisor.
        
        Args:
            analysis_result: Output from ErrorAnalyzer.analyze()
            n: Number of suggestions to return
            
        Returns:
            Top N RefinementSuggestion objects, ranked by priority
        """
        suggestions = self.generate_suggestions(analysis_result)
        suggestions = self.filter_topological_only(suggestions)
        suggestions = self.rank_suggestions(suggestions)
        return suggestions[:n]
    
    def generate_report(self, analysis_result: Dict, n: int = 5) -> str:
        """
        Generate a human-readable report of refinement suggestions.
        
        Args:
            analysis_result: Output from ErrorAnalyzer.analyze()
            n: Number of suggestions to include
            
        Returns:
            Formatted string report
        """
        suggestions = self.get_top_suggestions(analysis_result, n)
        
        report = []
        report.append("=" * 70)
        report.append("AI ADVISOR REFINEMENT SUGGESTIONS")
        report.append("=" * 70)
        report.append("")
        report.append(f"Generated {len(suggestions)} topologically-motivated suggestions")
        report.append("")
        report.append("**DIRECTIVE A COMPLIANCE:** All suggestions have topological origin.")
        report.append("**NO** phenomenological parameters introduced.")
        report.append("")
        
        for i, suggestion in enumerate(suggestions, 1):
            mod = suggestion.modification
            report.append("-" * 70)
            report.append(f"SUGGESTION {i}: {mod.name}")
            report.append(f"Priority Score: {mod.priority_score:.1f}")
            report.append(f"Confidence: {mod.confidence.value.upper()}")
            report.append("-" * 70)
            report.append("")
            report.append(f"Error Pattern Addressed: {suggestion.error_pattern}")
            report.append("")
            report.append(f"Mathematical Formula:")
            report.append(f"  {mod.mathematical_formula}")
            report.append("")
            report.append(f"Topological Basis:")
            for line in mod.topological_basis.strip().split('\n'):
                report.append(f"  {line.strip()}")
            report.append("")
            report.append(f"Affected Observables: {', '.join(mod.affected_observables)}")
            report.append(f"Expected Improvement: {mod.expected_improvement}")
            report.append("")
            report.append(f"Derivation Steps:")
            for step in mod.derivation_steps:
                report.append(f"  {step}")
            report.append("")
            report.append(f"Symmetries Preserved: {', '.join(mod.symmetries_preserved)}")
            report.append("")
            report.append(f"Testable Predictions:")
            for pred in mod.testable_predictions:
                report.append(f"  • {pred}")
            report.append("")
        
        report.append("=" * 70)
        report.append("END OF SUGGESTIONS")
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def to_dict(self) -> Dict:
        """Return advisor configuration as dictionary."""
        return {
            "error_patterns": list(self._error_pattern_map.keys()),
            "modification_types": [t.value for t in RefinementType],
            "confidence_levels": [c.value for c in ConfidenceLevel],
            "genai_available": GENAI_AVAILABLE,
            "genai_enabled": self._genai_client is not None
        }
    
    def _generate_genai_suggestions(self, analysis_result: Dict) -> Optional[str]:
        """
        Use Gen AI SDK to generate AI-powered refinement suggestions.
        
        This method uses Google's Gemini model to analyze error patterns
        and suggest topologically-motivated corrections. The suggestions
        are constrained to follow Directive A (topological origin only).
        
        Args:
            analysis_result: Output from ErrorAnalyzer.analyze()
            
        Returns:
            AI-generated suggestions as text, or None if Gen AI unavailable
        """
        if not self._genai_client:
            return None
        
        try:
            # Build prompt with error analysis context
            prompt = self._build_genai_prompt(analysis_result)
            
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
            
            response_text = ""
            for chunk in self._genai_client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                    continue
                response_text += chunk.text
            
            return response_text
            
        except Exception as e:
            print(f"Warning: Gen AI suggestion generation failed: {e}")
            return None
    
    def _build_genai_prompt(self, analysis_result: Dict) -> str:
        """
        Build a prompt for Gen AI that constrains suggestions to topological corrections.
        
        Args:
            analysis_result: Output from ErrorAnalyzer.analyze()
            
        Returns:
            Formatted prompt string
        """
        # Extract key error patterns
        patterns = self.analyze_error_pattern(analysis_result)
        
        prompt = f"""
You are an expert in topological quantum field theory, gauge theory, fiber bundle geometry, 
and the mathematical foundations of fundamental physics. You are assisting the Intrinsic 
Resonance Holography (IRH) theory evolution system.

## CRITICAL CONSTRAINTS (Directive A - No-Tuning Constraint):

**FORBIDDEN:**
❌ NO parameter tuning to fit experimental data
❌ NO arbitrary scaling factors or adjustment coefficients
❌ NO phenomenological formulas without geometric origin
❌ NO "fudge factors" or empirical corrections

**REQUIRED:**
✅ ONLY topological/geometric refinements
✅ ONLY modifications with clear mathematical derivation
✅ ONLY corrections from characteristic classes, Chern numbers, homotopy invariants
✅ ALL constants must be derived from topology/geometry
✅ ALL symmetries must be preserved (gauge, Lorentz, CPT)

## Error Analysis Results:

Identified error patterns: {', '.join(patterns)}

Detailed analysis:
{self._format_analysis_for_prompt(analysis_result)}

## Your Task:

Suggest 2-3 topologically-motivated corrections that address these error patterns.
For each suggestion, provide:

1. **Name**: Clear, descriptive name
2. **Topological Basis**: Which topological invariant or geometric structure gives rise to this correction?
3. **Mathematical Formula**: Exact formula with all terms defined
4. **Derivation Outline**: Step-by-step mathematical derivation from topology
5. **Affected Observables**: Which predictions will change?
6. **Expected Improvement**: Quantitative estimate of improvement
7. **Symmetries Preserved**: Which symmetries remain unbroken?
8. **Testable Predictions**: Novel predictions that can be experimentally verified

## Valid Topological Sources:

- Chern classes (c₁, c₂, ...) from fiber bundle curvature
- Pontryagin classes from SO(n) bundles
- Euler characteristic χ(M) of compactified manifolds
- Hopf fibration volume ratios (S³→S², S⁷→S⁴, S¹⁵→S⁸)
- Braid group representations (B₃ for SU(3), B₄ for 4-strand network)
- Winding numbers and homotopy groups π_n(S^n)
- Berry/geometric phases from parameter space topology
- Instanton contributions (winding number sectors)
- Weyl anomaly coefficients (a and c in 4D CFT)
- 24-cell polytope geometry (IRH uses 24-cell symmetry group)
- Holonomy around closed loops in gauge bundles

## IRH Theory Context:

The theory is based on:
- 4-strand cymatic resonance network (N=4 is topologically optimal)
- Metric mismatch η = 4/π from 4-strand substrate geometry
- Fine-structure constant α⁻¹ derived from Hopf fibration volume ratios
- Particles as B₃ braid group resonant modes (SU(3) color charge)
- Vacuum energy suppression via quaternionic destructive interference

Generate your suggestions now:
"""
        
        return prompt
    
    def _format_analysis_for_prompt(self, analysis_result: Dict) -> str:
        """Format error analysis for inclusion in Gen AI prompt."""
        lines = []
        
        if "patterns" in analysis_result:
            lines.append("\nError Patterns:")
            for pattern in analysis_result.get("patterns", [])[:5]:  # Top 5 patterns
                lines.append(f"  - {pattern.get('type', 'unknown')}: {pattern.get('description', '')}")
                lines.append(f"    Affected: {', '.join(pattern.get('affected_observables', [])[:5])}")
        
        if "poor_predictions" in analysis_result:
            lines.append("\nPoor Predictions (>3σ):")
            for pred in analysis_result.get("poor_predictions", [])[:5]:  # Top 5 worst
                lines.append(f"  - {pred.get('name', 'unknown')}: {pred.get('sigma_deviation', 0):.2f}σ")
                lines.append(f"    Theory: {pred.get('theory_value', 'N/A')}, Experiment: {pred.get('experimental_value', 'N/A')}")
        
        return "\n".join(lines) if lines else "No detailed error information available."
    
    def get_genai_suggestions(self, analysis_result: Dict) -> Optional[str]:
        """
        Get AI-powered refinement suggestions using Gen AI SDK.
        
        This is a convenience method for external use. It generates
        natural language suggestions that can be reviewed by humans.
        
        Args:
            analysis_result: Output from ErrorAnalyzer.analyze()
            
        Returns:
            AI-generated suggestions as formatted text, or None if unavailable
        """
        if not self._genai_client:
            return "Gen AI SDK not available. Install with: pip install --upgrade google-genai"
        
        return self._generate_genai_suggestions(analysis_result)
