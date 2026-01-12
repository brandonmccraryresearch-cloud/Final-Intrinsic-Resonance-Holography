# Using the Gen AI Evolution Workflow

## Purpose

The `evolution-with-genai.yml` workflow demonstrates how to use the `GOOGLE_CLOUD_API_KEY` secret you set up in GitHub Actions to run theory evolution cycles with AI-powered suggestions.

## Setup

### 1. Add the API Key Secret

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `GOOGLE_CLOUD_API_KEY`
5. Value: Paste your Google Cloud API key
6. Click **Add secret**

### 2. Enable the Workflow

The workflow is already in `.github/workflows/evolution-with-genai.yml` and ready to use.

## Running the Workflow

### Manual Trigger

1. Go to the **Actions** tab in your repository
2. Select **IRH Theory Evolution with Gen AI** from the left sidebar
3. Click **Run workflow** button
4. Configure options:
   - **max_refinements**: Number of refinements to test (default: 5)
   - **use_genai**: Enable/disable Gen AI suggestions (default: true)
5. Click **Run workflow**

### Automatic Schedule

The workflow runs automatically every Sunday at midnight UTC.

## What It Does

The workflow will:

1. ✅ Install all dependencies including google-genai
2. ✅ Verify the API key is accessible
3. ✅ Run complete evolution cycle:
   - Compute theoretical predictions
   - Validate against experimental data
   - Analyze error patterns
   - Generate template-based suggestions
   - **Generate AI-enhanced suggestions using Gen AI SDK**
4. ✅ Export results to JSON
5. ✅ Upload results as artifact (90-day retention)
6. ✅ Display summary in job output

## Output

### JSON Results File

Download `evolution_cycle_results.json` from the workflow artifacts. It contains:

```json
{
  "timestamp": "2026-01-10T12:00:00",
  "predictions": {
    "total": 12,
    "excellent": 1,
    "good": 0,
    "fair": 2,
    "poor": 6
  },
  "error_patterns": {
    "total": 11,
    "patterns": [...]
  },
  "template_suggestions": {
    "count": 3,
    "suggestions": [...]
  },
  "genai_suggestions": {
    "used": true,
    "available": true,
    "text": "..."
  }
}
```

### Job Summary

View the summary table in the Actions job output showing:
- Total predictions
- Validation results (Excellent/Good/Fair/Poor)
- Number of error patterns found
- Number of suggestions generated
- Whether Gen AI was used

## Example Output

When the workflow runs with Gen AI enabled, you'll see output like:

```
======================================================================
IRH Theory Evolution Cycle with Gen AI
Started: 2026-01-10T12:00:00
======================================================================

Gen AI SDK requested: True
Gen AI SDK available: True

Step 1: Computing theoretical predictions...
✅ Computed 12 predictions

Step 2: Validating against experiments...
✅ Validation complete:
   Excellent: 1
   Good: 0
   Fair: 2
   Poor: 6

Step 3: Analyzing error patterns...
✅ Found 11 error patterns
   1. high: Gauge sector has elevated errors (mean σ = 1981.6)...
   2. high: Cosmology sector has elevated errors (mean σ = 5.9)...
   3. high: Fundamental sector has elevated errors (mean σ = 725741.9)...

Step 4: Generating template-based suggestions...
✅ Generated 3 template suggestions
   1. Chern Class C_2 Correction
      Confidence: high
      Priority: 151.0
   ...

Step 5: Generating Gen AI enhanced suggestions...
(This may take 30-60 seconds with HIGH thinking level)

✅ Gen AI suggestions received

======================================================================
AI-ENHANCED SUGGESTIONS
======================================================================

[AI-generated topological refinement suggestions appear here]

======================================================================
EVOLUTION CYCLE COMPLETE
======================================================================

Template suggestions: 3
Gen AI used: True
Status: SUCCESS
```

## Troubleshooting

### "API key not set" Warning

**Problem**: Workflow shows `⚠️ API key not set`

**Solution**: 
1. Check that you named the secret exactly `GOOGLE_CLOUD_API_KEY` (case-sensitive)
2. Verify the secret exists in Settings → Secrets and variables → Actions
3. Make sure you're running the workflow from the correct branch

### "Gen AI SDK not available"

**Problem**: Error about Gen AI not being available

**Solution**: This shouldn't happen as the workflow installs it. If it does:
1. Check the "Install dependencies" step succeeded
2. Verify `pip install --upgrade google-genai` ran without errors

### Rate Limiting / API Errors

**Problem**: Gen AI returns errors about rate limits or quota

**Solution**:
1. Check your Google Cloud project quotas
2. Ensure billing is enabled
3. Wait a few minutes and retry
4. The workflow will fall back to template suggestions automatically

### No AI Suggestions Generated

**Problem**: Gen AI step completes but no suggestions shown

**Solution**:
1. Check the workflow logs for error messages
2. Verify your API key has correct permissions
3. Try running with `use_genai: false` to verify template system works
4. The prompt may have returned empty - check Gen AI SDK status page

## Cost Considerations

Running this workflow with Gen AI will incur Google Cloud API costs:
- Typical cost: ~$0.01-0.10 per run (depends on model and usage)
- Weekly schedule: ~$0.50-5.00 per month
- Manual runs are additional

To minimize costs:
- Use `use_genai: false` for testing
- Reduce frequency of scheduled runs
- Review costs in Google Cloud Console

## Security

The API key is:
- ✅ Stored securely in GitHub Secrets (encrypted)
- ✅ Only accessible to workflows you authorize
- ✅ Never exposed in logs or outputs
- ✅ Injected at runtime via environment variable
- ✅ Not accessible to pull requests from forks (security feature)

## Further Reading

- [Gen AI SDK Setup Guide](../docs/GEN_AI_SDK_SETUP.md) - Complete documentation
- [Evolution System README](../evolution_system/README.md) - Module documentation
- [Example Script](../examples/genai_advisor_example.py) - Local testing

---

**Questions?** Open an issue or check the documentation.
