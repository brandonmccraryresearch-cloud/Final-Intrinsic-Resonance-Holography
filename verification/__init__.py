"""
IRH Verification Framework
==========================

High-precision verification and validation modules for the
Intrinsic Resonance Holography (IRH) theoretical framework.

Modules:
--------
- precision: Arbitrary-precision calculations and CODATA comparison
- topology: Topological protection and perturbation analysis
- units: Dimensional consistency auditing with pint
- renormalization: RG flow and running coupling constants
- particle_physics: CKM/PMNS mixing matrix derivations

Usage:
------
```python
from verification.precision import constants
from verification.topology import perturbation_test
from verification.units import dimensional_analysis
from verification.renormalization import rg_flow
from verification.particle_physics import mixing_matrices

# Run validation
results = constants.validate_all_predictions()
constants.print_validation_report()

# Test topological protection
topo_results = perturbation_test.run_all_tests()

# Dimensional audit
dim_results = dimensional_analysis.run_all_audits()

# RG flow
rg = rg_flow.RGFlow()
rg.print_rg_flow_report()

# Mixing matrices
mixing_matrices.compare_ckm_with_experiment()
```
"""

__version__ = "1.0.0"
__author__ = "IRH Computational Research Team"
__all__ = ['precision', 'topology', 'units', 'renormalization', 'particle_physics']
