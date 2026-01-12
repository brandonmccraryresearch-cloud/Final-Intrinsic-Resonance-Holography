# Quick Start: Gemini 3 Pro Integration for IRH

Get started with AI-powered theory examination and refinement in 5 minutes.

## Step 1: Install Dependencies

```bash
pip install google-genai
```

Or use the full environment:

```bash
conda env create -f environment.yml
conda activate irh-compute
```

## Step 2: Get API Key

1. Visit https://aistudio.google.com/app/apikey
2. Create a new API key
3. Copy the key

## Step 3: Set Environment Variable

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**Permanent (add to ~/.bashrc or ~/.zshrc):**
```bash
echo 'export GEMINI_API_KEY="your_key"' >> ~/.bashrc
source ~/.bashrc
```

## Step 4: Run Your First Analysis

### Option A: Simple Example

```bash
python examples/simple_gemini_example.py
```

This will:
- Connect to Gemini 3 Pro
- Analyze IRH's fine-structure constant derivation
- Show real-time streaming output
- Display code execution and results

**Expected output:**
```
======================================================================
GEMINI 3 PRO - IRH THEORY ANALYSIS
======================================================================

Generating response with HIGH thinking level...
This may take 30-90 seconds for deep reasoning.

======================================================================

## Analysis of Fine-Structure Constant Derivation

The Intrinsic Resonance Holography framework proposes deriving α 
from Hopf fibration volume ratios. Let me analyze this rigorously:

[... detailed analysis ...]

Response generation complete!
```

### Option B: Self-Examination (Recommended)

```bash
python scripts/gemini_theory_examiner.py --analysis-type self-examine
```

This will:
- Load your theory from README.md
- Perform critical self-examination
- Identify weaknesses and gaps
- Suggest specific improvements
- Save results to JSON file

**Expected output:**
```
======================================================================
IRH Theory Self-Examination with Gemini 3 Pro
======================================================================

🚀 Initializing Gemini 3 Pro...
✅ Gemini 3 Pro ready

📖 Loading theory from: README.md
✅ Loaded 43527 characters

🔍 Performing critical self-examination...
   (This may take 1-2 minutes with HIGH thinking level)

[... detailed examination ...]

✅ Analysis complete!
✅ Results saved to: gemini_analysis_results.json
```

## Step 5: Review Results

### View Results in Terminal

Results are displayed in real-time during generation.

### View Saved Results

```bash
# Pretty-print JSON results
python -m json.tool gemini_analysis_results.json

# Or use jq (if installed)
jq . gemini_analysis_results.json
```

### Results Structure

```json
{
  "timestamp": "2026-01-12T18:30:00.000Z",
  "theory_file": "README.md",
  "theory_length": 43527,
  "analysis_type": "self-examine",
  "status": "success",
  "results": {
    "self_examination": "... detailed analysis ..."
  }
}
```

## Common First-Time Issues

### ❌ "ImportError: No module named 'google'"

**Solution:**
```bash
pip install google-genai
```

### ❌ "API key not found"

**Solution:**
```bash
# Check if set
echo $GEMINI_API_KEY

# If empty, set it
export GEMINI_API_KEY="your_key"
```

### ❌ "Rate limit exceeded"

**Solution:**
- Wait 60 seconds and retry
- Check your quota at https://aistudio.google.com
- Free tier has limits; consider upgrading

### ❌ "Response takes too long"

**This is normal!** HIGH thinking level can take 30-90 seconds.
- Be patient
- Watch for streaming output
- Response will arrive

## Next Steps

### 1. Try Different Analysis Types

```bash
# Mathematical rigor check
python scripts/gemini_theory_examiner.py --analysis-type mathematical

# Physical content focus
python scripts/gemini_theory_examiner.py --analysis-type physical

# Internal consistency
python scripts/gemini_theory_examiner.py --analysis-type consistency

# Refinement suggestions
python scripts/gemini_theory_examiner.py --refinements
```

### 2. Use Python API

```python
from evolution_system import GeminiTheoryAdvisor

# Initialize
advisor = GeminiTheoryAdvisor()

# Load theory
with open('README.md', 'r') as f:
    theory = f.read()

# Analyze
result = advisor.self_examine(theory, ['hardcoded values'])
print(result)
```

### 3. Customize for Your Needs

Edit `examples/simple_gemini_example.py`:
- Change the prompt to ask different questions
- Adjust thinking level (LOW/MEDIUM/HIGH)
- Enable/disable tools (code execution, search)

### 4. Integrate into Workflow

```bash
# Add to your daily workflow
# 1. Make theory changes
# 2. Run self-examination
python scripts/gemini_theory_examiner.py --analysis-type self-examine

# 3. Address CRITICAL issues
# 4. Get refinements
python scripts/gemini_theory_examiner.py --refinements

# 5. Implement and test
# 6. Re-examine
```

## Performance Tips

1. **Start with MEDIUM thinking**: Test prompts quickly
2. **Use HIGH for final analysis**: When you need maximum rigor
3. **Limit text size**: Keep theory input <100k characters
4. **Save results**: Don't re-run unnecessarily
5. **Batch analyses**: Run multiple overnight

## Getting Help

### Documentation

- **Full Guide**: See `docs/GEMINI_INTEGRATION.md`
- **Examples**: See `examples/README.md`
- **API Reference**: Check docstrings in `evolution_system/gemini_integration.py`

### Troubleshooting

- **API Issues**: Check https://ai.google.dev/
- **Installation**: Verify `pip list | grep google-genai`
- **API Key**: Test at https://aistudio.google.com

### Support

- **GitHub Issues**: Open an issue for bugs
- **Discussions**: Ask questions in GitHub Discussions
- **Documentation**: Check docs/ directory

## Example Session

Complete example of a productive session:

```bash
# 1. Set up
export GEMINI_API_KEY="your_key"

# 2. Quick test
python examples/simple_gemini_example.py

# 3. Full self-examination
python scripts/gemini_theory_examiner.py \
    --analysis-type self-examine \
    --output self_exam_$(date +%Y%m%d).json

# 4. Review results
cat self_exam_*.json | jq '.results.self_examination' | less

# 5. Get refinements
python scripts/gemini_theory_examiner.py \
    --refinements \
    --output refinements_$(date +%Y%m%d).json

# 6. Review refinements
cat refinements_*.json | jq '.results.refinements' | less

# 7. Implement changes
# ... make code changes ...

# 8. Re-examine
python scripts/gemini_theory_examiner.py \
    --analysis-type consistency \
    --output consistency_check_$(date +%Y%m%d).json
```

## Success Criteria

You've successfully integrated Gemini when you can:

- ✅ Run `simple_gemini_example.py` without errors
- ✅ Get a streaming response from Gemini
- ✅ See code execution results (if applicable)
- ✅ Save results to JSON file
- ✅ Review analysis for actionable insights

## What's Next?

Now that you have Gemini working:

1. **Regular Self-Examination**: Run weekly on theory updates
2. **Pre-Publication Review**: Full battery of checks before sharing
3. **Refinement Cycles**: Implement suggestions iteratively
4. **Custom Analysis**: Develop domain-specific prompts
5. **Integration**: Add to CI/CD pipeline

---

**You're ready to use AI-powered theory refinement!**

For advanced usage, see [docs/GEMINI_INTEGRATION.md](docs/GEMINI_INTEGRATION.md)
