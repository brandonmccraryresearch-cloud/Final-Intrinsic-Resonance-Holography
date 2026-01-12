"""
Evolution Cycle Orchestrator for IRH Theory Evolution System

Phase 4 Implementation: Run complete evolution cycles to improve the theory.

This module provides:
- Complete evolution cycle execution
- Multi-refinement processing
- Progress tracking and reporting
- Command-line interface

**Key Principle:** The orchestrator coordinates all components to systematically
improve the IRH theory through topologically-motivated refinements.

Usage:
    from evolution_system import EvolutionCycle
    
    # Run a complete evolution cycle
    cycle = EvolutionCycle()
    results = cycle.run(max_refinements=5)
    
    # Print summary
    cycle.print_summary()
    
    # Or from command line:
    # python -m evolution_system.evolution_cycle --max-refinements 5

Author: IRH Computational Research Team
Date: 2026-01-09
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import json
import argparse
import sys

# Local imports
try:
    from .calculation_engine import CalculationEngine
    from .experimental_database import ExperimentalDatabase
    from .validation_module import ValidationModule
    from .error_analyzer import ErrorAnalyzer
    from .ai_advisor import AIAdvisor, RefinementSuggestion
    from .integration_system import (
        IntegrationSystem, IntegrationResult
    )
    from .documentation_updater import DocumentationUpdater
except ImportError as e:
    # Handle standalone execution
    import warnings
    warnings.warn(f"Could not import evolution_system modules: {e}")


class CycleStatus:
    """Status of an evolution cycle."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class CycleResult:
    """Result of a single evolution cycle."""
    cycle_id: str
    status: str
    start_time: str
    end_time: Optional[str] = None
    
    # Counts
    refinements_tested: int = 0
    refinements_integrated: int = 0
    refinements_rejected: int = 0
    
    # Details
    integration_results: List[IntegrationResult] = field(default_factory=list)
    suggestions_considered: int = 0
    
    # Baseline statistics
    baseline_mean_sigma: Optional[float] = None
    baseline_pass_rate: Optional[float] = None
    
    # Final statistics
    final_mean_sigma: Optional[float] = None
    final_pass_rate: Optional[float] = None
    
    # Improvements
    sigma_improvement: Optional[float] = None  # Positive = better
    pass_rate_improvement: Optional[float] = None
    
    # Errors
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "cycle_id": self.cycle_id,
            "status": self.status,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "refinements_tested": self.refinements_tested,
            "refinements_integrated": self.refinements_integrated,
            "refinements_rejected": self.refinements_rejected,
            "suggestions_considered": self.suggestions_considered,
            "baseline_mean_sigma": self.baseline_mean_sigma,
            "baseline_pass_rate": self.baseline_pass_rate,
            "final_mean_sigma": self.final_mean_sigma,
            "final_pass_rate": self.final_pass_rate,
            "sigma_improvement": self.sigma_improvement,
            "pass_rate_improvement": self.pass_rate_improvement,
            "errors": self.errors,
            "integration_results": [r.to_dict() for r in self.integration_results],
        }


class EvolutionCycle:
    """
    Orchestrates a complete evolution cycle for the IRH theory.
    
    A cycle consists of:
    1. Computing all theoretical predictions
    2. Validating against experimental values
    3. Analyzing error patterns
    4. Generating refinement suggestions
    5. Testing and integrating successful refinements
    6. Updating documentation
    
    **Directive A Compliance:** All refinements must have topological origin.
    No phenomenological parameters are allowed.
    """
    
    def __init__(
        self,
        repo_root: Optional[str] = None,
        sigma_tolerance: float = 0.5,
        verbose: bool = True
    ):
        """
        Initialize the evolution cycle orchestrator.
        
        Args:
            repo_root: Path to repository root (auto-detected if None)
            sigma_tolerance: Maximum allowed σ regression (default 0.5)
            verbose: Whether to print progress information
        """
        self.verbose = verbose
        
        # Initialize components
        self.engine = CalculationEngine()
        self.db = ExperimentalDatabase()
        self.validator = ValidationModule(self.db)
        self.analyzer = ErrorAnalyzer()
        self.advisor = AIAdvisor()
        self.integrator = IntegrationSystem(sigma_tolerance)
        self.doc_updater = DocumentationUpdater(repo_root)
        
        # Cycle history
        self._cycle_history: List[CycleResult] = []
        self._current_cycle: Optional[CycleResult] = None
    
    def _log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def run(
        self,
        max_refinements: int = 5,
        auto_integrate: bool = False
    ) -> CycleResult:
        """
        Run a complete evolution cycle.
        
        Args:
            max_refinements: Maximum number of refinements to try
            auto_integrate: Whether to automatically integrate successful refinements
        
        Returns:
            CycleResult with cycle statistics
        """
        # Initialize cycle result
        cycle_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = CycleResult(
            cycle_id=cycle_id,
            status=CycleStatus.RUNNING,
            start_time=datetime.now().isoformat()
        )
        self._current_cycle = result
        
        self._log("=" * 70)
        self._log(f"EVOLUTION CYCLE {cycle_id}")
        self._log("=" * 70)
        self._log("")
        
        try:
            # Step 1: Compute baseline predictions
            self._log("Step 1: Computing baseline predictions...")
            predictions = self.engine.compute_all_predictions()
            self._log(f"  Computed {len(predictions)} predictions")
            
            # Step 2: Validate against experiments
            self._log("Step 2: Validating against experimental values...")
            baseline_report = self.validator.validate_all(predictions)
            
            result.baseline_mean_sigma = baseline_report.mean_sigma_deviation
            result.baseline_pass_rate = baseline_report.overall_pass_rate
            
            self._log(f"  Compared: {baseline_report.compared_predictions} predictions")
            self._log(f"  Mean σ: {result.baseline_mean_sigma:.2f}")
            self._log(f"  Pass rate: {result.baseline_pass_rate * 100:.1f}%")
            
            # Step 3: Analyze error patterns
            self._log("Step 3: Analyzing error patterns...")
            analysis = self.analyzer.analyze(baseline_report)
            
            self._log(f"  Patterns found: {len(analysis.patterns)}")
            self._log(f"  Critical: {analysis.critical_patterns}")
            self._log(f"  High: {analysis.high_patterns}")
            
            # Step 4: Generate refinement suggestions
            self._log("Step 4: Generating refinement suggestions...")
            suggestions = self.advisor.get_top_suggestions(
                analysis.to_dict(), n=max_refinements * 2
            )
            
            result.suggestions_considered = len(suggestions)
            self._log(f"  Generated {len(suggestions)} suggestions")
            
            if not suggestions:
                self._log("  No refinement suggestions generated")
                result.status = CycleStatus.COMPLETED
                result.end_time = datetime.now().isoformat()
                self._cycle_history.append(result)
                return result
            
            # Step 5: Test refinements
            self._log("Step 5: Testing refinement suggestions...")
            tested_count = 0
            
            for i, suggestion in enumerate(suggestions[:max_refinements], 1):
                self._log(f"")
                self._log(f"  [{i}/{min(len(suggestions), max_refinements)}] "
                         f"Testing: {suggestion.modification.name}")
                
                try:
                    integration_result = self.integrator.test_refinement(suggestion)
                    result.integration_results.append(integration_result)
                    tested_count += 1
                    
                    if integration_result.is_valid:
                        self._log(f"    ✓ VALIDATED (improvement: "
                                 f"{integration_result.target_improvement_pct:.2f}%)")
                        result.refinements_integrated += 1
                        
                        # Auto-integrate if enabled
                        if auto_integrate:
                            self._integrate_refinement(
                                suggestion, integration_result, result
                            )
                    else:
                        reason = integration_result.rejection_reason
                        self._log(f"    ✗ REJECTED ({reason.value if reason else 'unknown'})")
                        result.refinements_rejected += 1
                        
                except Exception as e:
                    self._log(f"    ✗ ERROR: {str(e)}")
                    result.errors.append(f"{suggestion.modification.name}: {str(e)}")
            
            result.refinements_tested = tested_count
            
            # Step 6: Compute final statistics
            self._log("")
            self._log("Step 6: Computing final statistics...")
            
            # Re-validate with any integrated refinements
            if result.refinements_integrated > 0 and auto_integrate:
                try:
                    self._log("  Recomputing predictions with integrated refinements...")
                    final_predictions = self.engine.compute_all_predictions()
                    self._log(f"  Recomputed {len(final_predictions)} predictions")
                    final_report = self.validator.validate_all(final_predictions)
                    result.final_mean_sigma = final_report.mean_sigma_deviation
                    result.final_pass_rate = final_report.overall_pass_rate
                except Exception as e:
                    # If recomputation fails for any reason, fall back to baseline statistics
                    self._log(f"  WARNING: Failed to recompute final statistics: {e}")
                    result.final_mean_sigma = result.baseline_mean_sigma
                    result.final_pass_rate = result.baseline_pass_rate
            else:
                result.final_mean_sigma = result.baseline_mean_sigma
                result.final_pass_rate = result.baseline_pass_rate
            
            # Calculate improvements
            if result.baseline_mean_sigma and result.final_mean_sigma:
                result.sigma_improvement = (
                    result.baseline_mean_sigma - result.final_mean_sigma
                )
            
            if result.baseline_pass_rate and result.final_pass_rate:
                result.pass_rate_improvement = (
                    result.final_pass_rate - result.baseline_pass_rate
                )
            
            result.status = CycleStatus.COMPLETED
            result.end_time = datetime.now().isoformat()
            
        except Exception as e:
            result.status = CycleStatus.FAILED
            result.end_time = datetime.now().isoformat()
            result.errors.append(str(e))
            self._log(f"CYCLE FAILED: {str(e)}")
        
        self._cycle_history.append(result)
        self._current_cycle = None
        
        # Print summary
        self._print_cycle_summary(result)
        
        return result
    
    def _integrate_refinement(
        self,
        suggestion: RefinementSuggestion,
        integration_result: IntegrationResult,
        cycle_result: CycleResult
    ):
        """Integrate a validated refinement and update documentation."""
        self._log(f"    Integrating refinement...")
        
        try:
            # Mark as integrated
            success = self.integrator.integrate_refinement(
                suggestion, integration_result
            )
            
            if success:
                # Create changelog entry
                entry = self.doc_updater.create_changelog_entry(
                    integration_result, suggestion
                )
                
                # Update documentation
                self.doc_updater.update_changelog(entry)
                self.doc_updater.update_integration_history(
                    integration_result, suggestion
                )
                
                self._log(f"    Documentation updated (v{entry.version})")
            else:
                self._log(f"    Integration failed")
                
        except Exception as e:
            self._log(f"    Integration error: {str(e)}")
            cycle_result.errors.append(f"Integration: {str(e)}")
    
    def _print_cycle_summary(self, result: CycleResult):
        """Print a summary of the cycle results."""
        self._log("")
        self._log("=" * 70)
        self._log("CYCLE SUMMARY")
        self._log("=" * 70)
        self._log("")
        self._log(f"Cycle ID:               {result.cycle_id}")
        self._log(f"Status:                 {result.status.upper()}")
        self._log(f"Duration:               {self._calculate_duration(result)}")
        self._log("")
        self._log(f"Suggestions considered: {result.suggestions_considered}")
        self._log(f"Refinements tested:     {result.refinements_tested}")
        self._log(f"Refinements integrated: {result.refinements_integrated}")
        self._log(f"Refinements rejected:   {result.refinements_rejected}")
        self._log("")
        
        if result.baseline_mean_sigma is not None:
            self._log(f"Baseline mean σ:        {result.baseline_mean_sigma:.3f}")
            self._log(f"Baseline pass rate:     {result.baseline_pass_rate * 100:.1f}%")
        
        if result.sigma_improvement is not None:
            sign = "+" if result.sigma_improvement > 0 else ""
            self._log(f"σ improvement:          {sign}{result.sigma_improvement:.3f}")
        
        if result.errors:
            self._log("")
            self._log(f"Errors ({len(result.errors)}):")
            for error in result.errors[:5]:
                self._log(f"  - {error}")
        
        self._log("")
        self._log("=" * 70)
    
    def _calculate_duration(self, result: CycleResult) -> str:
        """Calculate cycle duration as human-readable string."""
        if not result.start_time or not result.end_time:
            return "N/A"
        
        try:
            start = datetime.fromisoformat(result.start_time)
            end = datetime.fromisoformat(result.end_time)
            duration = end - start
            
            seconds = int(duration.total_seconds())
            if seconds < 60:
                return f"{seconds}s"
            elif seconds < 3600:
                return f"{seconds // 60}m {seconds % 60}s"
            else:
                return f"{seconds // 3600}h {(seconds % 3600) // 60}m"
        except Exception:
            return "N/A"
    
    def run_multiple(
        self,
        num_cycles: int = 3,
        max_refinements_per_cycle: int = 5,
        auto_integrate: bool = False
    ) -> List[CycleResult]:
        """
        Run multiple evolution cycles in sequence.
        
        Args:
            num_cycles: Number of cycles to run
            max_refinements_per_cycle: Max refinements per cycle
            auto_integrate: Whether to auto-integrate refinements
        
        Returns:
            List of CycleResult objects
        """
        results = []
        
        self._log("")
        self._log("=" * 70)
        self._log(f"RUNNING {num_cycles} EVOLUTION CYCLES")
        self._log("=" * 70)
        self._log("")
        
        for i in range(num_cycles):
            self._log(f"--- Cycle {i + 1} of {num_cycles} ---")
            self._log("")
            
            result = self.run(
                max_refinements=max_refinements_per_cycle,
                auto_integrate=auto_integrate
            )
            results.append(result)
            
            # Stop if cycle failed
            if result.status == CycleStatus.FAILED:
                self._log(f"Stopping due to cycle failure")
                break
            
            self._log("")
        
        # Print overall summary
        self._print_overall_summary(results)
        
        return results
    
    def _print_overall_summary(self, results: List[CycleResult]):
        """Print summary across multiple cycles."""
        self._log("")
        self._log("=" * 70)
        self._log("OVERALL EVOLUTION SUMMARY")
        self._log("=" * 70)
        self._log("")
        
        total_tested = sum(r.refinements_tested for r in results)
        total_integrated = sum(r.refinements_integrated for r in results)
        total_rejected = sum(r.refinements_rejected for r in results)
        
        self._log(f"Total cycles:           {len(results)}")
        self._log(f"Successful cycles:      {sum(1 for r in results if r.status == CycleStatus.COMPLETED)}")
        self._log(f"Failed cycles:          {sum(1 for r in results if r.status == CycleStatus.FAILED)}")
        self._log("")
        self._log(f"Total refinements tested:     {total_tested}")
        self._log(f"Total refinements integrated: {total_integrated}")
        self._log(f"Total refinements rejected:   {total_rejected}")
        
        if total_tested > 0:
            success_rate = total_integrated / total_tested * 100
            self._log(f"Overall success rate:         {success_rate:.1f}%")
        
        # Improvement from first to last cycle
        if len(results) >= 2:
            first = results[0]
            last = results[-1]
            
            if first.baseline_mean_sigma and last.final_mean_sigma:
                total_sigma_improvement = first.baseline_mean_sigma - last.final_mean_sigma
                self._log("")
                self._log(f"Total σ improvement:    {total_sigma_improvement:+.3f}")
        
        self._log("")
        self._log("=" * 70)
    
    def get_cycle_history(self) -> List[CycleResult]:
        """Get history of all evolution cycles."""
        return self._cycle_history
    
    def export_results(self, output_path: Optional[str] = None) -> str:
        """
        Export cycle results to JSON.
        
        Args:
            output_path: Path to output file (default: cycle_results.json)
        
        Returns:
            Path to output file
        """
        if output_path is None:
            output_path = "cycle_results.json"
        
        # Normalize to string in case a Path object is provided
        output_path_str = str(output_path)
        
        results_dict = {
            "generated": datetime.now().isoformat(),
            "total_cycles": len(self._cycle_history),
            "cycles": [r.to_dict() for r in self._cycle_history],
        }
        
        try:
            with open(output_path_str, 'w', encoding='utf-8') as f:
                json.dump(results_dict, f, indent=2)
        except (OSError, TypeError, ValueError) as e:
            error_msg = (
                f"Failed to export evolution cycle results to "
                f"'{output_path_str}': {e}"
            )
            # Best-effort logging; do not let logging failures mask the original error
            try:
                self._log(error_msg)
            except Exception:
                pass
            raise RuntimeError(error_msg) from e
        
        return output_path_str
    
    def to_dict(self) -> Dict:
        """Return orchestrator configuration as dictionary."""
        return {
            "sigma_tolerance": self.integrator.regression_tester.sigma_tolerance,
            "verbose": self.verbose,
            "cycles_run": len(self._cycle_history),
            "doc_updater": self.doc_updater.to_dict(),
        }


def main():
    """Command-line interface for evolution cycles."""
    parser = argparse.ArgumentParser(
        description="Run IRH Theory Evolution Cycles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run single cycle with default settings
  python -m evolution_system.evolution_cycle
  
  # Run 3 cycles with 10 refinements each
  python -m evolution_system.evolution_cycle --cycles 3 --max-refinements 10
  
  # Auto-integrate successful refinements
  python -m evolution_system.evolution_cycle --auto-integrate
  
  # Export results to custom path
  python -m evolution_system.evolution_cycle --output results/cycle_$(date +%Y%m%d).json
"""
    )
    
    parser.add_argument(
        "--cycles", "-c",
        type=int,
        default=1,
        help="Number of evolution cycles to run (default: 1)"
    )
    
    parser.add_argument(
        "--max-refinements", "-m",
        type=int,
        default=5,
        help="Maximum refinements to test per cycle (default: 5)"
    )
    
    parser.add_argument(
        "--auto-integrate", "-a",
        action="store_true",
        help="Automatically integrate successful refinements"
    )
    
    parser.add_argument(
        "--sigma-tolerance", "-s",
        type=float,
        default=0.5,
        help="Maximum allowed σ regression (default: 0.5)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="cycle_results.json",
        help="Output path for results JSON (default: cycle_results.json)"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress output"
    )
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = EvolutionCycle(
        sigma_tolerance=args.sigma_tolerance,
        verbose=not args.quiet
    )
    
    # Run cycles
    if args.cycles == 1:
        result = orchestrator.run(
            max_refinements=args.max_refinements,
            auto_integrate=args.auto_integrate
        )
        results = [result]
    else:
        results = orchestrator.run_multiple(
            num_cycles=args.cycles,
            max_refinements_per_cycle=args.max_refinements,
            auto_integrate=args.auto_integrate
        )
    
    # Export results
    output_path = orchestrator.export_results(args.output)
    print(f"\nResults exported to: {output_path}")
    
    # Return exit code based on cycle status
    if all(r.status == CycleStatus.COMPLETED for r in results):
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
