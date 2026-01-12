#!/usr/bin/env python3
"""
Example: Using Gen AI SDK with IRH AI Advisor

This script demonstrates how to use the Gen AI SDK integration
to generate AI-powered refinement suggestions for the IRH theory.

Requirements:
- pip install google-genai
- export GOOGLE_CLOUD_API_KEY="your_key_here"
"""

import os
import sys

# Check if running from correct directory
if not os.path.exists('evolution_system'):
    print("Error: Run this script from the repository root directory")
    sys.exit(1)

from evolution_system import AIAdvisor, ErrorAnalyzer, ValidationModule, CalculationEngine, ExperimentalDatabase

def main():
    """Run the Gen AI enhanced AI Advisor."""
    
    print("=" * 70)
    print("IRH AI Advisor - Gen AI SDK Example")
    print("=" * 70)
    print()
    
    # Step 1: Check Gen AI availability
    print("1. Checking Gen AI SDK availability...")
    advisor = AIAdvisor()
    
    if advisor._genai_client:
        print("   ✅ Gen AI SDK is available and configured")
        print(f"   API Key: {'*' * 20}{os.environ.get('GOOGLE_CLOUD_API_KEY', '')[-4:]}")
    else:
        print("   ⚠️  Gen AI SDK not available")
        print("   Install with: pip install --upgrade google-genai")
        print("   Set API key: export GOOGLE_CLOUD_API_KEY='your_key'")
        print()
        print("   Continuing with built-in topological templates...")
    print()
    
    # Step 2: Compute predictions
    print("2. Computing theoretical predictions...")
    engine = CalculationEngine()
    predictions = engine.compute_all_predictions()
    print(f"   ✅ Computed {len(predictions)} predictions")
    print()
    
    # Step 3: Validate against experiments
    print("3. Validating against experimental measurements...")
    db = ExperimentalDatabase()
    validator = ValidationModule(db)
    report = validator.validate_all(predictions)
    print(f"   ✅ Validation complete")
    print(f"   Excellent: {report.excellent_count}, Good: {report.good_count}")
    print(f"   Fair: {report.fair_count}, Poor: {report.poor_count}")
    print()
    
    # Step 4: Analyze errors
    print("4. Analyzing error patterns...")
    analyzer = ErrorAnalyzer()
    analysis = analyzer.analyze(report)
    print(f"   ✅ Found {len(analysis.patterns)} error patterns")
    for pattern in analysis.patterns[:3]:
        print(f"   - {pattern.severity.value}: {pattern.description[:60]}...")
    print()
    
    # Step 5: Generate template-based suggestions
    print("5. Generating template-based suggestions...")
    template_suggestions = advisor.get_top_suggestions(analysis.to_dict(), n=3)
    print(f"   ✅ Generated {len(template_suggestions)} suggestions")
    for i, sugg in enumerate(template_suggestions, 1):
        print(f"   {i}. {sugg.modification.name}")
        print(f"      Confidence: {sugg.modification.confidence.value}")
        print(f"      Priority: {sugg.modification.priority_score:.1f}")
    print()
    
    # Step 6: Generate AI-enhanced suggestions (if available)
    if advisor._genai_client:
        print("6. Generating AI-enhanced suggestions with Gen AI SDK...")
        print("   (This may take 30-60 seconds with HIGH thinking level)")
        print()
        
        try:
            ai_suggestions = advisor.get_genai_suggestions(analysis.to_dict())
            
            if ai_suggestions:
                print("   ✅ Gen AI suggestions received")
                print()
                print("=" * 70)
                print("AI-ENHANCED REFINEMENT SUGGESTIONS")
                print("=" * 70)
                print()
                print(ai_suggestions)
                print()
            else:
                print("   ⚠️  No suggestions generated (API error or rate limit)")
                
        except Exception as e:
            print(f"   ❌ Error generating AI suggestions: {e}")
    else:
        print("6. Skipping AI-enhanced suggestions (Gen AI SDK not available)")
    
    print()
    print("=" * 70)
    print("Example complete!")
    print("=" * 70)
    
    # Summary
    print()
    print("Summary:")
    print(f"- Template-based suggestions: {len(template_suggestions)}")
    print(f"- Gen AI SDK available: {advisor._genai_client is not None}")
    print()
    print("To use Gen AI SDK in your own code:")
    print()
    print("    advisor = AIAdvisor()")
    print("    if advisor._genai_client:")
    print("        suggestions = advisor.get_genai_suggestions(analysis.to_dict())")
    print("        print(suggestions)")
    print()

if __name__ == "__main__":
    main()
