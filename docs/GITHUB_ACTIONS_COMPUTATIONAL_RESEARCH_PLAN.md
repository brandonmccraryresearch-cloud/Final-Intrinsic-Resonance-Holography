# GitHub Actions Computational Research Plan

## Overview

This document provides a comprehensive research plan for using GitHub Actions workflows to run full-scale computational validation of the **Intrinsic Resonance Holography (IRH)** theoretical framework. The goal is to create executable Python/Jupyter notebooks that correspond one-to-one with each section of the theoretical framework.

---

## 1. GitHub Actions Computational Capabilities

### 1.1 Runner Specifications

GitHub-hosted runners provide the following computational resources:

| Resource | Ubuntu Runner | Windows Runner | macOS Runner |
|----------|--------------|----------------|--------------|
| **vCPUs** | 4 cores | 4 cores | 3 cores (M1: 4) |
| **RAM** | 16 GB | 16 GB | 14 GB |
| **Storage** | 14 GB SSD | 14 GB SSD | 14 GB SSD |
| **Architecture** | x86_64 | x86_64 | ARM64 (M1) |

**For IRH computations**: Ubuntu runners are recommended due to:
- Best compatibility with scientific Python stack
- Fastest startup time
- Native support for NumPy, SciPy, SymPy acceleration

### 1.2 Job Time Limits

- **Default timeout**: 6 hours per job
- **Maximum configurable**: 72 hours (using `timeout-minutes`)
- **Free tier limits**: 
  - Public repos: Unlimited minutes
  - Private repos: 2,000 minutes/month (Pro), 3,000 minutes/month (Team)

### 1.3 Computational Libraries Available

GitHub Actions runners come with pre-installed:
- Python 3.9, 3.10, 3.11, 3.12
- pip, pipenv, poetry
- NumPy, SciPy (via apt)
- Miniconda/Anaconda (via setup action)

---

## 2. Anaconda/Miniconda Workflow Setup

### 2.1 Recommended Approach: `setup-miniconda` Action

The official `conda-incubator/setup-miniconda@v3` action provides:
- Full Anaconda ecosystem support
- Conda environment caching
- mamba solver for fast dependency resolution

### 2.2 Environment Configuration

Create a dedicated `environment.yml` for IRH computations:

```yaml
name: irh-compute
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - numpy>=1.24
  - scipy>=1.11
  - sympy>=1.12
  - matplotlib>=3.7
  - jupyter>=1.0
  - nbconvert>=7.0
  - pandas>=2.0
  - mpmath>=1.3        # Arbitrary precision arithmetic
  - numba>=0.57        # JIT compilation for performance
  - networkx>=3.1      # Graph theory for CRN simulations
  - scikit-learn>=1.3  # ML for pattern recognition
  - pip:
    - qutip>=5.0                 # Quantum toolbox for braid group calculations
    - spherical-functions>=2022.4.5  # Spherical harmonics (Hopf fibration)
```

### 2.3 Mamba Solver (Recommended)

Use `mamba` instead of `conda` for 10-100x faster dependency resolution:

```yaml
# Pin to a specific commit SHA for supply chain security
# Check https://github.com/conda-incubator/setup-miniconda/releases for latest
- uses: conda-incubator/setup-miniconda@a4260408e20b96e80095f42ff7f1a15b27dd94ca  # v3.1.0
  with:
    miniforge-version: "24.7.1-0"  # Pin to specific version
    activate-environment: irh-compute
    environment-file: environment.yml
    use-mamba: true
```

> **Security Note:** Always pin third-party GitHub Actions to immutable commit SHAs rather than version tags to protect against supply chain attacks. Verify the SHA corresponds to a trusted release.

---

## 3. Network Access and Firewall Configuration

### 3.1 Default Network Access

GitHub Actions runners have:
- **Full outbound internet access** by default
- No firewall restrictions for package downloads
- Access to PyPI, conda-forge, GitHub, etc.

### 3.2 Enabling Enhanced Network Access (Copilot Agent Sessions)

When running computations via GitHub Copilot Coding Agent sessions:

**Option to Enable**: In your repository settings:
1. Go to **Settings** → **Copilot** → **Policies**
2. Enable **"Allow Copilot to access external network resources"**

This allows the agent to:
- Download packages from PyPI/conda-forge
- Fetch external data
- Access web APIs

### 3.3 Self-Hosted Runners (For Heavier Computation)

For computations exceeding 6 hours or requiring more resources:

```yaml
runs-on: [self-hosted, linux, x64]
```

Self-hosted runners allow:
- Custom hardware (GPUs, high RAM)
- Persistent environment caching
- No time limits

---

## 4. Workflow Configuration for IRH Computations

### 4.1 Complete Workflow File

The workflow file `.github/workflows/irh-compute.yml` provides:

1. **Trigger Options**:
   - `workflow_dispatch`: Manual trigger with parameters
   - `push`: Automatic on code changes
   - `schedule`: Periodic validation runs

2. **Matrix Strategy** for parallel execution:
   - Run multiple notebook sections simultaneously
   - Test across Python versions

3. **Artifact Management**:
   - Save computed outputs
   - Generate downloadable reports
   - Cache environments for speed

### 4.2 Key Workflow Features

```yaml
# Enable manual triggering with inputs
on:
  workflow_dispatch:
    inputs:
      section:
        description: 'Theory section to compute (1-6, or "all")'
        required: true
        default: 'all'
```

---

## 5. Notebook Structure for IRH Theory Validation

### 5.1 One-to-One Correlation Requirement

Each notebook must:
1. Clearly reference the exact equation from IRHv25/v26
2. Implement the mathematical computation
3. Display both symbolic and numerical results
4. Validate against expected values
5. Include inline LaTeX matching the theory

### 5.2 Proposed Notebook Structure

| Notebook | Theory Section | Key Computations |
|----------|---------------|------------------|
| `01_substrate_foundation.ipynb` | Section 1: Ontological Foundation | 4-strand stability, N=4 derivation |
| `02_harmony_functional.ipynb` | Section 2: Mathematical Engine | α derivation, metric mismatch η=4/π |
| `03_particle_sector.ipynb` | Section 3: Harmonic Crystallization | Higgs VEV, Koide formula |
| `04_cosmology.ipynb` | Section 4: Holographic Hum | Λ derivation, dark matter ratio |
| `05_gauge_sector.ipynb` | Section 5: Coherence Connections | SU(3)×SU(2)×U(1) emergence |
| `06_validation_suite.ipynb` | Section 6: Computational Validation | Tier 1-3 protocols |
| `07_appendices.ipynb` | Appendices A-E | Formal derivations |

### 5.3 Notebook Template Structure

Each notebook follows:

```python
# Cell 1: Theory Reference
"""
## [Section X]: [Title]
### Corresponding IRH v26.0 Reference: [Exact Section]

**Equation being validated:**
$$
[LaTeX equation from theory]
$$
"""

# Cell 2: Imports and Setup
import numpy as np
from sympy import *
# ...

# Cell 3: Symbolic Derivation
# Reproduce the mathematical derivation step-by-step

# Cell 4: Numerical Computation
# Calculate numerical values

# Cell 5: Validation
# Compare to known values and theory predictions

# Cell 6: Visualization
# Plot results with annotations

# Cell 7: Output Summary
# Structured output for paper inclusion
```

---

## 6. Options to Enable for Full Functionality

### 6.1 Repository Settings

| Setting | Location | Purpose |
|---------|----------|---------|
| **Actions enabled** | Settings → Actions | Required for workflows |
| **Workflow permissions** | Settings → Actions → General | Set to "Read and write" |
| **Copilot network access** | Settings → Copilot | Enable external network |
| **Artifact retention** | Settings → Actions → General | Set to 90 days |

### 6.2 Workflow Permissions (in `yml`)

```yaml
permissions:
  contents: write          # Write results back to repo
  actions: read            # Access artifacts
  pull-requests: write     # Update PRs with results
```

### 6.3 Environment Variables

```yaml
env:
  PYTHONUNBUFFERED: "1"           # Real-time output
  NUMBA_CACHE_DIR: "${{ github.workspace }}/.numba_cache"
  MPLBACKEND: "Agg"               # Non-interactive matplotlib
```

---

## 7. Execution Strategy

### 7.1 Initial Setup (One-time)

1. ✅ Create `.github/workflows/irh-compute.yml`
2. ✅ Create `environment.yml` with dependencies
3. Create initial notebook templates
4. Test workflow manually

### 7.2 Iterative Development

For each theory section:
1. Create/update the corresponding notebook
2. Run workflow with `section` input
3. Review outputs and artifacts
4. Validate against theory
5. Iterate until numerical agreement

### 7.3 Final Integration

1. Run full validation suite (`section: all`)
2. Generate comprehensive report
3. Embed notebook outputs in final paper
4. Archive all artifacts

---

## 8. Monitoring and Debugging

### 8.1 Workflow Monitoring

- Use **Actions tab** to monitor job progress
- Enable **debug logging** via repository secrets:
  - `ACTIONS_STEP_DEBUG: true`
  - `ACTIONS_RUNNER_DEBUG: true`

### 8.2 Artifact Downloads

Computed outputs are saved as downloadable artifacts:
- Executed notebooks with outputs
- Generated plots (PNG/PDF)
- Numerical results (CSV/JSON)
- Validation reports

### 8.3 Caching Strategy

The workflow caches:
- Conda environments (~2-5 min saved per run)
- Numba JIT compilations
- Downloaded packages

---

## 9. Advanced Features

### 9.1 GPU Acceleration (Optional)

For intensive numerical work, enable CUDA:

```yaml
runs-on: ubuntu-latest
steps:
  # Pin to commit SHA for supply chain security
  # Verify SHA at https://github.com/Jimver/cuda-toolkit/releases
  - uses: Jimver/cuda-toolkit@dc581bfeb6c52f0c3484b7d63c2ba4297bea8af0  # v0.2.11
    with:
      cuda: '12.1.0'
```

> **Security Note:** Third-party actions with write permissions pose supply chain risks. Pin to commit SHAs and verify the downloaded CUDA artifacts. Consider using official NVIDIA actions or manual installation for production workflows.

### 9.2 Parallel Notebook Execution

Matrix strategy for parallel runs:

```yaml
strategy:
  matrix:
    notebook:
      - 01_substrate_foundation
      - 02_harmony_functional
      - 03_particle_sector
```

### 9.3 Scheduled Validation

Run periodic validation to catch regressions:

```yaml
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
```

---

## 10. Summary Checklist

### Before First Run
- [ ] Enable GitHub Actions for repository
- [ ] Set workflow permissions to "Read and write"
- [ ] Enable Copilot network access (if using agent)
- [ ] Create `environment.yml`
- [ ] Create workflow file

### For Each Computation Session
- [ ] Select theory section to compute
- [ ] Trigger workflow manually or via push
- [ ] Monitor job progress in Actions tab
- [ ] Download artifacts when complete
- [ ] Validate results against theory

### Integration Requirements
- [ ] Each notebook references exact equations
- [ ] Outputs match expected precision
- [ ] Plots are publication-ready
- [ ] Validation passes Tier 1-3 protocols

---

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [setup-miniconda Action](https://github.com/conda-incubator/setup-miniconda)
- [GitHub Runner Specifications](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
