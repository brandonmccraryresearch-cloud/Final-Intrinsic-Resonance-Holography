#!/usr/bin/env python3
"""
Gemini AI Code Review for IRH Directive Compliance

This script uses Google's Gemini AI to perform intelligent code review
focused on IRH Directive A, B, and C compliance. It provides actionable
suggestions for deriving constants from topological invariants.

Key Features:
- Loads directive constraints from agent instructions
- Analyzes code changes in PRs
- Identifies violations with severity levels
- **Priority: Always suggest derivation path over failure admission**
- Generates actionable fix recommendations

Usage:
    python gemini_review.py \
        --pr-number 42 \
        --directives .github/agents/irh-computational-research.agent.md \
        --focus-areas "hardcoded values,experimental inputs,placeholder implementations" \
        --output review_results.json

Author: IRH Computational Research Team
Version: 1.0.0
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import subprocess


try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Install with: pip install google-generativeai",
          file=sys.stderr)


class GeminiReviewer:
    """AI-powered code reviewer for IRH directive compliance."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini reviewer.
        
        Args:
            api_key: Gemini API key (if None, reads from GEMINI_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        self.model = None
        self.directives = {}
        self.issues: List[Dict[str, Any]] = []
        
        if GEMINI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                # Use Gemini 3 Pro for advanced reasoning and code review
                self.model = genai.GenerativeModel('gemini-3-pro')
            except Exception as e:
                print(f"Warning: Could not initialize Gemini: {e}", file=sys.stderr)
                self.model = None
    
    def load_directives(self, directives_file: str) -> None:
        """
        Load directive constraints from agent instructions file.
        
        Args:
            directives_file: Path to agent instructions markdown file
        """
        try:
            with open(directives_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract directive sections
            self.directives = {
                'full_content': content,
                'directive_a': self._extract_section(content, 'DIRECTIVE A'),
                'directive_b': self._extract_section(content, 'DIRECTIVE B'),
                'directive_c': self._extract_section(content, 'DIRECTIVE C'),
            }
            
            print(f"Loaded directives from {directives_file}")
            
        except Exception as e:
            print(f"Error loading directives: {e}", file=sys.stderr)
            self.directives = {}
    
    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a specific section from markdown content."""
        pattern = rf'## {section_name}.*?(?=\n## |\n---|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(0) if match else ""
    
    def get_pr_diff(self, pr_number: int) -> str:
        """
        Get the diff for a PR using GitHub CLI or git commands.
        
        Args:
            pr_number: Pull request number
            
        Returns:
            PR diff as string
        """
        try:
            # Try using GitHub CLI first
            result = subprocess.run(
                ['gh', 'pr', 'diff', str(pr_number)],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback: get diff from git
            try:
                # Fetch PR branch
                result = subprocess.run(
                    ['git', 'diff', f'origin/main...HEAD'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.stdout
            except subprocess.CalledProcessError as e:
                print(f"Error getting PR diff: {e}", file=sys.stderr)
                return ""
    
    def analyze_with_gemini(self, code_diff: str, focus_areas: List[str]) -> List[Dict[str, Any]]:
        """
        Use Gemini AI to analyze code for directive violations.
        
        Args:
            code_diff: Git diff of code changes
            focus_areas: Specific areas to focus on
            
        Returns:
            List of issues found
        """
        if not self.model:
            print("Gemini model not available, using rule-based analysis", file=sys.stderr)
            return self._rule_based_analysis(code_diff, focus_areas)
        
        # Construct prompt for Gemini
        prompt = self._build_analysis_prompt(code_diff, focus_areas)
        
        try:
            # Generate review with Gemini
            response = self.model.generate_content(prompt)
            
            # Parse response to extract issues
            issues = self._parse_gemini_response(response.text)
            return issues
            
        except Exception as e:
            print(f"Error during Gemini analysis: {e}", file=sys.stderr)
            return self._rule_based_analysis(code_diff, focus_areas)
    
    def _build_analysis_prompt(self, code_diff: str, focus_areas: List[str]) -> str:
        """Build the prompt for Gemini analysis."""
        prompt = f"""You are an expert code reviewer for the Intrinsic Resonance Holography (IRH) theoretical physics framework.

Your task is to review the following code changes and identify violations of IRH computational directives.

## DIRECTIVES TO ENFORCE:

{self.directives.get('directive_a', 'See full directives')}

{self.directives.get('directive_b', 'See full directives')}

{self.directives.get('directive_c', 'See full directives')}

## FOCUS AREAS:
{', '.join(focus_areas)}

## CODE CHANGES TO REVIEW:

```diff
{code_diff[:500000]}  # Gemini 3 Pro supports up to 1M token context (approximately 750K characters)
```

## YOUR TASK:

1. Identify any violations of Directive A (hardcoded experimental values)
2. Identify any violations of Directive B (precision requirements)
3. Identify any violations of Directive C (improper terminology)
4. For EACH violation, provide:
   - File and line number (if discernible from diff)
   - Severity: CRITICAL, WARNING, or INFO
   - Clear explanation of the violation
   - **ACTIONABLE FIX** - Always suggest derivation path, never just "acknowledge limitation"
   
5. For hardcoded values → Suggest topological derivation approach (Hopf fibration, Chern classes, etc.)
6. For experimental inputs → Suggest theoretical calculation method
7. For placeholders → Suggest completion from IRH theory

## OUTPUT FORMAT:

Return a JSON array of issues:

```json
[
  {{
    "file": "notebooks/02_harmony_functional.ipynb",
    "line": 42,
    "severity": "CRITICAL",
    "message": "Hardcoded experimental value α = 1/137.036 used as input",
    "violation_type": "DIRECTIVE_A_HARDCODED_VALUE",
    "fix_required": "Derive α from Hopf fibration volume ratios: α⁻¹ = (Vol(S⁷)/Vol(S³)) × η where η = 4/π. See Section 2 of IRHv26.0.",
    "suggested_code": "# Derive from topology\\nvolume_S7 = (np.pi**4) / 24\\nvolume_S3 = 2 * np.pi**2\\neta = 4 / np.pi\\nalpha_inv = (volume_S7 / volume_S3) * eta"
  }},
  ...
]
```

**IMPORTANT:** Your suggestions should ALWAYS prioritize theoretical derivation over pragmatic workarounds.

Begin your analysis:
"""
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse Gemini's response to extract issues."""
        issues = []
        
        # Try to extract JSON from response
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            try:
                issues_data = json.loads(json_match.group(1))
                if isinstance(issues_data, list):
                    issues = issues_data
                else:
                    print("Warning: Gemini returned non-list JSON", file=sys.stderr)
            except json.JSONDecodeError as e:
                print(f"Warning: Could not parse Gemini JSON: {e}", file=sys.stderr)
        
        # Fallback: parse structured text
        if not issues:
            issues = self._parse_text_response(response_text)
        
        return issues
    
    def _parse_text_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse text response if JSON parsing fails."""
        issues = []
        
        # Look for severity markers
        severity_patterns = [
            (r'\*\*CRITICAL\*\*:(.+?)(?=\*\*|$)', 'CRITICAL'),
            (r'\*\*WARNING\*\*:(.+?)(?=\*\*|$)', 'WARNING'),
            (r'\*\*INFO\*\*:(.+?)(?=\*\*|$)', 'INFO'),
        ]
        
        for pattern, severity in severity_patterns:
            matches = re.finditer(pattern, response_text, re.DOTALL)
            for match in matches:
                issue_text = match.group(1).strip()
                issues.append({
                    'file': 'Unknown',
                    'line': 0,
                    'severity': severity,
                    'message': issue_text[:200],
                    'violation_type': 'UNKNOWN',
                    'fix_required': 'See Gemini response for details'
                })
        
        return issues
    
    def _rule_based_analysis(self, code_diff: str, focus_areas: List[str]) -> List[Dict[str, Any]]:
        """
        Fallback rule-based analysis when Gemini is not available.
        
        This provides basic pattern matching for common violations.
        """
        issues = []
        
        # Parse diff to extract changed lines
        current_file = None
        current_line = 0
        
        for line in code_diff.split('\n'):
            # Track which file we're in
            if line.startswith('+++'):
                current_file = line[6:].strip()
            
            # Track line numbers
            if line.startswith('@@'):
                match = re.search(r'\+(\d+)', line)
                if match:
                    current_line = int(match.group(1))
            
            # Check added lines
            if line.startswith('+') and not line.startswith('+++'):
                current_line += 1
                
                # Check for hardcoded experimental values
                if 'hardcoded values' in ' '.join(focus_areas):
                    if re.search(r'137\.03[0-9]', line):
                        issues.append({
                            'file': current_file or 'Unknown',
                            'line': current_line,
                            'severity': 'CRITICAL',
                            'message': 'Potential hardcoded fine-structure constant',
                            'violation_type': 'DIRECTIVE_A_HARDCODED_VALUE',
                            'fix_required': 'Derive α from Hopf fibration volume ratios'
                        })
                    
                    if re.search(r'0\.511|9\.109', line):
                        issues.append({
                            'file': current_file or 'Unknown',
                            'line': current_line,
                            'severity': 'CRITICAL',
                            'message': 'Potential hardcoded electron mass',
                            'violation_type': 'DIRECTIVE_A_HARDCODED_VALUE',
                            'fix_required': 'Derive from Koide formula eigenvalue problem'
                        })
                
                # Check for information metaphors (Directive C)
                if re.search(r'information\s+(transfer|exchange|encode)', line, re.IGNORECASE):
                    issues.append({
                        'file': current_file or 'Unknown',
                        'line': current_line,
                        'severity': 'WARNING',
                        'message': 'Information-theoretic metaphor detected',
                        'violation_type': 'DIRECTIVE_C_TERMINOLOGY',
                        'fix_required': 'Use gauge theory terminology: "curvature", "connection", "holonomy"'
                    })
        
        return issues
    
    def review_pr(self, pr_number: int, focus_areas: List[str]) -> Dict[str, Any]:
        """
        Perform complete PR review.
        
        Args:
            pr_number: Pull request number
            focus_areas: Specific areas to focus on
            
        Returns:
            Review results dictionary
        """
        # Get PR diff
        print(f"Fetching PR #{pr_number} diff...")
        code_diff = self.get_pr_diff(pr_number)
        
        if not code_diff:
            print("Warning: No diff available, skipping analysis", file=sys.stderr)
            return {
                'pr_number': pr_number,
                'issues': [],
                'has_critical': False
            }
        
        # Analyze with Gemini or fallback
        print(f"Analyzing code changes (focus: {', '.join(focus_areas)})...")
        issues = self.analyze_with_gemini(code_diff, focus_areas)
        
        # Compile results
        has_critical = any(issue.get('severity') == 'CRITICAL' for issue in issues)
        
        results = {
            'pr_number': pr_number,
            'issues': issues,
            'has_critical': has_critical,
            'total_issues': len(issues),
            'critical_count': sum(1 for i in issues if i.get('severity') == 'CRITICAL'),
            'warning_count': sum(1 for i in issues if i.get('severity') == 'WARNING'),
        }
        
        print(f"\nAnalysis complete: {len(issues)} issues found")
        print(f"  - Critical: {results['critical_count']}")
        print(f"  - Warnings: {results['warning_count']}")
        
        return results


def main():
    """Main entry point for Gemini code review."""
    parser = argparse.ArgumentParser(
        description='AI-powered code review for IRH directive compliance'
    )
    parser.add_argument(
        '--pr-number',
        type=int,
        required=True,
        help='Pull request number to review'
    )
    parser.add_argument(
        '--directives',
        type=str,
        default='.github/agents/irh-computational-research.agent.md',
        help='Path to agent directives file'
    )
    parser.add_argument(
        '--focus-areas',
        type=str,
        default='hardcoded values,experimental inputs,placeholder implementations',
        help='Comma-separated list of focus areas'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='review_results.json',
        help='Output file for review results (JSON)'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        default=None,
        help='Gemini API key (or set GEMINI_API_KEY env var)'
    )
    
    args = parser.parse_args()
    
    # Parse focus areas
    focus_areas = [area.strip() for area in args.focus_areas.split(',')]
    
    # Initialize reviewer
    reviewer = GeminiReviewer(api_key=args.api_key)
    
    # Load directives
    if Path(args.directives).exists():
        reviewer.load_directives(args.directives)
    else:
        print(f"Warning: Directives file not found: {args.directives}", file=sys.stderr)
    
    # Perform review
    results = reviewer.review_pr(args.pr_number, focus_areas)
    
    # Write results
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults written to: {args.output}")
    
    # Print summary
    print(f"\n{'='*70}")
    print("GEMINI CODE REVIEW SUMMARY")
    print(f"{'='*70}")
    print(f"PR: #{results['pr_number']}")
    print(f"Total issues: {results.get('total_issues', 0)}")
    print(f"  - Critical: {results.get('critical_count', 0)}")
    print(f"  - Warnings: {results.get('warning_count', 0)}")
    
    if results.get('issues'):
        print(f"\n{'='*70}")
        print("ISSUES FOUND:")
        print(f"{'='*70}")
        for issue in results['issues'][:5]:  # Show first 5
            print(f"\n[{issue.get('severity', 'UNKNOWN')}] {issue.get('file', 'Unknown')}:{issue.get('line', 0)}")
            print(f"  {issue.get('message', 'No message')}")
            print(f"  Fix: {issue.get('fix_required', 'No fix suggested')[:100]}")
        
        if len(results['issues']) > 5:
            print(f"\n... and {len(results['issues']) - 5} more issues")
    
    # Exit with error if critical issues found
    if results.get('has_critical', False):
        print(f"\n{'='*70}")
        print("❌ CRITICAL ISSUES DETECTED")
        print(f"{'='*70}")
        sys.exit(1)
    else:
        print(f"\n{'='*70}")
        print("✅ NO CRITICAL ISSUES")
        print(f"{'='*70}")
        sys.exit(0)


if __name__ == '__main__':
    main()
