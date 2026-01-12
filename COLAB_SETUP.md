# Google Colab Setup Guide for IRHv57 Notebooks

This guide helps you run IRH computational notebooks in Google Colab with zero local setup.

---

## 🚀 Quick Start (3 steps)

### Step 1: Open Notebook in Colab

**Option A: Direct Upload**
1. Go to https://colab.research.google.com
2. Click **File → Upload notebook**
3. Navigate to `notebooks/` folder and select any `.ipynb` file

**Option B: From GitHub**
1. Go to https://colab.research.google.com
2. Click **File → Open notebook → GitHub**
3. Enter repository URL: `brandonmccraryresearch-cloud/Final-Intrinsic-Resonance-Holography`
4. Select branch: `main` (or your working branch)
5. Choose notebook from list

**Option C: Direct Link Pattern**
```
https://colab.research.google.com/github/brandonmccraryresearch-cloud/Final-Intrinsic-Resonance-Holography/blob/main/notebooks/01_d4_lattice_foundation.ipynb
```
Replace `01_d4_lattice_foundation.ipynb` with any notebook name.

### Step 2: Enable GPU/TPU (Optional but Recommended)

For faster computation, especially for Monte Carlo integrations:

1. Click **Runtime → Change runtime type**
2. Select **Hardware accelerator**: GPU or TPU
3. Click **Save**

**Note:** Most notebooks run fine on CPU. GPU helps with:
- Notebook 04 (10M Monte Carlo samples)
- Notebook 08 (comprehensive validation)

### Step 3: Run All Cells

1. Click **Runtime → Run all** (or press Ctrl+F9)
2. Wait for dependency installation (first cell, ~30 seconds)
3. Watch results appear sequentially

**Estimated run times:**
- Notebooks 01-03: ~2-5 minutes each
- Notebook 04: ~5-10 minutes (Monte Carlo)
- Notebooks 05-07: ~2-5 minutes each
- Notebook 08: ~10-15 minutes (full validation)

---

## 📦 Dependencies (Auto-Installed)

Each notebook includes this cell:
```python
try:
    import google.colab
    IN_COLAB = True
    !pip install -q mpmath numpy scipy matplotlib sympy
except:
    IN_COLAB = False
```

**What gets installed:**
- `mpmath` - Arbitrary precision arithmetic (50+ decimal places)
- `numpy` - Numerical arrays and operations
- `scipy` - Scientific computing and constants database
- `matplotlib` - Visualization and plotting
- `sympy` - Symbolic mathematics

**No additional setup required!**

---

## 📂 Saving Results

### Option 1: Download Figures

Right-click any generated figure → **Save image as...**

Figures are also available as PNG files in the notebook output:
- `01_d4_lattice_foundation.png`
- `02_continuum_emergence.png`
- etc.

### Option 2: Download to Google Drive

Add this cell to save outputs:
```python
from google.colab import drive
drive.mount('/content/drive')

# Save results to Drive
import shutil
shutil.copy('04_fine_structure_constant.png', '/content/drive/MyDrive/IRH_Results/')
```

### Option 3: Export Notebook with Outputs

1. Click **File → Download → Download .ipynb**
2. Or: **File → Save a copy in Drive**

---

## 🔍 Troubleshooting

### Issue 1: "Package installation failed"

**Solution:**
```python
# Run this cell first
!pip install --upgrade pip
!pip install mpmath numpy scipy matplotlib sympy --force-reinstall
```

### Issue 2: "Cell execution timeout"

**Cause:** Long computation (e.g., 10M Monte Carlo samples)

**Solution:**
- Use GPU runtime (faster)
- Or reduce `n_samples` in the code:
  ```python
  n_samples = 1000000  # Reduce from 10M to 1M for speed
  ```

### Issue 3: "Out of memory"

**Cause:** Large array allocations

**Solution:**
1. **Runtime → Factory reset runtime**
2. Enable GPU (more memory)
3. Run cells individually instead of "Run all"

### Issue 4: "ModuleNotFoundError: No module named 'mpmath'"

**Cause:** Skipped installation cell

**Solution:**
Run Cell 2 (Imports and Setup) explicitly:
```python
!pip install -q mpmath numpy scipy matplotlib sympy
import mpmath as mp
```

---

## ⚙️ Advanced Configuration

### Increase Precision

For higher accuracy calculations:
```python
import mpmath as mp
mp.dps = 100  # 100 decimal places instead of 50
```

**Warning:** Higher precision = slower computation

### Adjust Monte Carlo Samples

In Notebook 04:
```python
n_samples = 10000000  # Default: 10 million

# For faster testing:
n_samples = 100000    # 100k samples (~10x faster, less accurate)

# For publication quality:
n_samples = 100000000 # 100M samples (~10x slower, more accurate)
```

### Enable Verbose Output

Add to any computation cell:
```python
verbose = True
if verbose:
    print(f"Debug: variable_name = {variable_name}")
```

---

## 📊 Running Multiple Notebooks

### Sequential Execution

To run all 8 notebooks in order:

1. Open Notebook 01
2. **Runtime → Run all**
3. Wait for completion
4. Open Notebook 02
5. Repeat steps 2-4 for notebooks 03-08

### Parallel Execution

For faster validation (requires multiple Colab tabs):

1. Open 8 browser tabs
2. Load one notebook per tab (01-08)
3. Start "Run all" on each tab simultaneously
4. Download results from each tab when complete

**Note:** Free Colab limits concurrent notebooks. Consider Colab Pro for parallel runs.

---

## 💡 Best Practices

### Before Running

1. **Read Cell 1 (Markdown)** - Understand theory being tested
2. **Check runtime type** - Use GPU for compute-heavy notebooks
3. **Clear all outputs** - **Edit → Clear all outputs** for clean start

### During Execution

1. **Monitor progress** - Watch print statements
2. **Check intermediate results** - Verify computations make sense
3. **Don't interrupt** - Let Monte Carlo complete

### After Completion

1. **Review validation results** - Check "PASS ✓" or "FAIL ✗"
2. **Examine figures** - Visual confirmation of derivations
3. **Read summary** - Cell 7 provides key takeaways
4. **Compare to IRHv57.md** - Cross-reference theory document

---

## 🎯 Validation Checklist

For each notebook, verify:

- [ ] All cells executed without errors
- [ ] Dependencies installed successfully
- [ ] Theoretical values derived (not hardcoded)
- [ ] Validation shows "PASS ✓"
- [ ] Experimental values labeled "FOR VALIDATION ONLY"
- [ ] Figures generated and saved
- [ ] Summary matches expectations from IRHv57.md

---

## 📝 Example Session

**Goal:** Validate fine-structure constant derivation

**Steps:**
1. Open: `04_fine_structure_constant.ipynb`
2. Runtime: Change to GPU
3. Execute: Run all cells
4. Wait: ~5-10 minutes
5. Results:
   - G(0) = 0.04597 (Watson integral)
   - α⁻¹_bare = 136.68 (bare coupling)
   - α⁻¹_phys = 137.03 (physical + screening)
   - Deviation: 0.004% from CODATA
   - Validation: PASS ✓
6. Download: `04_fine_structure_constant.png`
7. Conclusion: α derived from D₄ topology!

---

## 🔗 Helpful Links

- **Colab Homepage**: https://colab.research.google.com
- **Colab FAQ**: https://research.google.com/colaboratory/faq.html
- **GitHub Repo**: https://github.com/brandonmccraryresearch-cloud/Final-Intrinsic-Resonance-Holography
- **Theory Document**: [IRHv57.md](IRHv57.md)
- **Notebook Guide**: [notebooks/README_NOTEBOOKS.md](notebooks/README_NOTEBOOKS.md)

---

## 🆘 Support

If you encounter issues:

1. **Check this guide** - Most common issues covered above
2. **Review notebook README** - [notebooks/README_NOTEBOOKS.md](notebooks/README_NOTEBOOKS.md)
3. **Read theory document** - [IRHv57.md](IRHv57.md) for context
4. **Open GitHub issue** - Report bugs or unexpected behavior
5. **Check compliance** - Run `scripts/check_directive_compliance.py` locally

---

## ✅ Success Criteria

You've successfully run IRHv57 notebooks when:

- ✅ All 8 notebooks execute without errors
- ✅ Theoretical predictions derived (not fitted)
- ✅ Validations pass (>90% within 3σ)
- ✅ Figures visualize key results
- ✅ No hardcoded experimental values as inputs
- ✅ Statistical analysis confirms accuracy

**Congratulations! You've validated IRH v57.0 theory computationally.**

---

*Last updated: January 12, 2026*  
*IRH v57.0 - The Definitive Axiomatic Synthesis*
