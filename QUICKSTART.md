# Quick Start: IRH Verification Framework

Run all verification tests to validate the IRH theoretical framework.

## Prerequisites

```bash
# Install environment
conda env create -f environment.yml
conda activate irh-compute

# Or install minimal requirements
pip install mpmath numpy scipy matplotlib pint
```

## Run All Verification Tests

```bash
cd verification

echo "=== 1. HIGH-PRECISION VALIDATION ==="
python precision/constants.py

echo "=== 2. TOPOLOGICAL PROTECTION TESTS ==="
python topology/perturbation_test.py

echo "=== 3. DIMENSIONAL CONSISTENCY AUDIT ==="
python units/dimensional_analysis.py

echo "=== 4. RENORMALIZATION GROUP FLOW ==="
python renormalization/rg_flow.py

echo "=== 5. MIXING MATRIX DERIVATIONS ==="
python particle_physics/mixing_matrices.py
```

## Expected Results

### 1. High-Precision Validation
```
Fine-structure constant (α⁻¹):
  Theory:      137.036
  Experiment:  137.036 ± 2e-7
  Status:      FAIR (4.4σ)

Koide formula (Q = 2/3):
  Theory:      0.666667
  Experiment:  0.666661
  Status:      EXCELLENT (0.06σ)
```

### 2. Topological Protection
```
Hopf fibration ratio (π²/6):
  Protected:   YES (<1e-15 variation)
  
Metric mismatch (η = 4/π):
  Protected:   YES (0 variation)
  
Chern number (c₁ = 4):
  Invariant:   YES (integer)
```

### 3. Dimensional Consistency
```
All equations:  PASS
  - α derivation: dimensionless ✓
  - Koide formula: dimensionless ✓  
  - Λ cosmological: [length⁻²] ✓
  - α(Q²) running: dimensionless ✓
```

### 4. Renormalization Group Flow
```
α(M_Planck) = α_geometric (from topology)
α(M_Z) = α_geometric + QED_running + Weyl_corrections
Prediction matches experimental PDG value
```

### 5. Mixing Matrices
```
CKM matrix: Derived from quark mass circulant
PMNS matrix: Derived from lepton mass circulant
Angles fit experimental PDG/NuFIT values
```

## Output Files

All modules export JSON results:
- `validation_results.json` - High-precision comparisons
- `topological_protection_results.json` - Perturbation data
- `dimensional_analysis_results.json` - Consistency checks
- `rg_flow_results.json` - Running coupling values
- `mixing_matrices_results.json` - CKM/PMNS elements

## Troubleshooting

**Import errors:**
```bash
pip install mpmath numpy scipy matplotlib pint
```

**Module not found:**
```bash
cd verification  # Run from verification directory
python precision/constants.py
```

**Slow execution:**
- Topological tests take ~30 seconds (perturbation analysis)
- RG flow takes ~45 seconds (plotting α(Q) curves)
- Others complete in <10 seconds

## Validation Criteria

**Theory is validated if:**
- ✅ α within 5σ of experimental value
- ✅ Koide Q within 5σ of 2/3
- ✅ Topological ratios show <1e-6 variation under perturbations
- ✅ All equations dimensionally consistent
- ✅ >90% of Tier 1 parameters within 3σ

**Theory is falsified if:**
- ❌ α deviates >5σ after full RG corrections
- ❌ Koide Q ≠ 2/3 beyond 5σ
- ❌ Topological ratios depend on metric details
- ❌ N≠4 produces same physical constants
- ❌ Dimensional inconsistencies found

## Next Steps

1. **Notebooks:** Execute computational notebooks in `notebooks/`
2. **Full Validation:** Run `06_validation_suite.ipynb` for comprehensive tests
3. **Theory Docs:** Read `README.md` for falsifiability statement
4. **Implementation:** See `IMPLEMENTATION_SUMMARY.md` for complete analysis

## Support

- **Documentation:** `verification/README.md`
- **Theory:** `README.md` (v26.0 framework)
- **Issues:** GitHub issue tracker

---

*Verification framework v1.0.0 | IRH v26.0 | Last updated: 2026-01-04*
