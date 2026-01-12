#!/usr/bin/env python3
"""
Gemini 3 Pro Theory Self-Examination Script
============================================

This script performs comprehensive self-examination of IRH theory using
Google's Gemini 3 Pro AI model with HIGH thinking level.

Features:
- Mathematical consistency checking
- Physical interpretability analysis
- Derivation completeness validation
- Experimental testability assessment
- Refinement suggestions

Usage:
    export GEMINI_API_KEY="your_api_key_here"
    python gemini_theory_examiner.py [--theory-file PATH] [--analysis-type TYPE]

Analysis Types:
    - comprehensive (default): Full analysis
    - mathematical: Focus on mathematical rigor
    - physical: Focus on physical content
    - consistency: Check internal consistency
    - self-examine: Critical self-examination

Author: IRH Computational Research Team
Version: 1.0.0
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import evolution_system
sys.path.insert(0, str(Path(__file__).parent.parent))

from evolution_system.gemini_integration import GeminiTheoryAdvisor


def load_theory(theory_file: Path, max_chars: int = 100000) -> str:
    """
    Load theory text from file.
    
    Args:
        theory_file: Path to theory file
        max_chars: Maximum characters to load
        
    Returns:
        Theory text
    """
    if not theory_file.exists():
        print(f"❌ Error: Theory file not found: {theory_file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(theory_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if len(content) > max_chars:
            print(f"⚠️  Warning: Theory file is {len(content)} chars, truncating to {max_chars}")
            content = content[:max_chars]
        
        return content
    
    except Exception as e:
        print(f"❌ Error loading theory file: {e}", file=sys.stderr)
        sys.exit(1)


def save_results(results: dict, output_file: Path):
    """Save analysis results to JSON file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"\n✅ Results saved to: {output_file}")
    except Exception as e:
        print(f"⚠️  Warning: Could not save results: {e}", file=sys.stderr)


def main():
    """Main entry point for theory examination."""
    parser = argparse.ArgumentParser(
        description='Gemini 3 Pro Theory Self-Examination',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Self-examine current theory
    python gemini_theory_examiner.py --analysis-type self-examine
    
    # Comprehensive mathematical analysis
    python gemini_theory_examiner.py --theory-file README.md --analysis-type mathematical
    
    # Check consistency with custom concerns
    python gemini_theory_examiner.py --self-examine --concerns "hardcoded values" "gauge terminology"
    
    # Generate refinement suggestions
    python gemini_theory_examiner.py --refinements
"""
    )
    
    parser.add_argument(
        '--theory-file',
        type=Path,
        default=Path('README.md'),
        help='Path to theory file (default: README.md)'
    )
    
    parser.add_argument(
        '--analysis-type',
        choices=['comprehensive', 'mathematical', 'physical', 'consistency', 'self-examine'],
        default='self-examine',
        help='Type of analysis to perform (default: self-examine)'
    )
    
    parser.add_argument(
        '--refinements',
        action='store_true',
        help='Generate refinement suggestions'
    )
    
    parser.add_argument(
        '--concerns',
        nargs='+',
        help='Specific concerns for self-examination'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('gemini_analysis_results.json'),
        help='Output file for results (default: gemini_analysis_results.json)'
    )
    
    parser.add_argument(
        '--max-chars',
        type=int,
        default=100000,
        help='Maximum characters to load from theory file (default: 100000)'
    )
    
    args = parser.parse_args()
    
    # Print header
    print("="*70)
    print("IRH Theory Self-Examination with Gemini 3 Pro")
    print("="*70)
    print()
    
    # Initialize Gemini advisor
    print("🚀 Initializing Gemini 3 Pro...")
    advisor = GeminiTheoryAdvisor()
    
    if not advisor.client:
        print("\n❌ Failed to initialize Gemini client")
        print("\nPlease ensure:")
        print("  1. Install google-genai: pip install google-genai")
        print("  2. Set API key: export GEMINI_API_KEY='your_key_here'")
        sys.exit(1)
    
    print("✅ Gemini 3 Pro ready\n")
    
    # Load theory
    print(f"📖 Loading theory from: {args.theory_file}")
    theory_text = load_theory(args.theory_file, args.max_chars)
    print(f"✅ Loaded {len(theory_text)} characters\n")
    
    # Prepare results dictionary
    results = {
        'timestamp': datetime.now().isoformat(),
        'theory_file': str(args.theory_file),
        'theory_length': len(theory_text),
        'analysis_type': args.analysis_type,
        'results': {}
    }
    
    # Perform analysis
    try:
        if args.refinements:
            print("🔧 Generating refinement suggestions...")
            print("   (This may take 1-2 minutes with HIGH thinking level)\n")
            
            response = advisor.suggest_refinements(theory_text)
            results['results']['refinements'] = response
            
        elif args.analysis_type == 'self-examine':
            print("🔍 Performing critical self-examination...")
            print("   (This may take 1-2 minutes with HIGH thinking level)\n")
            
            response = advisor.self_examine(theory_text, args.concerns)
            results['results']['self_examination'] = response
            
        else:
            print(f"🔬 Performing {args.analysis_type} analysis...")
            print("   (This may take 1-2 minutes with HIGH thinking level)\n")
            
            response = advisor.analyze_theory(theory_text, args.analysis_type)
            results['results'][args.analysis_type] = response
        
        if response:
            print("\n✅ Analysis complete!")
            results['status'] = 'success'
        else:
            print("\n❌ Analysis failed - no response received")
            results['status'] = 'failed'
            results['error'] = 'No response from Gemini'
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        results['status'] = 'interrupted'
        sys.exit(1)
    
    except Exception as e:
        analysis_context = args.analysis_type if not args.refinements else 'refinement generation'
        print(f"\n❌ Error during {analysis_context}: {e}", file=sys.stderr)
        results['status'] = 'error'
        results['error'] = str(e)
        results['error_context'] = analysis_context
        sys.exit(1)
    
    # Save results
    save_results(results, args.output)
    
    # Print summary
    print("\n" + "="*70)
    print("ANALYSIS SUMMARY")
    print("="*70)
    print(f"Theory file: {args.theory_file}")
    print(f"Analysis type: {args.analysis_type}")
    print(f"Status: {results['status']}")
    if response:
        print(f"Response length: {len(response)} characters")
    print(f"Results saved: {args.output}")
    print("="*70)
    
    print("\n💡 Next steps:")
    print("   1. Review the analysis results")
    print("   2. Address any CRITICAL or MAJOR issues identified")
    print("   3. Consider implementing suggested refinements")
    print("   4. Re-run analysis after making changes")
    print()


if __name__ == '__main__':
    main()
