"""
Renormalization Group (RG) Flow for IRH Framework
==================================================

This module implements the running of coupling constants with energy scale,
incorporating the Weyl anomaly and topological corrections from IRH theory.

The RG flow demonstrates how the "bare" geometric value of α evolves
with energy due to quantum corrections.
"""

import mpmath as mp
import numpy as np
from typing import Dict, Tuple
import matplotlib.pyplot as plt

# Set high precision
mp.dps = 50


class RGFlow:
    """
    Renormalization Group flow for coupling constants.
    """
    
    def __init__(self):
        """Initialize RG flow calculator."""
        # Reference scale (typically Z boson mass)
        self.M_Z = mp.mpf('91.1876')  # GeV
        
        # Planck scale
        self.M_Planck = mp.mpf('1.220910e19')  # GeV
        
        # Electroweak scale
        self.M_EW = mp.mpf('246.22')  # GeV (Higgs VEV)
        
        # GUT scale (typical)
        self.M_GUT = mp.mpf('2e16')  # GeV
    
    def beta_QED(self, alpha: mp.mpf, n_fermions: int = 3) -> mp.mpf:
        """
        QED beta function at one-loop.
        
        β(α) = dα/d(ln μ) = (2/3π) × n_f × α²
        
        Args:
            alpha: Fine-structure constant at current scale
            n_fermions: Number of active fermion families
        
        Returns:
            β(α) coefficient
        """
        beta = (mp.mpf(2) / (3 * mp.pi)) * mp.mpf(n_fermions) * alpha**2
        return beta
    
    def beta_QCD(self, alpha_s: mp.mpf, n_flavors: int = 6) -> mp.mpf:
        """
        QCD beta function at one-loop.
        
        β(α_s) = -(11 - (2/3)n_f) / (4π) × α_s²
        
        Args:
            alpha_s: Strong coupling constant
            n_flavors: Number of active quark flavors
        
        Returns:
            β(α_s) coefficient (negative for asymptotic freedom)
        """
        beta = -(11 - (mp.mpf(2)/3) * mp.mpf(n_flavors)) / (4 * mp.pi) * alpha_s**2
        return beta
    
    def run_coupling_QED(self, alpha_0: mp.mpf, mu_0: mp.mpf, mu: mp.mpf,
                         n_fermions: int = 3) -> mp.mpf:
        """
        Run QED coupling from scale μ₀ to μ.
        
        α(μ) = α(μ₀) / [1 - β·α(μ₀)·ln(μ/μ₀)]
        
        where β = (2n_f)/(3π) at one-loop
        
        Args:
            alpha_0: α at reference scale μ₀
            mu_0: Reference scale (GeV)
            mu: Target scale (GeV)
            n_fermions: Number of active fermions
        
        Returns:
            α(μ) at target scale
        """
        # Beta function coefficient
        beta_coeff = (2 * mp.mpf(n_fermions)) / (3 * mp.pi)
        
        # Logarithmic ratio
        log_ratio = mp.log(mu / mu_0)
        
        # Running formula
        denominator = 1 - beta_coeff * alpha_0 * log_ratio
        alpha_mu = alpha_0 / denominator
        
        return alpha_mu
    
    def run_coupling_QCD(self, alpha_s_0: mp.mpf, mu_0: mp.mpf, mu: mp.mpf,
                         n_flavors: int = 6) -> mp.mpf:
        """
        Run QCD coupling from scale μ₀ to μ.
        
        α_s(μ) = α_s(μ₀) / [1 + β₀·α_s(μ₀)·ln(μ/μ₀)]
        
        where β₀ = (11 - (2/3)n_f) / (4π) at one-loop
        
        Args:
            alpha_s_0: α_s at reference scale μ₀
            mu_0: Reference scale (GeV)
            mu: Target scale (GeV)
            n_flavors: Number of active quark flavors
        
        Returns:
            α_s(μ) at target scale
        """
        # Beta function coefficient (note: positive in denominator for asymptotic freedom)
        beta_0 = (11 - (mp.mpf(2)/3) * mp.mpf(n_flavors)) / (4 * mp.pi)
        
        # Logarithmic ratio
        log_ratio = mp.log(mu / mu_0)
        
        # Running formula (note: + sign for asymptotic freedom)
        denominator = 1 + beta_0 * alpha_s_0 * log_ratio
        alpha_s_mu = alpha_s_0 / denominator
        
        return alpha_s_mu
    
    def irh_geometric_alpha(self) -> Tuple[mp.mpf, Dict]:
        """
        Compute "bare" geometric α from IRH theory at Planck scale.
        
        This is the α value that emerges purely from topology,
        before RG running.
        
        Returns:
            (α_geometric, metadata)
        """
        # Hopf fibration volume ratio
        # Vol(S^7)/Vol(S^3) = (π⁴/3)/(2π²) = π²/6
        hopf_ratio = mp.pi**2 / 6
        
        # 24-cell vertices
        n_vertices = mp.mpf(24)
        
        # Metric mismatch
        eta = mp.mpf(4) / mp.pi
        
        # Weyl anomaly at Planck scale
        a_weyl = mp.mpf(5) / (16 * mp.pi**2)
        
        # Combine
        alpha_inv_geometric = hopf_ratio * n_vertices * (1 + eta * a_weyl)
        alpha_geometric = 1 / alpha_inv_geometric
        
        metadata = {
            'hopf_ratio': float(hopf_ratio),
            'n_vertices': float(n_vertices),
            'eta': float(eta),
            'a_weyl': float(a_weyl),
            'alpha_inv': float(alpha_inv_geometric),
            'scale': 'Planck scale (topological)',
            'derivation': 'Pure geometry, no QFT corrections'
        }
        
        return alpha_geometric, metadata
    
    def irh_weyl_correction(self, Q: mp.mpf) -> mp.mpf:
        """
        Weyl anomaly correction to α at scale Q.
        
        The Weyl anomaly provides an additional logarithmic correction
        beyond standard QED running.
        
        Δα⁻¹(Q) = -(β_weyl/12π) × ln(Q²/M_Pl²)
        
        where β_weyl depends on the conformal anomaly coefficient.
        
        Args:
            Q: Energy scale (GeV)
        
        Returns:
            Weyl correction to α⁻¹
        """
        # Weyl anomaly beta coefficient
        # For N=4 strands: β_weyl ~ a_weyl = 5/(16π²)
        beta_weyl = mp.mpf(5) / (16 * mp.pi**2)
        
        # Logarithmic correction
        log_correction = mp.log(Q**2 / self.M_Planck**2)
        
        # Weyl contribution to α⁻¹
        delta_alpha_inv = -(beta_weyl / (12 * mp.pi)) * log_correction
        
        return delta_alpha_inv
    
    def alpha_with_irh_corrections(self, Q: mp.mpf) -> Tuple[mp.mpf, Dict]:
        """
        Compute α(Q) including both QED running and IRH Weyl corrections.
        
        α⁻¹(Q) = α⁻¹_geom + QED_running + Weyl_correction
        
        Args:
            Q: Energy scale (GeV)
        
        Returns:
            (α(Q), detailed_components)
        """
        # Step 1: Geometric bare value at Planck scale
        alpha_geom, geom_meta = self.irh_geometric_alpha()
        alpha_inv_geom = 1 / alpha_geom
        
        # Step 2: QED running from Planck to Q
        alpha_Q_QED = self.run_coupling_QED(alpha_geom, self.M_Planck, Q, n_fermions=3)
        alpha_inv_QED = 1 / alpha_Q_QED
        
        # Step 3: Weyl anomaly correction
        delta_alpha_inv_weyl = self.irh_weyl_correction(Q)
        
        # Step 4: Combine corrections
        alpha_inv_total = alpha_inv_geom + (alpha_inv_QED - alpha_inv_geom) + delta_alpha_inv_weyl
        alpha_total = 1 / alpha_inv_total
        
        components = {
            'Q_GeV': float(Q),
            'alpha_geometric': float(alpha_geom),
            'alpha_inv_geometric': float(alpha_inv_geom),
            'alpha_inv_QED_running': float(alpha_inv_QED),
            'delta_alpha_inv_weyl': float(delta_alpha_inv_weyl),
            'alpha_inv_total': float(alpha_inv_total),
            'alpha_total': float(alpha_total),
            'QED_contribution': float(alpha_inv_QED - alpha_inv_geom),
            'Weyl_contribution': float(delta_alpha_inv_weyl),
            'metadata': geom_meta
        }
        
        return alpha_total, components
    
    def compute_alpha_at_standard_scales(self) -> Dict:
        """
        Compute α at experimentally relevant energy scales.
        
        Returns:
            Dictionary with α values at key scales
        """
        results = {}
        
        # Standard scales to evaluate
        scales = {
            'Low energy (me)': mp.mpf('0.000511'),  # Electron mass
            'Z boson mass': self.M_Z,
            'Top quark mass': mp.mpf('172.76'),
            'Electroweak scale': self.M_EW,
            'GUT scale': self.M_GUT,
            'Planck scale': self.M_Planck
        }
        
        for name, Q in scales.items():
            alpha_Q, components = self.alpha_with_irh_corrections(Q)
            results[name] = {
                'Q_GeV': float(Q),
                'alpha': float(alpha_Q),
                'alpha_inv': float(1/alpha_Q),
                'components': components
            }
        
        return results


def plot_rg_flow(output_file: str = 'rg_flow_alpha.png'):
    """
    Plot RG flow of α from Planck scale to low energy.
    """
    rg = RGFlow()
    
    # Energy scale range (log scale from electron mass to Planck)
    Q_min = mp.log10(mp.mpf('0.000511'))  # Electron mass
    Q_max = mp.log10(rg.M_Planck)
    
    Q_range_log = np.linspace(float(Q_min), float(Q_max), 200)
    Q_range = [mp.mpf(10)**mp.mpf(q) for q in Q_range_log]
    
    # Compute α at each scale
    alpha_values = []
    alpha_inv_values = []
    
    print("Computing RG flow...")
    for i, Q in enumerate(Q_range):
        if i % 20 == 0:
            print(f"  {i+1}/{len(Q_range)}: Q = {float(Q):.2e} GeV")
        
        alpha_Q, _ = rg.alpha_with_irh_corrections(Q)
        alpha_values.append(float(alpha_Q))
        alpha_inv_values.append(float(1/alpha_Q))
    
    # Create figure
    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    # Plot 1: α vs energy scale
    ax1.semilogx(Q_range_log, alpha_values, 'b-', linewidth=2, label='α(Q) with IRH corrections')
    
    # Mark special scales
    ax1.axvline(np.log10(float(rg.M_Z)), color='r', linestyle='--', alpha=0.5, label='Z boson')
    ax1.axvline(np.log10(float(rg.M_EW)), color='g', linestyle='--', alpha=0.5, label='EW scale')
    ax1.axvline(np.log10(float(rg.M_GUT)), color='purple', linestyle='--', alpha=0.5, label='GUT scale')
    
    # Experimental value at MZ
    alpha_exp_MZ = 1/128.95  # PDG value
    ax1.axhline(alpha_exp_MZ, color='orange', linestyle=':', linewidth=2, label='α(MZ) experimental')
    
    ax1.set_xlabel('log₁₀(Q / GeV)', fontsize=12)
    ax1.set_ylabel('α(Q)', fontsize=12)
    ax1.set_title('Running of Fine-Structure Constant α(Q)', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: α⁻¹ vs energy scale (more linear behavior)
    ax2.plot(Q_range_log, alpha_inv_values, 'b-', linewidth=2, label='α⁻¹(Q) with IRH corrections')
    
    # Mark special scales
    ax2.axvline(np.log10(float(rg.M_Z)), color='r', linestyle='--', alpha=0.5, label='Z boson')
    ax2.axvline(np.log10(float(rg.M_EW)), color='g', linestyle='--', alpha=0.5, label='EW scale')
    ax2.axvline(np.log10(float(rg.M_GUT)), color='purple', linestyle='--', alpha=0.5, label='GUT scale')
    
    # Experimental value at MZ
    alpha_inv_exp_MZ = 128.95
    ax2.axhline(alpha_inv_exp_MZ, color='orange', linestyle=':', linewidth=2, label='α⁻¹(MZ) experimental')
    
    ax2.set_xlabel('log₁₀(Q / GeV)', fontsize=12)
    ax2.set_ylabel('α⁻¹(Q)', fontsize=12)
    ax2.set_title('Running of Inverse Fine-Structure Constant α⁻¹(Q)', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to {output_file}")
    plt.close()


def print_rg_flow_report():
    """
    Print detailed report of RG flow at standard scales.
    """
    rg = RGFlow()
    
    print("=" * 80)
    print("IRH RENORMALIZATION GROUP FLOW REPORT")
    print("=" * 80)
    print()
    
    # Geometric bare value
    alpha_geom, geom_meta = rg.irh_geometric_alpha()
    print("BARE GEOMETRIC VALUE (Planck Scale)")
    print("-" * 80)
    print(f"α⁻¹_geometric = {float(1/alpha_geom):.10f}")
    print(f"α_geometric   = {float(alpha_geom):.10e}")
    print(f"Derivation: Hopf fibration + 24-cell + Weyl anomaly")
    print()
    
    # Values at standard scales
    print("RUNNING TO STANDARD SCALES")
    print("-" * 80)
    
    results = rg.compute_alpha_at_standard_scales()
    
    for name, data in results.items():
        print(f"\n{name}:")
        print(f"  Q = {data['Q_GeV']:.6e} GeV")
        print(f"  α(Q) = {data['alpha']:.10e}")
        print(f"  α⁻¹(Q) = {data['alpha_inv']:.10f}")
        
        if 'components' in data:
            comp = data['components']
            print(f"  QED contribution: {comp['QED_contribution']:+.10f}")
            print(f"  Weyl contribution: {comp['Weyl_contribution']:+.10f}")
    
    # Comparison with experiment at MZ
    print("\n" + "=" * 80)
    print("COMPARISON WITH EXPERIMENT AT MZ")
    print("=" * 80)
    
    alpha_inv_MZ_irh = results['Z boson mass']['alpha_inv']
    
    # Experimental values (PDG 2020)
    alpha_inv_MZ_exp = 128.95
    
    print(f"\nIRH prediction:  α⁻¹(MZ) = {alpha_inv_MZ_irh:.10f}")
    print(f"Experimental:    α⁻¹(MZ) = {alpha_inv_MZ_exp:.10f}")
    print(f"Relative error:  {abs(alpha_inv_MZ_irh - alpha_inv_MZ_exp)/alpha_inv_MZ_exp * 100:.4f}%")
    
    print("\n" + "=" * 80)


if __name__ == '__main__':
    # Print RG flow report
    print_rg_flow_report()
    
    # Generate plot
    plot_rg_flow()
    
    # Export results to JSON
    import json
    
    rg = RGFlow()
    results = rg.compute_alpha_at_standard_scales()
    
    # Convert mpmath to float for JSON
    def convert_for_json(obj):
        if isinstance(obj, dict):
            return {k: convert_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_for_json(item) for item in obj]
        elif isinstance(obj, mp.mpf):
            return float(obj)
        else:
            return obj
    
    json_results = convert_for_json(results)
    
    with open('rg_flow_results.json', 'w') as f:
        json.dump(json_results, f, indent=2)
    
    print("\nResults exported to rg_flow_results.json")
