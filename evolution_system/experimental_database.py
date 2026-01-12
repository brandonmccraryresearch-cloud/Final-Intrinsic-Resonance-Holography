"""
Experimental Database for IRH Theory Evolution System
=====================================================

Comprehensive database of experimental values from:
- CODATA 2022: Fundamental physical constants
- PDG 2022: Particle physics properties
- Planck 2018: Cosmological parameters

**CRITICAL:** These values are ONLY for validation purposes.
They are NEVER used as inputs to theoretical calculations.
All values are marked "FOR VALIDATION ONLY" per Directive A.

Data Sources:
-------------
- CODATA 2022: https://physics.nist.gov/cuu/Constants/
- PDG 2022: https://pdg.lbl.gov/
- Planck 2018: https://arxiv.org/abs/1807.06209

Usage:
------
```python
from evolution_system import ExperimentalDatabase

db = ExperimentalDatabase()

# Get a specific constant
alpha = db.get('alpha')
print(f"α = {alpha.value} ± {alpha.uncertainty}")

# Get all constants by tier
tier1 = db.get_tier(1)
for const in tier1:
    print(f"{const.name}: {const.value}")

# Get all constants by category  
leptons = db.get_category('lepton_masses')
```
"""

import mpmath as mp
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from enum import Enum

# Set high precision for all calculations
mp.dps = 50


class ConstantCategory(Enum):
    """Categories of experimental constants."""
    FUNDAMENTAL = "fundamental"           # α, ℏ, c, G
    LEPTON_MASSES = "lepton_masses"       # e, μ, τ masses
    QUARK_MASSES = "quark_masses"         # u, d, s, c, b, t masses
    GAUGE_COUPLINGS = "gauge_couplings"   # α₁, α₂, α₃
    ELECTROWEAK = "electroweak"           # sin²θW, MZ, MW, MH
    COSMOLOGICAL = "cosmological"         # Λ, ΩΛ, ΩDM, Ωb, H0
    MIXING_MATRICES = "mixing_matrices"   # CKM, PMNS elements
    PRECISION_TESTS = "precision_tests"   # g-2, EDMs
    QCD = "qcd"                           # ΛQCD, string tension


class ValidationTier(Enum):
    """Validation tiers for prioritizing tests."""
    TIER_1 = 1  # Core parameters: α, gauge couplings, lepton masses
    TIER_2 = 2  # Derived quantities: Higgs VEV, W/Z masses, CKM
    TIER_3 = 3  # Cosmological: Λ, ΩΛ, ΩDM, Ωb
    TIER_4 = 4  # Precision tests: g-2, EDMs, CP violation


@dataclass
class ExperimentalConstant:
    """
    An experimental measurement with uncertainty and metadata.
    
    **NOTE:** FOR VALIDATION ONLY - Never use as input to theory calculations.
    """
    name: str
    symbol: str
    value: mp.mpf
    uncertainty: mp.mpf
    unit: str
    source: str
    year: int
    category: ConstantCategory
    tier: ValidationTier
    description: str = ""
    notes: str = ""
    
    # Cross-reference to theory derivation (if available)
    theory_reference: Optional[str] = None
    
    # Status for tracking
    is_validated: bool = False
    validation_result: Optional[Dict] = field(default=None, repr=False)
    
    def __post_init__(self):
        """Ensure values are mpmath types."""
        if not isinstance(self.value, mp.mpf):
            self.value = mp.mpf(str(self.value))
        if not isinstance(self.uncertainty, mp.mpf):
            self.uncertainty = mp.mpf(str(self.uncertainty))
    
    def relative_uncertainty(self) -> mp.mpf:
        """Return relative uncertainty."""
        if self.value == 0:
            return mp.mpf('inf')
        return self.uncertainty / abs(self.value)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'name': self.name,
            'symbol': self.symbol,
            'value': float(self.value),
            'uncertainty': float(self.uncertainty),
            'unit': self.unit,
            'source': self.source,
            'year': self.year,
            'category': self.category.value,
            'tier': self.tier.value,
            'description': self.description,
            'notes': self.notes,
            'theory_reference': self.theory_reference,
        }


class ExperimentalDatabase:
    """
    Comprehensive database of experimental measurements.
    
    **CRITICAL:** All values are FOR VALIDATION ONLY per Directive A.
    These values must NEVER be used as inputs to theoretical calculations.
    
    Structure:
    ----------
    - Tier 1: Core parameters (α, gauge couplings, lepton masses)
    - Tier 2: Derived quantities (Higgs VEV, W/Z masses, CKM)
    - Tier 3: Cosmological (Λ, ΩΛ, ΩDM, Ωb)
    - Tier 4: Precision tests (g-2, EDMs, CP violation)
    """
    
    def __init__(self):
        """Initialize the experimental database."""
        self._constants: Dict[str, ExperimentalConstant] = {}
        self._load_all_constants()
    
    def _load_all_constants(self):
        """Load all experimental constants into the database."""
        self._load_fundamental_constants()
        self._load_lepton_masses()
        self._load_quark_masses()
        self._load_gauge_couplings()
        self._load_electroweak_parameters()
        self._load_cosmological_parameters()
        self._load_qcd_parameters()
        self._load_mixing_matrices()
        self._load_precision_tests()
    
    def _load_fundamental_constants(self):
        """
        CODATA 2022 fundamental constants.
        
        **FOR VALIDATION ONLY** - Per Directive A, these are never used
        as inputs to theoretical calculations.
        """
        # Fine-structure constant
        self._constants['alpha'] = ExperimentalConstant(
            name="Fine-structure constant",
            symbol="α",
            value=mp.mpf('7.2973525693e-3'),
            uncertainty=mp.mpf('1.1e-12'),
            unit="dimensionless",
            source="CODATA 2022",
            year=2022,
            category=ConstantCategory.FUNDAMENTAL,
            tier=ValidationTier.TIER_1,
            description="Electromagnetic coupling constant",
            theory_reference="IRH v26.0 Section 1; notebooks/02_harmony_functional.ipynb",
            notes="FOR VALIDATION ONLY - Never use as input to theory"
        )
        
        # Inverse fine-structure constant - EXPERIMENTAL VALUE FOR VALIDATION ONLY
        self._constants['alpha_inv'] = ExperimentalConstant(
            name="Inverse fine-structure constant",
            symbol="α⁻¹",
            value=mp.mpf('137.035999177'),  # CODATA 2022 - FOR VALIDATION ONLY
            uncertainty=mp.mpf('2.1e-8'),
            unit="dimensionless",
            source="CODATA 2022",
            year=2022,
            category=ConstantCategory.FUNDAMENTAL,
            tier=ValidationTier.TIER_1,
            description="Inverse of electromagnetic coupling",
            theory_reference="IRH v26.0 Section 1; notebooks/02_harmony_functional.ipynb",
            notes="FOR VALIDATION ONLY - Primary validation target"
        )
        
        # Planck constant
        self._constants['hbar'] = ExperimentalConstant(
            name="Reduced Planck constant",
            symbol="ℏ",
            value=mp.mpf('1.054571817e-34'),
            uncertainty=mp.mpf('0'),  # Exact by definition
            unit="J⋅s",
            source="CODATA 2022",
            year=2022,
            category=ConstantCategory.FUNDAMENTAL,
            tier=ValidationTier.TIER_1,
            description="Quantum of action (exact by SI definition)",
            notes="FOR VALIDATION ONLY - Exact value"
        )
        
        # Speed of light
        self._constants['c'] = ExperimentalConstant(
            name="Speed of light in vacuum",
            symbol="c",
            value=mp.mpf('299792458'),
            uncertainty=mp.mpf('0'),  # Exact by definition
            unit="m/s",
            source="CODATA 2022",
            year=2022,
            category=ConstantCategory.FUNDAMENTAL,
            tier=ValidationTier.TIER_1,
            description="Maximum signal speed (exact by SI definition)",
            notes="FOR VALIDATION ONLY - Exact value"
        )
        
        # Gravitational constant
        self._constants['G'] = ExperimentalConstant(
            name="Newtonian gravitational constant",
            symbol="G",
            value=mp.mpf('6.67430e-11'),
            uncertainty=mp.mpf('1.5e-15'),
            unit="m³⋅kg⁻¹⋅s⁻²",
            source="CODATA 2022",
            year=2022,
            category=ConstantCategory.FUNDAMENTAL,
            tier=ValidationTier.TIER_2,
            description="Gravitational coupling strength",
            notes="FOR VALIDATION ONLY - Largest relative uncertainty of fundamental constants"
        )
        
        # Planck mass
        self._constants['m_planck'] = ExperimentalConstant(
            name="Planck mass",
            symbol="m_Pl",
            value=mp.mpf('2.176434e-8'),
            uncertainty=mp.mpf('2.4e-13'),
            unit="kg",
            source="CODATA 2022",
            year=2022,
            category=ConstantCategory.FUNDAMENTAL,
            tier=ValidationTier.TIER_2,
            description="Characteristic mass scale of quantum gravity",
            notes="FOR VALIDATION ONLY - Derived from ℏ, c, G"
        )
        
        # Planck length
        self._constants['l_planck'] = ExperimentalConstant(
            name="Planck length",
            symbol="l_Pl",
            value=mp.mpf('1.616255e-35'),
            uncertainty=mp.mpf('1.8e-40'),
            unit="m",
            source="CODATA 2022",
            year=2022,
            category=ConstantCategory.FUNDAMENTAL,
            tier=ValidationTier.TIER_2,
            description="Characteristic length scale of quantum gravity",
            notes="FOR VALIDATION ONLY - Derived from ℏ, c, G"
        )
    
    def _load_lepton_masses(self):
        """
        Lepton masses from CODATA 2022 / PDG 2022.
        
        **FOR VALIDATION ONLY** - Per Directive A
        """
        # Electron mass - EXPERIMENTAL VALUE FOR VALIDATION ONLY
        self._constants['m_electron'] = ExperimentalConstant(
            name="Electron mass",
            symbol="m_e",
            value=mp.mpf('0.51099895000'),  # MeV/c² - CODATA 2022 FOR VALIDATION ONLY
            uncertainty=mp.mpf('1.5e-10'),
            unit="MeV/c²",
            source="CODATA 2022",
            year=2022,
            category=ConstantCategory.LEPTON_MASSES,
            tier=ValidationTier.TIER_1,
            description="Electron rest mass",
            theory_reference="IRH v26.0 Section 3 (Koide formula); notebooks/03_particle_sector.ipynb",
            notes="FOR VALIDATION ONLY - Koide formula constraint"
        )
        
        # Muon mass - EXPERIMENTAL VALUE FOR VALIDATION ONLY
        self._constants['m_muon'] = ExperimentalConstant(
            name="Muon mass",
            symbol="m_μ",
            value=mp.mpf('105.6583755'),  # MeV/c² - CODATA 2022 FOR VALIDATION ONLY
            uncertainty=mp.mpf('2.3e-6'),
            unit="MeV/c²",
            source="CODATA 2022",
            year=2022,
            category=ConstantCategory.LEPTON_MASSES,
            tier=ValidationTier.TIER_1,
            description="Muon rest mass",
            theory_reference="IRH v26.0 Section 3 (Koide formula); notebooks/03_particle_sector.ipynb",
            notes="FOR VALIDATION ONLY - Koide formula constraint"
        )
        
        # Tau mass - EXPERIMENTAL VALUE FOR VALIDATION ONLY
        self._constants['m_tau'] = ExperimentalConstant(
            name="Tau mass",
            symbol="m_τ",
            value=mp.mpf('1776.86'),  # MeV/c² - PDG 2022 FOR VALIDATION ONLY
            uncertainty=mp.mpf('0.12'),
            unit="MeV/c²",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.LEPTON_MASSES,
            tier=ValidationTier.TIER_1,
            description="Tau rest mass",
            theory_reference="IRH v26.0 Section 3 (Koide formula); notebooks/03_particle_sector.ipynb",
            notes="FOR VALIDATION ONLY - Koide formula constraint"
        )
        
        # Electron neutrino mass (upper limit)
        self._constants['m_nu_e'] = ExperimentalConstant(
            name="Electron neutrino mass limit",
            symbol="m_νe",
            value=mp.mpf('0'),  # Upper limit
            uncertainty=mp.mpf('0.8e-6'),  # 0.8 eV upper limit
            unit="MeV/c²",
            source="KATRIN 2022",
            year=2022,
            category=ConstantCategory.LEPTON_MASSES,
            tier=ValidationTier.TIER_4,
            description="Direct kinematic upper limit",
            notes="FOR VALIDATION ONLY - Upper limit only"
        )
    
    def _load_quark_masses(self):
        """
        Quark masses from PDG 2022.
        
        **FOR VALIDATION ONLY** - Per Directive A
        
        Note: Light quark masses are MS-bar values at μ = 2 GeV.
        Heavy quark masses are pole masses.
        """
        # Up quark
        self._constants['m_up'] = ExperimentalConstant(
            name="Up quark mass",
            symbol="m_u",
            value=mp.mpf('2.16'),  # MeV (MS-bar at 2 GeV)
            uncertainty=mp.mpf('0.49'),
            unit="MeV/c²",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.QUARK_MASSES,
            tier=ValidationTier.TIER_2,
            description="Up quark MS-bar mass at 2 GeV",
            notes="FOR VALIDATION ONLY - Large uncertainty"
        )
        
        # Down quark
        self._constants['m_down'] = ExperimentalConstant(
            name="Down quark mass",
            symbol="m_d",
            value=mp.mpf('4.67'),  # MeV (MS-bar at 2 GeV)
            uncertainty=mp.mpf('0.48'),
            unit="MeV/c²",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.QUARK_MASSES,
            tier=ValidationTier.TIER_2,
            description="Down quark MS-bar mass at 2 GeV",
            notes="FOR VALIDATION ONLY - Large uncertainty"
        )
        
        # Strange quark
        self._constants['m_strange'] = ExperimentalConstant(
            name="Strange quark mass",
            symbol="m_s",
            value=mp.mpf('93.4'),  # MeV (MS-bar at 2 GeV)
            uncertainty=mp.mpf('8.6'),
            unit="MeV/c²",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.QUARK_MASSES,
            tier=ValidationTier.TIER_2,
            description="Strange quark MS-bar mass at 2 GeV",
            notes="FOR VALIDATION ONLY"
        )
        
        # Charm quark
        self._constants['m_charm'] = ExperimentalConstant(
            name="Charm quark mass",
            symbol="m_c",
            value=mp.mpf('1270'),  # MeV (MS-bar at m_c)
            uncertainty=mp.mpf('20'),
            unit="MeV/c²",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.QUARK_MASSES,
            tier=ValidationTier.TIER_2,
            description="Charm quark MS-bar mass at m_c",
            notes="FOR VALIDATION ONLY"
        )
        
        # Bottom quark
        self._constants['m_bottom'] = ExperimentalConstant(
            name="Bottom quark mass",
            symbol="m_b",
            value=mp.mpf('4180'),  # MeV (MS-bar at m_b)
            uncertainty=mp.mpf('30'),
            unit="MeV/c²",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.QUARK_MASSES,
            tier=ValidationTier.TIER_2,
            description="Bottom quark MS-bar mass at m_b",
            notes="FOR VALIDATION ONLY"
        )
        
        # Top quark
        self._constants['m_top'] = ExperimentalConstant(
            name="Top quark mass",
            symbol="m_t",
            value=mp.mpf('172760'),  # MeV (pole mass)
            uncertainty=mp.mpf('300'),
            unit="MeV/c²",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.QUARK_MASSES,
            tier=ValidationTier.TIER_2,
            description="Top quark pole mass",
            notes="FOR VALIDATION ONLY - Most precisely measured quark mass"
        )
    
    def _load_gauge_couplings(self):
        """
        Gauge coupling constants at MZ scale from PDG 2022.
        
        **FOR VALIDATION ONLY** - Per Directive A
        """
        # Strong coupling constant
        self._constants['alpha_s'] = ExperimentalConstant(
            name="Strong coupling constant",
            symbol="α_s(M_Z)",
            value=mp.mpf('0.1179'),
            uncertainty=mp.mpf('0.0010'),
            unit="dimensionless",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.GAUGE_COUPLINGS,
            tier=ValidationTier.TIER_1,
            description="QCD coupling at Z mass scale",
            theory_reference="notebooks/05_gauge_sector.ipynb",
            notes="FOR VALIDATION ONLY - Key GUT constraint"
        )
        
        # Weak mixing angle (sin²θW)
        self._constants['sin2_theta_w'] = ExperimentalConstant(
            name="Weak mixing angle",
            symbol="sin²θ_W(M_Z)",
            value=mp.mpf('0.23121'),
            uncertainty=mp.mpf('0.00004'),
            unit="dimensionless",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.GAUGE_COUPLINGS,
            tier=ValidationTier.TIER_1,
            description="Electroweak mixing angle at Z mass",
            theory_reference="notebooks/05_gauge_sector.ipynb",
            notes="FOR VALIDATION ONLY - Electroweak unification"
        )
        
        # SU(2) coupling g2 at MZ
        # g₂ = e/sin(θW), where e = √(4πα)
        self._constants['g2'] = ExperimentalConstant(
            name="SU(2) gauge coupling",
            symbol="g₂(M_Z)",
            value=mp.mpf('0.6517'),
            uncertainty=mp.mpf('0.0002'),
            unit="dimensionless",
            source="PDG 2022 (derived)",
            year=2022,
            category=ConstantCategory.GAUGE_COUPLINGS,
            tier=ValidationTier.TIER_1,
            description="Weak isospin coupling at Z mass",
            notes="FOR VALIDATION ONLY - Derived from α and sin²θW"
        )
        
        # U(1) coupling g1 at MZ (GUT normalized: g₁ = √(5/3) × g')
        self._constants['g1'] = ExperimentalConstant(
            name="U(1) gauge coupling (GUT normalized)",
            symbol="g₁(M_Z)",
            value=mp.mpf('0.3574'),
            uncertainty=mp.mpf('0.0001'),
            unit="dimensionless",
            source="PDG 2022 (derived)",
            year=2022,
            category=ConstantCategory.GAUGE_COUPLINGS,
            tier=ValidationTier.TIER_1,
            description="Hypercharge coupling at Z mass (GUT normalized)",
            notes="FOR VALIDATION ONLY - g₁ = √(5/3) × g'"
        )
        
        # SU(3) coupling g3 at MZ
        # g₃ = √(4π×α_s)
        self._constants['g3'] = ExperimentalConstant(
            name="SU(3) gauge coupling",
            symbol="g₃(M_Z)",
            value=mp.mpf('1.2177'),
            uncertainty=mp.mpf('0.0052'),
            unit="dimensionless",
            source="PDG 2022 (derived)",
            year=2022,
            category=ConstantCategory.GAUGE_COUPLINGS,
            tier=ValidationTier.TIER_1,
            description="Strong coupling at Z mass",
            notes="FOR VALIDATION ONLY - g₃ = √(4πα_s)"
        )
    
    def _load_electroweak_parameters(self):
        """
        Electroweak parameters from PDG 2022.
        
        **FOR VALIDATION ONLY** - Per Directive A
        """
        # Z boson mass
        self._constants['m_Z'] = ExperimentalConstant(
            name="Z boson mass",
            symbol="M_Z",
            value=mp.mpf('91187.6'),  # MeV
            uncertainty=mp.mpf('2.1'),
            unit="MeV/c²",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.ELECTROWEAK,
            tier=ValidationTier.TIER_2,
            description="Z boson pole mass",
            notes="FOR VALIDATION ONLY - Reference scale for RG running"
        )
        
        # W boson mass
        self._constants['m_W'] = ExperimentalConstant(
            name="W boson mass",
            symbol="M_W",
            value=mp.mpf('80369'),  # MeV
            uncertainty=mp.mpf('13'),
            unit="MeV/c²",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.ELECTROWEAK,
            tier=ValidationTier.TIER_2,
            description="W boson pole mass",
            notes="FOR VALIDATION ONLY - MW anomaly under investigation"
        )
        
        # Higgs boson mass
        self._constants['m_Higgs'] = ExperimentalConstant(
            name="Higgs boson mass",
            symbol="M_H",
            value=mp.mpf('125250'),  # MeV
            uncertainty=mp.mpf('170'),
            unit="MeV/c²",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.ELECTROWEAK,
            tier=ValidationTier.TIER_2,
            description="Higgs boson mass",
            notes="FOR VALIDATION ONLY"
        )
        
        # Higgs vacuum expectation value
        self._constants['v_higgs'] = ExperimentalConstant(
            name="Higgs VEV",
            symbol="v",
            value=mp.mpf('246220'),  # MeV
            uncertainty=mp.mpf('10'),
            unit="MeV",
            source="PDG 2022 (derived)",
            year=2022,
            category=ConstantCategory.ELECTROWEAK,
            tier=ValidationTier.TIER_2,
            description="Higgs vacuum expectation value v = (√2 G_F)^(-1/2)",
            notes="FOR VALIDATION ONLY - Electroweak symmetry breaking scale"
        )
        
        # Fermi constant
        self._constants['G_F'] = ExperimentalConstant(
            name="Fermi constant",
            symbol="G_F",
            value=mp.mpf('1.1663788e-5'),  # GeV⁻²
            uncertainty=mp.mpf('6e-12'),
            unit="GeV⁻²",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.ELECTROWEAK,
            tier=ValidationTier.TIER_2,
            description="Weak interaction coupling from muon lifetime",
            notes="FOR VALIDATION ONLY - Precise from muon lifetime"
        )
    
    def _load_cosmological_parameters(self):
        """
        Cosmological parameters from Planck 2018.
        
        **FOR VALIDATION ONLY** - Per Directive A
        """
        # Hubble parameter
        self._constants['H0'] = ExperimentalConstant(
            name="Hubble constant",
            symbol="H₀",
            value=mp.mpf('67.4'),  # km/s/Mpc
            uncertainty=mp.mpf('0.5'),
            unit="km/s/Mpc",
            source="Planck 2018",
            year=2018,
            category=ConstantCategory.COSMOLOGICAL,
            tier=ValidationTier.TIER_3,
            description="Present-day expansion rate",
            notes="FOR VALIDATION ONLY - Tension with local measurements"
        )
        
        # Dark energy density
        self._constants['Omega_Lambda'] = ExperimentalConstant(
            name="Dark energy density parameter",
            symbol="Ω_Λ",
            value=mp.mpf('0.6889'),
            uncertainty=mp.mpf('0.0056'),
            unit="dimensionless",
            source="Planck 2018",
            year=2018,
            category=ConstantCategory.COSMOLOGICAL,
            tier=ValidationTier.TIER_3,
            description="Dark energy fraction of critical density",
            theory_reference="notebooks/04_cosmology.ipynb",
            notes="FOR VALIDATION ONLY - Cosmological constant problem"
        )
        
        # Dark matter density
        self._constants['Omega_DM'] = ExperimentalConstant(
            name="Dark matter density parameter",
            symbol="Ω_DM",
            value=mp.mpf('0.2607'),
            uncertainty=mp.mpf('0.0059'),
            unit="dimensionless",
            source="Planck 2018",
            year=2018,
            category=ConstantCategory.COSMOLOGICAL,
            tier=ValidationTier.TIER_3,
            description="Cold dark matter fraction of critical density",
            theory_reference="notebooks/04_cosmology.ipynb",
            notes="FOR VALIDATION ONLY"
        )
        
        # Baryon density
        self._constants['Omega_b'] = ExperimentalConstant(
            name="Baryon density parameter",
            symbol="Ω_b",
            value=mp.mpf('0.0486'),
            uncertainty=mp.mpf('0.0010'),
            unit="dimensionless",
            source="Planck 2018",
            year=2018,
            category=ConstantCategory.COSMOLOGICAL,
            tier=ValidationTier.TIER_3,
            description="Baryon fraction of critical density",
            theory_reference="notebooks/04_cosmology.ipynb",
            notes="FOR VALIDATION ONLY"
        )
        
        # Cosmological constant (in natural units)
        self._constants['Lambda'] = ExperimentalConstant(
            name="Cosmological constant",
            symbol="Λ",
            value=mp.mpf('1.1056e-52'),  # m⁻²
            uncertainty=mp.mpf('1e-54'),
            unit="m⁻²",
            source="Planck 2018 (derived)",
            year=2018,
            category=ConstantCategory.COSMOLOGICAL,
            tier=ValidationTier.TIER_3,
            description="Einstein's cosmological constant",
            theory_reference="notebooks/04_cosmology.ipynb",
            notes="FOR VALIDATION ONLY - 10^123 discrepancy with QFT"
        )
    
    def _load_qcd_parameters(self):
        """
        QCD parameters from PDG 2022 and lattice QCD.
        
        **FOR VALIDATION ONLY** - Per Directive A
        """
        # QCD scale (Lambda_QCD)
        self._constants['Lambda_QCD'] = ExperimentalConstant(
            name="QCD scale",
            symbol="Λ_QCD",
            value=mp.mpf('217'),  # MeV (5-flavor MS-bar)
            uncertainty=mp.mpf('25'),
            unit="MeV",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.QCD,
            tier=ValidationTier.TIER_2,
            description="QCD confinement scale",
            notes="FOR VALIDATION ONLY - Scale where α_s ~ 1"
        )
        
        # QCD string tension
        self._constants['sigma_QCD'] = ExperimentalConstant(
            name="QCD string tension",
            symbol="σ_QCD",
            value=mp.mpf('0.44'),  # GeV²
            uncertainty=mp.mpf('0.03'),
            unit="GeV²",
            source="Lattice QCD 2022",
            year=2022,
            category=ConstantCategory.QCD,
            tier=ValidationTier.TIER_2,
            description="String tension from Wilson loops",
            theory_reference="notebooks/05_gauge_sector.ipynb",
            notes="FOR VALIDATION ONLY - Confinement parameter"
        )
        
        # Proton mass
        self._constants['m_proton'] = ExperimentalConstant(
            name="Proton mass",
            symbol="m_p",
            value=mp.mpf('938.272088'),  # MeV/c²
            uncertainty=mp.mpf('0.000016'),
            unit="MeV/c²",
            source="CODATA 2022",
            year=2022,
            category=ConstantCategory.QCD,
            tier=ValidationTier.TIER_2,
            description="Proton rest mass",
            notes="FOR VALIDATION ONLY - Mostly QCD binding energy"
        )
        
        # Pion mass
        self._constants['m_pion'] = ExperimentalConstant(
            name="Charged pion mass",
            symbol="m_π",
            value=mp.mpf('139.57039'),  # MeV/c²
            uncertainty=mp.mpf('0.00018'),
            unit="MeV/c²",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.QCD,
            tier=ValidationTier.TIER_2,
            description="Charged pion mass",
            notes="FOR VALIDATION ONLY - Goldstone boson of chiral symmetry"
        )
    
    def _load_mixing_matrices(self):
        """
        CKM and PMNS mixing matrix parameters from PDG 2022.
        
        **FOR VALIDATION ONLY** - Per Directive A
        """
        # CKM Cabibbo angle
        self._constants['theta_12_CKM'] = ExperimentalConstant(
            name="CKM Cabibbo angle",
            symbol="θ₁₂ (CKM)",
            value=mp.mpf('0.2265'),  # radians → sin(θ₁₂)
            uncertainty=mp.mpf('0.0005'),
            unit="radians",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.MIXING_MATRICES,
            tier=ValidationTier.TIER_2,
            description="Quark 1-2 mixing angle",
            theory_reference="verification/particle_physics/mixing_matrices.py",
            notes="FOR VALIDATION ONLY - sin(θ₁₂) = |V_us|"
        )
        
        # CKM |V_cb|
        self._constants['V_cb'] = ExperimentalConstant(
            name="CKM |V_cb|",
            symbol="|V_cb|",
            value=mp.mpf('0.0410'),
            uncertainty=mp.mpf('0.0014'),
            unit="dimensionless",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.MIXING_MATRICES,
            tier=ValidationTier.TIER_2,
            description="Quark 2-3 mixing amplitude",
            notes="FOR VALIDATION ONLY"
        )
        
        # CKM |V_ub|
        self._constants['V_ub'] = ExperimentalConstant(
            name="CKM |V_ub|",
            symbol="|V_ub|",
            value=mp.mpf('0.00382'),
            uncertainty=mp.mpf('0.00024'),
            unit="dimensionless",
            source="PDG 2022",
            year=2022,
            category=ConstantCategory.MIXING_MATRICES,
            tier=ValidationTier.TIER_2,
            description="Quark 1-3 mixing amplitude",
            notes="FOR VALIDATION ONLY"
        )
        
        # PMNS solar angle
        self._constants['theta_12_PMNS'] = ExperimentalConstant(
            name="PMNS solar angle",
            symbol="θ₁₂ (PMNS)",
            value=mp.mpf('0.5836'),  # radians (33.44°)
            uncertainty=mp.mpf('0.012'),
            unit="radians",
            source="NuFIT 5.0 (2020)",
            year=2020,
            category=ConstantCategory.MIXING_MATRICES,
            tier=ValidationTier.TIER_2,
            description="Neutrino solar mixing angle",
            notes="FOR VALIDATION ONLY - Large mixing"
        )
        
        # PMNS atmospheric angle
        self._constants['theta_23_PMNS'] = ExperimentalConstant(
            name="PMNS atmospheric angle",
            symbol="θ₂₃ (PMNS)",
            value=mp.mpf('0.8587'),  # radians (49.2°)
            uncertainty=mp.mpf('0.016'),
            unit="radians",
            source="NuFIT 5.0 (2020)",
            year=2020,
            category=ConstantCategory.MIXING_MATRICES,
            tier=ValidationTier.TIER_2,
            description="Neutrino atmospheric mixing angle",
            notes="FOR VALIDATION ONLY - Near maximal"
        )
        
        # PMNS reactor angle
        self._constants['theta_13_PMNS'] = ExperimentalConstant(
            name="PMNS reactor angle",
            symbol="θ₁₃ (PMNS)",
            value=mp.mpf('0.1496'),  # radians (8.57°)
            uncertainty=mp.mpf('0.003'),
            unit="radians",
            source="NuFIT 5.0 (2020)",
            year=2020,
            category=ConstantCategory.MIXING_MATRICES,
            tier=ValidationTier.TIER_2,
            description="Neutrino reactor mixing angle",
            notes="FOR VALIDATION ONLY - Small but nonzero"
        )
    
    def _load_precision_tests(self):
        """
        Precision electroweak and QED tests from experiment.
        
        **FOR VALIDATION ONLY** - Per Directive A
        """
        # Electron anomalous magnetic moment
        self._constants['a_electron'] = ExperimentalConstant(
            name="Electron anomalous magnetic moment",
            symbol="a_e",
            value=mp.mpf('1.15965218073e-3'),
            uncertainty=mp.mpf('2.8e-13'),
            unit="dimensionless",
            source="CODATA 2022",
            year=2022,
            category=ConstantCategory.PRECISION_TESTS,
            tier=ValidationTier.TIER_4,
            description="(g-2)/2 for electron",
            notes="FOR VALIDATION ONLY - Most precise QED test"
        )
        
        # Muon anomalous magnetic moment
        self._constants['a_muon'] = ExperimentalConstant(
            name="Muon anomalous magnetic moment",
            symbol="a_μ",
            value=mp.mpf('1.16592061e-3'),
            uncertainty=mp.mpf('4.1e-10'),
            unit="dimensionless",
            source="Muon g-2 (2021)",
            year=2021,
            category=ConstantCategory.PRECISION_TESTS,
            tier=ValidationTier.TIER_4,
            description="(g-2)/2 for muon",
            notes="FOR VALIDATION ONLY - ~4.2σ tension with SM (under investigation)"
        )
        
        # Electron electric dipole moment (upper limit)
        self._constants['d_electron'] = ExperimentalConstant(
            name="Electron EDM limit",
            symbol="|d_e|",
            value=mp.mpf('0'),  # Upper limit
            uncertainty=mp.mpf('4.1e-30'),  # e⋅cm
            unit="e⋅cm",
            source="ACME III (2023)",
            year=2023,
            category=ConstantCategory.PRECISION_TESTS,
            tier=ValidationTier.TIER_4,
            description="Electron electric dipole moment (upper limit)",
            notes="FOR VALIDATION ONLY - CP violation constraint"
        )
        
        # W mass anomaly (CDF II measurement)
        self._constants['m_W_CDF'] = ExperimentalConstant(
            name="W mass (CDF II)",
            symbol="M_W (CDF)",
            value=mp.mpf('80433.5'),  # MeV
            uncertainty=mp.mpf('9.4'),
            unit="MeV/c²",
            source="CDF II (2022)",
            year=2022,
            category=ConstantCategory.PRECISION_TESTS,
            tier=ValidationTier.TIER_4,
            description="W mass from CDF II - tension with SM",
            notes="FOR VALIDATION ONLY - 7σ tension under investigation"
        )
    
    # =========================================================================
    # Public API Methods
    # =========================================================================
    
    def get(self, key: str) -> ExperimentalConstant:
        """
        Get a constant by key.
        
        Args:
            key: Constant identifier (e.g., 'alpha', 'm_electron')
        
        Returns:
            ExperimentalConstant object
        
        Raises:
            KeyError: If constant not found
        """
        if key not in self._constants:
            raise KeyError(f"Constant '{key}' not found in database. "
                          f"Available: {list(self._constants.keys())}")
        return self._constants[key]
    
    def get_value(self, key: str) -> mp.mpf:
        """
        Get just the value of a constant.
        
        Args:
            key: Constant identifier
        
        Returns:
            Value as mpmath mpf
        """
        return self.get(key).value
    
    def get_uncertainty(self, key: str) -> mp.mpf:
        """
        Get just the uncertainty of a constant.
        
        Args:
            key: Constant identifier
        
        Returns:
            Uncertainty as mpmath mpf
        """
        return self.get(key).uncertainty
    
    def get_all(self) -> Dict[str, ExperimentalConstant]:
        """
        Get all constants in the database.
        
        Returns:
            Dictionary of all constants
        """
        return self._constants.copy()
    
    def get_tier(self, tier: Union[int, ValidationTier]) -> List[ExperimentalConstant]:
        """
        Get all constants in a validation tier.
        
        Args:
            tier: Tier number (1-4) or ValidationTier enum
        
        Returns:
            List of constants in that tier
        """
        if isinstance(tier, int):
            tier = ValidationTier(tier)
        
        return [c for c in self._constants.values() if c.tier == tier]
    
    def get_category(self, category: Union[str, ConstantCategory]) -> List[ExperimentalConstant]:
        """
        Get all constants in a category.
        
        Args:
            category: Category name or ConstantCategory enum
        
        Returns:
            List of constants in that category
        """
        if isinstance(category, str):
            category = ConstantCategory(category)
        
        return [c for c in self._constants.values() if c.category == category]
    
    def list_keys(self) -> List[str]:
        """
        List all available constant keys.
        
        Returns:
            List of constant identifiers
        """
        return list(self._constants.keys())
    
    def count(self) -> int:
        """
        Return total number of constants in database.
        
        Returns:
            Number of constants
        """
        return len(self._constants)
    
    def summary(self) -> Dict:
        """
        Generate a summary of the database.
        
        Returns:
            Dictionary with counts by tier and category
        """
        return {
            'total_constants': self.count(),
            'by_tier': {
                tier.name: len(self.get_tier(tier))
                for tier in ValidationTier
            },
            'by_category': {
                cat.name: len(self.get_category(cat))
                for cat in ConstantCategory
            },
            'sources': list(set(c.source for c in self._constants.values()))
        }
    
    def to_dict(self) -> Dict:
        """
        Export entire database to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of all constants
        """
        return {
            key: const.to_dict()
            for key, const in self._constants.items()
        }
    
    def print_summary(self):
        """Print a human-readable summary of the database."""
        print("=" * 80)
        print("IRH EXPERIMENTAL DATABASE SUMMARY")
        print("=" * 80)
        print()
        
        summary = self.summary()
        print(f"Total constants: {summary['total_constants']}")
        print()
        
        print("By Validation Tier:")
        for tier_name, count in summary['by_tier'].items():
            print(f"  {tier_name}: {count} constants")
        print()
        
        print("By Category:")
        for cat_name, count in summary['by_category'].items():
            print(f"  {cat_name}: {count} constants")
        print()
        
        print("Data Sources:")
        for source in sorted(summary['sources']):
            print(f"  - {source}")
        print()
        
        print("=" * 80)
        print("⚠️  ALL VALUES ARE FOR VALIDATION ONLY - Per Directive A")
        print("=" * 80)


# Module-level instance for convenience
_default_database: Optional[ExperimentalDatabase] = None


def get_database() -> ExperimentalDatabase:
    """
    Get the default experimental database instance.
    
    Returns:
        ExperimentalDatabase singleton
    """
    global _default_database
    if _default_database is None:
        _default_database = ExperimentalDatabase()
    return _default_database


if __name__ == '__main__':
    # Demo usage
    db = ExperimentalDatabase()
    db.print_summary()
    
    # Example: Get fine-structure constant
    print("\nExample - Fine-structure constant:")
    alpha = db.get('alpha_inv')
    print(f"  {alpha.name}: {alpha.value} ± {alpha.uncertainty}")
    print(f"  Source: {alpha.source}")
    print(f"  Note: {alpha.notes}")
    
    # Export to JSON
    import json
    
    output = db.to_dict()
    with open('experimental_database.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\nDatabase exported to experimental_database.json")
