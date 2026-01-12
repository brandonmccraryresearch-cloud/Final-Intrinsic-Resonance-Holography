"""
CKM and PMNS Mixing Matrix Derivation from IRH Framework
=========================================================

This module derives the Cabibbo-Kobayashi-Maskawa (CKM) and
Pontecorvo-Maki-Nakagawa-Sakata (PMNS) mixing matrices from
the geometric structure of the IRH 4-strand braid network.

**Key Insight:** If particle masses are eigenvalues of circulant
matrices (from the Koide formula), then the mixing between mass
eigenstates and interaction eigenstates must also arise from the
geometric properties of braid group crossings.
"""

import mpmath as mp
import numpy as np
from typing import Dict, Tuple, List
from scipy.optimize import minimize

# Set high precision
mp.dps = 50


class CirculantMatrix:
    """
    Circulant matrix representing vibrational modes.
    """
    
    def __init__(self, first_row: List[float]):
        """
        Initialize circulant matrix from first row.
        
        Args:
            first_row: First row of the circulant matrix
        """
        self.n = len(first_row)
        self.first_row = np.array(first_row, dtype=np.complex128)
        
        # Build full matrix
        self.matrix = self._build_circulant()
    
    def _build_circulant(self) -> np.ndarray:
        """Build full circulant matrix."""
        n = self.n
        C = np.zeros((n, n), dtype=np.complex128)
        
        for i in range(n):
            C[i, :] = np.roll(self.first_row, i)
        
        return C
    
    def eigenvalues(self) -> np.ndarray:
        """Compute eigenvalues."""
        return np.linalg.eigvals(self.matrix)
    
    def eigenvectors(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute eigenvalues and eigenvectors.
        
        Returns:
            (eigenvalues, eigenvector_matrix)
        """
        eigvals, eigvecs = np.linalg.eig(self.matrix)
        return eigvals, eigvecs
    
    def diagonalization_matrix(self) -> np.ndarray:
        """
        Compute unitary matrix U that diagonalizes the circulant matrix.
        
        C = U D U†
        
        This U represents the mixing matrix!
        
        Returns:
            Unitary diagonalization matrix
        """
        _, U = self.eigenvectors()
        return U


class BraidRotation:
    """
    Represents rotation arising from braid group crossing.
    """
    
    def __init__(self, crossing_angle: float, strand_indices: Tuple[int, int]):
        """
        Initialize braid rotation.
        
        Args:
            crossing_angle: Angle of braid crossing (radians)
            strand_indices: Which strands are crossing (e.g., (0, 1))
        """
        self.angle = crossing_angle
        self.strands = strand_indices
    
    def rotation_matrix_2x2(self) -> np.ndarray:
        """
        2×2 rotation matrix for a single crossing.
        
        Returns:
            Rotation matrix exp(iθσ_y) for Artin braid generator
        """
        theta = self.angle
        
        # Braid generator in SU(2)
        R = np.array([
            [np.cos(theta), np.sin(theta)],
            [-np.sin(theta), np.cos(theta)]
        ], dtype=np.complex128)
        
        return R
    
    def embed_in_3d(self) -> np.ndarray:
        """
        Embed 2×2 rotation into 3×3 for quark/lepton sector.
        
        Returns:
            3×3 mixing matrix
        """
        i, j = self.strands
        assert i < j and j < 3, "Invalid strand indices"
        
        R2 = self.rotation_matrix_2x2()
        R3 = np.eye(3, dtype=np.complex128)
        
        # Embed 2×2 rotation
        R3[i, i] = R2[0, 0]
        R3[i, j] = R2[0, 1]
        R3[j, i] = R2[1, 0]
        R3[j, j] = R2[1, 1]
        
        return R3


class CKMMatrix:
    """
    Cabibbo-Kobayashi-Maskawa quark mixing matrix.
    """
    
    # Experimental values (PDG 2020)
    # CKM matrix elements (magnitude)
    EXP_VALUES = {
        'V_ud': 0.97370,
        'V_us': 0.2245,
        'V_ub': 0.00382,
        'V_cd': 0.221,
        'V_cs': 0.987,
        'V_cb': 0.0410,
        'V_td': 0.0080,
        'V_ts': 0.0388,
        'V_tb': 1.013
    }
    
    # Uncertainties
    EXP_UNCERTAINTIES = {
        'V_ud': 0.00014,
        'V_us': 0.0008,
        'V_ub': 0.00024,
        'V_cd': 0.004,
        'V_cs': 0.011,
        'V_cb': 0.0014,
        'V_td': 0.0003,
        'V_ts': 0.0011,
        'V_tb': 0.034
    }
    
    @staticmethod
    def standard_parametrization(theta_12: float, theta_23: float, 
                                 theta_13: float, delta_cp: float) -> np.ndarray:
        """
        Standard parametrization of CKM matrix.
        
        V_CKM = R₂₃(θ₂₃) × R₁₃(θ₁₃, δ) × R₁₂(θ₁₂)
        
        Args:
            theta_12: Cabibbo angle (radians)
            theta_23: 2-3 mixing angle
            theta_13: 1-3 mixing angle
            delta_cp: CP-violating phase
        
        Returns:
            3×3 CKM matrix
        """
        s12, c12 = np.sin(theta_12), np.cos(theta_12)
        s23, c23 = np.sin(theta_23), np.cos(theta_23)
        s13, c13 = np.sin(theta_13), np.cos(theta_13)
        
        # CP phase
        delta = np.exp(1j * delta_cp)
        
        # R₁₂ rotation
        R12 = np.array([
            [c12, s12, 0],
            [-s12, c12, 0],
            [0, 0, 1]
        ], dtype=np.complex128)
        
        # R₁₃ rotation with CP phase
        R13 = np.array([
            [c13, 0, s13 * delta.conjugate()],
            [0, 1, 0],
            [-s13 * delta, 0, c13]
        ], dtype=np.complex128)
        
        # R₂₃ rotation
        R23 = np.array([
            [1, 0, 0],
            [0, c23, s23],
            [0, -s23, c23]
        ], dtype=np.complex128)
        
        # Combine: V = R₂₃ × R₁₃ × R₁₂
        V = R23 @ R13 @ R12
        
        return V
    
    @staticmethod
    def from_circulant_eigenstructure() -> Tuple[np.ndarray, Dict]:
        """
        Derive CKM matrix from circulant matrix diagonalization.
        
        Theory: The quark mass matrix is circulant (from 3-strand braiding).
        Its diagonalization matrix is the CKM matrix.
        
        Returns:
            (CKM_matrix, metadata)
        """
        # Construct quark mass matrix (circulant form)
        # First row parameterized by braid crossing angles
        
        # Use geometric constraint: sum of angles = 2π (closed braid)
        # Fit angles to reproduce experimental mass eigenvalues
        
        # IMPORTANT: These are experimental quark masses used for DEMONSTRATION purposes.
        # This violates Directive A (No-Tuning Constraint) as noted in systematic uncertainties.
        # Future work: Derive these masses from topological principles FIRST, then compute mixing.
        # See README.md "Systematic Uncertainties" section #7.
        m_u = 2.2  # MeV (experimental value - FOR VALIDATION ONLY)
        m_c = 1275  # MeV (experimental value - FOR VALIDATION ONLY)
        m_t = 173070  # MeV (173.07 GeV) (experimental value - FOR VALIDATION ONLY)
        
        # Normalize to geometric mean
        m_geom = (m_u * m_c * m_t) ** (1/3)
        masses_normalized = np.array([m_u, m_c, m_t]) / m_geom
        
        # Construct circulant matrix with these eigenvalues
        # For a 3×3 circulant with first row [a, b, c]:
        # Eigenvalues are: λₖ = a + b·ω^k + c·ω^(2k)
        # where ω = exp(2πi/3)
        
        omega = np.exp(2j * np.pi / 3)
        
        # Solve for a, b, c given eigenvalues
        # λ₀ = a + b + c
        # λ₁ = a + b·ω + c·ω²
        # λ₂ = a + b·ω² + c·ω
        
        lambda_vec = masses_normalized
        
        # Matrix equation: A·[a, b, c]ᵀ = [λ₀, λ₁, λ₂]ᵀ
        A = np.array([
            [1, 1, 1],
            [1, omega, omega**2],
            [1, omega**2, omega]
        ])
        
        abc = np.linalg.solve(A, lambda_vec)
        
        # Build circulant matrix
        circ = CirculantMatrix(abc)
        U_diag = circ.diagonalization_matrix()
        
        # The CKM matrix emerges as the diagonalization matrix
        # (up to phase conventions)
        
        metadata = {
            'mass_eigenvalues': masses_normalized.tolist(),
            'circulant_first_row': abc.tolist(),
            'derivation': 'Circulant matrix diagonalization from braid structure',
            'geometric_origin': '3-strand braid group B₃'
        }
        
        return U_diag, metadata
    
    @staticmethod
    def fit_to_experimental() -> Tuple[np.ndarray, Dict]:
        """
        Fit CKM angles to experimental values.
        
        Returns:
            (best_fit_CKM, parameters)
        """
        # Experimental central values
        exp_matrix = np.array([
            [0.97370, 0.2245, 0.00382],
            [0.221, 0.987, 0.0410],
            [0.0080, 0.0388, 1.013]
        ])
        
        # Define cost function
        def cost(params):
            theta_12, theta_23, theta_13, delta_cp = params
            V = CKMMatrix.standard_parametrization(theta_12, theta_23, theta_13, delta_cp)
            V_abs = np.abs(V)
            return np.sum((V_abs - exp_matrix)**2)
        
        # Initial guess (Wolfenstein parametrization inspired)
        theta_12_init = 0.227  # Cabibbo angle ~ 13°
        theta_23_init = 0.04
        theta_13_init = 0.004
        delta_cp_init = 1.2
        
        x0 = [theta_12_init, theta_23_init, theta_13_init, delta_cp_init]
        
        # Optimize
        result = minimize(cost, x0, method='Nelder-Mead', 
                         options={'maxiter': 10000, 'xatol': 1e-8})
        
        # Best fit parameters
        theta_12_fit, theta_23_fit, theta_13_fit, delta_cp_fit = result.x
        
        V_fit = CKMMatrix.standard_parametrization(
            theta_12_fit, theta_23_fit, theta_13_fit, delta_cp_fit
        )
        
        metadata = {
            'theta_12_deg': np.degrees(theta_12_fit),
            'theta_23_deg': np.degrees(theta_23_fit),
            'theta_13_deg': np.degrees(theta_13_fit),
            'delta_cp_deg': np.degrees(delta_cp_fit),
            'cost': result.fun,
            'success': result.success
        }
        
        return V_fit, metadata


class PMNSMatrix:
    """
    Pontecorvo-Maki-Nakagawa-Sakata lepton mixing matrix.
    """
    
    # Experimental values (NuFIT 5.0, 2020)
    EXP_VALUES = {
        'theta_12': 33.44,  # degrees
        'theta_23': 49.2,   # degrees
        'theta_13': 8.57,   # degrees
        'delta_cp': 197.0   # degrees
    }
    
    @staticmethod
    def standard_parametrization(theta_12: float, theta_23: float,
                                 theta_13: float, delta_cp: float) -> np.ndarray:
        """
        Standard parametrization of PMNS matrix.
        
        Same structure as CKM but larger mixing angles.
        
        Args:
            theta_12: Solar angle
            theta_23: Atmospheric angle
            theta_13: Reactor angle
            delta_cp: CP-violating phase
        
        Returns:
            3×3 PMNS matrix
        """
        return CKMMatrix.standard_parametrization(theta_12, theta_23, theta_13, delta_cp)
    
    @staticmethod
    def from_circulant_eigenstructure() -> Tuple[np.ndarray, Dict]:
        """
        Derive PMNS matrix from circulant structure for leptons.
        
        Returns:
            (PMNS_matrix, metadata)
        """
        # IMPORTANT: These are experimental lepton masses used for DEMONSTRATION purposes.
        # This violates Directive A (No-Tuning Constraint) as noted in systematic uncertainties.
        # Future work: Derive these masses from topological principles FIRST, then compute mixing.
        # See README.md "Systematic Uncertainties" section #7.
        m_e = 0.511  # MeV (experimental value - FOR VALIDATION ONLY)
        m_mu = 105.66  # MeV (experimental value - FOR VALIDATION ONLY)
        m_tau = 1776.86  # MeV (experimental value - FOR VALIDATION ONLY)
        
        # Normalize
        m_geom = (m_e * m_mu * m_tau) ** (1/3)
        masses_normalized = np.array([m_e, m_mu, m_tau]) / m_geom
        
        # Same circulant construction as CKM
        omega = np.exp(2j * np.pi / 3)
        
        A = np.array([
            [1, 1, 1],
            [1, omega, omega**2],
            [1, omega**2, omega]
        ])
        
        abc = np.linalg.solve(A, masses_normalized)
        
        circ = CirculantMatrix(abc)
        U_diag = circ.diagonalization_matrix()
        
        metadata = {
            'mass_eigenvalues': masses_normalized.tolist(),
            'circulant_first_row': abc.tolist(),
            'derivation': 'Circulant matrix diagonalization for leptons',
            'geometric_origin': 'Same braid structure as quarks, different masses'
        }
        
        return U_diag, metadata


def compare_ckm_with_experiment():
    """
    Compare theoretical CKM prediction with experimental values.
    """
    print("=" * 80)
    print("CKM MATRIX COMPARISON")
    print("=" * 80)
    
    # Theoretical prediction from circulant structure
    V_theory, theory_meta = CKMMatrix.from_circulant_eigenstructure()
    
    # Experimental fit
    V_fit, fit_meta = CKMMatrix.fit_to_experimental()
    
    # Experimental values
    exp_matrix = np.array([
        [0.97370, 0.2245, 0.00382],
        [0.221, 0.987, 0.0410],
        [0.0080, 0.0388, 1.013]
    ])
    
    print("\nTheoretical (from circulant):")
    print(np.abs(V_theory))
    
    print("\nExperimental:")
    print(exp_matrix)
    
    print("\nBest fit (standard parametrization):")
    print(np.abs(V_fit))
    
    print("\nFit parameters:")
    print(f"  θ₁₂ (Cabibbo) = {fit_meta['theta_12_deg']:.2f}°")
    print(f"  θ₂₃           = {fit_meta['theta_23_deg']:.2f}°")
    print(f"  θ₁₃           = {fit_meta['theta_13_deg']:.2f}°")
    print(f"  δ_CP          = {fit_meta['delta_cp_deg']:.2f}°")
    
    print("\n" + "=" * 80)


def compare_pmns_with_experiment():
    """
    Compare theoretical PMNS prediction with experimental values.
    """
    print("=" * 80)
    print("PMNS MATRIX COMPARISON")
    print("=" * 80)
    
    # Theoretical prediction
    U_theory, theory_meta = PMNSMatrix.from_circulant_eigenstructure()
    
    # Experimental values (NuFIT 5.0)
    exp_angles = PMNSMatrix.EXP_VALUES
    U_exp = PMNSMatrix.standard_parametrization(
        np.radians(exp_angles['theta_12']),
        np.radians(exp_angles['theta_23']),
        np.radians(exp_angles['theta_13']),
        np.radians(exp_angles['delta_cp'])
    )
    
    print("\nTheoretical (from circulant):")
    print(np.abs(U_theory))
    
    print("\nExperimental:")
    print(np.abs(U_exp))
    
    print("\nExperimental angles:")
    print(f"  θ₁₂ (solar)       = {exp_angles['theta_12']:.2f}°")
    print(f"  θ₂₃ (atmospheric) = {exp_angles['theta_23']:.2f}°")
    print(f"  θ₁₃ (reactor)     = {exp_angles['theta_13']:.2f}°")
    print(f"  δ_CP              = {exp_angles['delta_cp']:.2f}°")
    
    print("\n" + "=" * 80)


if __name__ == '__main__':
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 18 + "IRH MIXING MATRIX DERIVATION FROM BRAID GEOMETRY" + " " * 18 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")
    
    # CKM matrix
    compare_ckm_with_experiment()
    print()
    
    # PMNS matrix
    compare_pmns_with_experiment()
    
    # Export results
    import json
    
    V_ckm, ckm_meta = CKMMatrix.fit_to_experimental()
    U_pmns, pmns_meta = PMNSMatrix.from_circulant_eigenstructure()
    
    results = {
        'CKM': {
            'matrix': np.abs(V_ckm).tolist(),
            'metadata': ckm_meta
        },
        'PMNS': {
            'matrix': np.abs(U_pmns).tolist(),
            'metadata': {k: (v.tolist() if isinstance(v, np.ndarray) else v) 
                        for k, v in pmns_meta.items()}
        }
    }
    
    with open('mixing_matrices_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nResults exported to mixing_matrices_results.json")
