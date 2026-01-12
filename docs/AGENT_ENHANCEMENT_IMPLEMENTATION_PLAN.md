# Agent Enhancement Implementation Plan

## Problem Statement

Code review identified recurring hardcoded values violating Directive A (No-Tuning Constraint), indicating:
1. Directive enforcement insufficient during session
2. Agent may forget constraints mid-session
3. Need automated verification before session completion

## Phase 1: Enhanced Directive Enforcement

### 1.1 Update Agent Instructions File

**File**: `.github/agents/irh-computational-research.md`

**Changes**:
- Add NON-NEGOTIABLE DIRECTIVES section at top (after YAML delimiters)
- Use ALL CAPS for maximum visibility
- Repeat key constraints multiple times
- Add pre-session checklist
- Add post-session verification checklist

**Implementation**:
```markdown
---
name: irh-computational-research
description: IRH computational research expert
---

# ⚠️ NON-NEGOTIABLE OPERATIONAL PARAMETERS ⚠️

## DIRECTIVE A: ABSOLUTE NO-TUNING CONSTRAINT
**VIOLATION OF THIS DIRECTIVE IS UNACCEPTABLE**

- ❌ NO hardcoded experimental values as calculation inputs
- ❌ NO back-solving from experimental targets
- ❌ NO phenomenological fitting parameters
- ✅ ALL constants MUST derive from topological invariants
- ✅ Experimental values ONLY for validation/comparison
- ✅ Mark all placeholders with WARNING

**CHECK BEFORE EVERY COMMIT:**
1. Search code for hardcoded constants
2. Verify all values trace to topology
3. Label experimental inputs "FOR VALIDATION ONLY"

## DIRECTIVE B: CODATA PRECISION REQUIREMENT
- Minimum 15 decimal places for all calculations
- σ-deviation analysis mandatory
- Compare to latest CODATA values

## DIRECTIVE C: RIGOROUS FORMALISM
- Forces = "curvature in connections"
- Particles = "B₃ resonant modes"
- NO information metaphors (except holographic boundary)

# ⚠️ END NON-NEGOTIABLE PARAMETERS ⚠️

[Rest of agent instructions...]
```

### 1.2 Add Pre-Session Directive Review

Add to agent instructions:
```markdown
## Session Initialization Protocol

**BEFORE MAKING ANY CODE CHANGES:**
1. Review NON-NEGOTIABLE DIRECTIVES (scroll to top)
2. Acknowledge constraints in internal reasoning
3. Plan approach ensuring compliance
4. Identify potential violation points
```

### 1.3 Add Post-Session Verification Checklist

Add to agent instructions:
```markdown
## Session Completion Protocol

**BEFORE FINALIZING SESSION:**
1. Search all modified files for hardcoded values
2. Verify experimental inputs labeled "FOR VALIDATION ONLY"
3. Check placeholders have WARNING comments
4. Run automated verification (see workflow below)
5. Request code review if uncertain
```

## Phase 2: Automated Code Review Workflow

### 2.1 Create Pre-Merge Verification Workflow

**File**: `.github/workflows/agent-directive-check.yml`

**Purpose**: 
- Automatically verify Directive A compliance
- Scan for hardcoded constants
- Check for proper labeling
- Trigger review if violations detected

**Implementation**:
```yaml
name: Agent Directive Compliance Check

on:
  pull_request:
    types: [opened, synchronize, ready_for_review]
  workflow_dispatch:

jobs:
  directive-check:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install ast-grep pylint bandit
      
      - name: Scan for hardcoded experimental values
        id: scan
        run: |
          python scripts/check_directive_compliance.py \
            --check-hardcoded-values \
            --check-experimental-labels \
            --check-placeholder-warnings \
            --output violations.json
      
      - name: Upload violation report
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: directive-violations
          path: violations.json
      
      - name: Comment on PR if violations found
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const violations = JSON.parse(fs.readFileSync('violations.json', 'utf8'));
            
            const body = `## ⚠️ Directive A Violations Detected
            
            The following hardcoded values were found:
            
            ${violations.map(v => `- \`${v.file}:${v.line}\`: ${v.value} (${v.context})`).join('\n')}
            
            **Required actions:**
            1. Derive values from topological invariants
            2. Label experimental inputs "FOR VALIDATION ONLY"
            3. Add WARNING to placeholders
            
            See [Directive A](../agents/irh-computational-research.md#directive-a) for details.`;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
```

### 2.2 Create Directive Compliance Checker Script

**File**: `scripts/check_directive_compliance.py`

**Features**:
- Parse Python files for hardcoded constants
- Identify experimental value patterns (137.036, 0.511, etc.)
- Check for proper labeling ("FOR VALIDATION ONLY")
- Verify placeholder warnings
- Generate violation report

**Implementation**: (See separate script file)

### 2.3 Integrate with Existing Code Review

Modify `.github/workflows/irh-compute.yml` to:
1. Run directive check before execution
2. Hold session open for review
3. Force implementation of suggestions

## Phase 3: AI-Guided Review Integration

### 3.1 Add Gemini Review Step

**File**: `.github/workflows/gemini-review.yml`

**Purpose**:
- Trigger comprehensive AI review before session end
- Hold session open until review complete
- Force implementation of suggestions
- Prioritize derivation over admission of failure

**Implementation**:
```yaml
name: Gemini Code Review

on:
  workflow_call:
    inputs:
      pr_number:
        required: true
        type: number
      session_id:
        required: true
        type: string

jobs:
  gemini-review:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Gemini API
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          pip install google-generativeai
      
      - name: Run Gemini review
        id: review
        run: |
          python scripts/gemini_review.py \
            --pr-number ${{ inputs.pr_number }} \
            --directives .github/agents/irh-computational-research.md \
            --focus-areas "hardcoded values,experimental inputs,placeholder implementations" \
            --output review_results.json
      
      - name: Post review comments
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = JSON.parse(fs.readFileSync('review_results.json', 'utf8'));
            
            for (const issue of review.issues) {
              if (issue.severity === 'CRITICAL') {
                github.rest.pulls.createReviewComment({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  pull_number: ${{ inputs.pr_number }},
                  body: `🚨 CRITICAL: ${issue.message}\n\n**Required:** ${issue.fix_required}`,
                  commit_id: context.sha,
                  path: issue.file,
                  line: issue.line
                });
              }
            }
      
      - name: Block merge if critical issues
        if: steps.review.outputs.has_critical == 'true'
        run: |
          echo "::error::Critical directive violations must be resolved"
          exit 1
      
      - name: Notify agent session
        run: |
          # Keep session alive and force implementation
          curl -X POST \
            -H "Authorization: Bearer ${{ secrets.GITHUB_TOKEN }}" \
            -d '{"session_id": "${{ inputs.session_id }}", "action": "implement_review"}' \
            https://api.github.com/repos/${{ github.repository }}/dispatches
```

### 3.2 Create Gemini Review Script

**File**: `scripts/gemini_review.py`

**Features**:
- Load Directive A, B, C constraints
- Analyze all code changes
- Identify violations with severity
- Suggest derivations (not admissions of failure)
- Generate actionable fix recommendations

**Key Logic**:
```python
def analyze_for_violations(code, directives):
    """
    Priority: Always suggest derivation path over failure admission.
    
    If code has:
    - Hardcoded value → Suggest topological derivation
    - Experimental input → Suggest theoretical calculation
    - Placeholder → Suggest completion from theory
    
    Never suggest: "Acknowledge limitation" as primary fix
    Always suggest: Physical/mathematical derivation
    """
    pass
```

## Phase 4: Future Enhancements (Next Phase)

### 4.1 Self-Improving Theoretical Framework

**Concept**: AI-guided theory evolution system that:
1. Computes all predictions from current theory
2. Identifies correct vs. error predictions
3. Learns from mistakes
4. Suggests theoretical refinements
5. Iteratively improves framework

**Implementation Plan**:
- Create `theory_evolution/` module
- Implement calculation engine
- Build error analysis system
- Add AI-guided refinement
- Synoptic integration of corrections

**File**: `docs/THEORY_EVOLUTION_SYSTEM.md` (to be created)

### 4.2 Components

1. **Calculation Engine**: Runs all IRH predictions
2. **Validation Module**: Compares to experiments
3. **Error Analyzer**: Identifies systematic issues
4. **AI Advisor**: Suggests theoretical modifications
5. **Integration System**: Synoptically combines improvements

## Implementation Timeline

### Week 1: Phase 1 (Directive Enforcement) ✅ COMPLETED
- [x] Update agent instructions with NON-NEGOTIABLE section
- [x] Add pre-session and post-session checklists
- [x] Test with sample sessions

### Week 2: Phase 2 (Automated Verification) ✅ COMPLETED
- [x] Create directive compliance checker script
- [x] Implement workflow integration
- [x] Test on existing violations

### Week 3: Phase 3 (AI Review Integration) ✅ COMPLETED
- [x] Set up Gemini API access structure
- [x] Create review script
- [x] Integrate with workflow
- [x] Test end-to-end flow (ready for API key configuration)

### Week 4+: Phase 4 (Theory Evolution) 📋 DOCUMENTED
- [x] Design system architecture
- [ ] Implement calculation engine (future work)
- [ ] Build error analysis (future work)
- [ ] Create AI advisor (future work)
- [ ] Test iterations (future work)

## Success Metrics

1. **Directive Compliance**: Zero hardcoded values in merged code
2. **Review Efficiency**: 100% of PRs reviewed before merge
3. **Fix Rate**: >90% of suggestions implemented
4. **Theory Accuracy**: Measurable improvement in prediction accuracy

## Notes

- All hardcoded values violating Directive A are unacceptable
- Automated enforcement prevents human error/forgetfulness
- AI review provides consistent standards
- Future system enables continuous improvement

## Status

- [x] Phase 1: **COMPLETED** (2026-01-04)
  - Updated `.github/agents/irh-computational-research.agent.md` with NON-NEGOTIABLE DIRECTIVES
  - Added DIRECTIVE A, B, C enforcement sections
  - Added Session Initialization and Completion Protocols
  
- [x] Phase 2: **COMPLETED** (2026-01-04)
  - Created `scripts/check_directive_compliance.py` with comprehensive violation detection
  - Created `.github/workflows/agent-directive-check.yml` for automated PR checking
  - Implemented hardcoded value detection, experimental label checking, and placeholder warnings
  - Added PR commenting and artifact upload functionality
  
- [x] Phase 3: **COMPLETED** (2026-01-04)
  - Created `scripts/gemini_review.py` with AI-powered code analysis
  - Created `.github/workflows/gemini-review.yml` as reusable workflow
  - Implemented directive-aware review with actionable fix suggestions
  - Added rule-based fallback for environments without Gemini API access
  - Prioritizes derivation suggestions over pragmatic workarounds
  
- [x] Phase 4: **DESIGN PHASE COMPLETED** (2026-01-04)
  - Created comprehensive `docs/THEORY_EVOLUTION_SYSTEM.md` documentation
  - Documented all 5 system components with detailed specifications
  - Defined implementation roadmap, success metrics, and safety mechanisms
  - Ready for future implementation after Phases 1-3 validation
