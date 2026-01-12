# IRH Verification Framework

This directory contains high-precision verification and validation modules for the Intrinsic Resonance Holography (IRH) theoretical framework.

## Purpose

The verification framework ensures that IRH predictions meet the rigorous standards of formal theoretical physics by:

1. **Arbitrary-precision calculations** (15+ decimal places) for all fundamental constants
2. **Topological protection analysis** to demonstrate that results are not fine-tuned
3. **Dimensional consistency auditing** for all equations bridging geometry to physics
4. **Renormalization group flow** with Weyl anomaly corrections
5. **Mixing matrix derivations** from circulant/braid group structure

## Modules

### 1. `precision/constants.py`

High-precision calculations using `mpmath` with 50 decimal places.

**Features:**
- Fine-structure constant α to 15+ decimals: geometric base + radiative corrections
- Includes QED vacuum polarization and Weyl anomaly contributions
- Koide formula Q = 2/3 calculation and validation
- Cosmological constant suppression factors
- Comparison with CODATA 2018/2022 experimental values
- Statistical significance testing (σ-deviations)

**Usage:**
```bash
python precision/constants.py
```

**Output:**
- Console: Validation report with theory vs experiment comparison
- File: `validation_results.json`

### 2. `topology/perturbation_test.py`

Topological protection analysis via strand geometry perturbations.

**Features:**
- Tests that Vol(S⁷)/Vol(S³) = π²/6 is truly topological (invariant)
- Verifies η = 4/π stability under metric perturbations
- Demonstrates Chern number c₁(CP³) = 4 is an integer invariant
- Analyzes fine-structure constant sensitivity to curvature changes
- Tests N≠4 strand configurations (should fail)

**Usage:**
```bash
python topology/perturbation_test.py
```

**Output:**
- Console: Test suite results with protection status
- Files: `topological_protection_results.json`, perturbation plots
- Figures: `hopf_stability.png`, `eta_stability.png`, `alpha_sensitivity.png`

### 3. `units/dimensional_analysis.py`

Automated dimensional consistency auditing using `pint`.

**Features:**
- Verifies α derivation is dimensionless throughout
- Checks Koide formula dimensional consistency
- Audits cosmological constant Λ dimensions [length⁻²]
- Validates running coupling α(Q²) remains dimensionless
- Analyzes geometric-to-physical bridge for unit consistency

**Usage:**
```bash
python units/dimensional_analysis.py
```

**Output:**
- Console: Dimensional audit report with pass/fail for each equation
- File: `dimensional_analysis_results.json`

### 4. `renormalization/rg_flow.py`

Renormalization group flow with IRH Weyl anomaly corrections.

**Features:**
- Computes "bare" geometric α at Planck scale from topology
- Runs α from M_Planck to low energy scales using QED beta function
- Adds Weyl anomaly logarithmic corrections: Δα⁻¹ ~ ln(Q²/M_Pl²)
- Compares α(M_Z) prediction with experimental value
- Visualizes RG flow from electron mass to Planck scale

**Usage:**
```bash
python renormalization/rg_flow.py
```

**Output:**
- Console: RG flow report at standard energy scales
- File: `rg_flow_results.json`
- Figure: `rg_flow_alpha.png` (α(Q) and α⁻¹(Q) vs log₁₀(Q))

### 5. `particle_physics/mixing_matrices.py`

CKM and PMNS mixing matrix derivations from circulant eigenstructure.

**Features:**
- Derives CKM matrix from quark mass circulant matrix
- Derives PMNS matrix from lepton mass circulant matrix
- Fits standard parametrization angles to experimental values
- Compares theoretical predictions with PDG/NuFIT measurements
- Demonstrates geometric origin of flavor mixing

**Usage:**
```bash
python particle_physics/mixing_matrices.py
```

**Output:**
- Console: CKM and PMNS matrix comparisons
- File: `mixing_matrices_results.json`

## Dependencies

All modules require the packages specified in `environment.yml`:

```yaml
- python=3.11
- numpy>=1.24
- scipy>=1.11
- mpmath>=1.3
- sympy>=1.12
- matplotlib>=3.7
- pint>=0.23  # For dimensional analysis
```

Install with:
```bash
conda env create -f ../environment.yml
conda activate irh-compute
```

## Running the Full Verification Suite

To run all verification modules sequentially:

```bash
cd verification

echo "=== HIGH-PRECISION VALIDATION ==="
python precision/constants.py

echo "=== TOPOLOGICAL PROTECTION ANALYSIS ==="
python topology/perturbation_test.py

echo "=== DIMENSIONAL CONSISTENCY AUDIT ==="
python units/dimensional_analysis.py

echo "=== RENORMALIZATION GROUP FLOW ==="
python renormalization/rg_flow.py

echo "=== MIXING MATRIX DERIVATIONS ==="
python particle_physics/mixing_matrices.py
```

Or use the provided script (if created):
```bash
./run_verification_suite.sh
```

## Integration with Notebooks

The verification modules are designed to be imported into Jupyter notebooks:

```python
# In notebook Cell 5: Validation
from verification.precision.constants import validate_all_predictions, compare_with_experiment

results = validate_all_predictions()
print(f"α agreement: {results['alpha']['agreement_status']}")
print(f"σ deviation: {results['alpha']['sigma_deviation']:.2f}σ")
```

## Falsifiability Criteria

See the main README.md for the complete falsifiability statement. Key criteria:

1. **α deviation:** >5σ from geometric prediction (after RG running) invalidates theory
2. **Koide formula:** Q ≠ 2/3 beyond 5σ falsifies circulant structure
3. **Topological invariance:** If ratios depend on metric details, topology claim fails
4. **N=4 uniqueness:** Other N values must not reproduce Standard Model
5. **Mixing matrices:** >10% error in CKM/PMNS angles from circulant structure

## Output Files

All verification modules export JSON results for further analysis:

- `validation_results.json` - High-precision constant comparisons
- `topological_protection_results.json` - Perturbation test data
- `dimensional_analysis_results.json` - Dimensional consistency checks
- `rg_flow_results.json` - Running coupling values at standard scales
- `mixing_matrices_results.json` - CKM/PMNS matrix elements

## Visualization

Generated figures are saved to `outputs/figures/` (if directory exists):

- `hopf_stability.png` - Hopf fibration ratio invariance
- `eta_stability.png` - Metric mismatch η = 4/π stability
- `alpha_sensitivity.png` - α sensitivity to curvature perturbations
- `rg_flow_alpha.png` - Running of α from Planck to low energy

## Precision Standards

All calculations meet publication-quality precision requirements:

- **Symbolic derivations:** Exact (using SymPy)
- **Numerical computations:** 50 decimal places (mpmath)
- **Final results:** Reported to 15 decimal places minimum
- **Comparisons:** Include experimental uncertainties from CODATA/PDG
- **Statistical tests:** χ², σ-deviations, confidence intervals

## Contributing

When adding new verification modules:

1. Follow the existing structure (standalone executable + importable functions)
2. Include docstrings with mathematical equations
3. Export results to JSON for reproducibility
4. Generate publication-ready visualizations
5. Document precision requirements and sources
6. Add tests to validation suite

## References

- **CODATA 2018:** Fundamental physical constants (NIST)
- **PDG 2020:** Particle Data Group review
- **NuFIT 5.0:** Neutrino oscillation global fit
- **Planck 2018:** Cosmological parameters

## License

Same as parent repository (see LICENSE file).

---

*Verification framework version 1.0.0*  
*Last updated: 2026-01-04*
