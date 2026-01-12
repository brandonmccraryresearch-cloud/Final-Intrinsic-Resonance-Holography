"""
Documentation Updater Module for IRH Theory Evolution System

Phase 3 Implementation: Automated documentation updates for integrated refinements.

This module provides:
- Automatic changelog generation for successful refinements
- Theory document version bumping
- Integration history reporting
- Refinement documentation templates

**Key Principle:** When a refinement is integrated, all relevant documentation
must be updated to maintain full traceability of theoretical development.

Usage:
    from evolution_system import DocumentationUpdater, IntegrationResult
    
    # After successful integration
    updater = DocumentationUpdater()
    updater.update_changelog(result)
    updater.update_theory_version("26.1")
    updater.generate_refinement_report(result)

Author: IRH Computational Research Team
Date: 2026-01-09
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import json


@dataclass
class ChangelogEntry:
    """A single entry in the theory changelog."""
    version: str
    date: str
    refinement_name: str
    description: str
    affected_observables: List[str]
    improvement_pct: float
    topological_origin: str
    
    # Validation details
    regression_tests_passed: int
    symmetries_preserved: List[str]
    
    # Links
    theory_reference: Optional[str] = None
    notebook_reference: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "version": self.version,
            "date": self.date,
            "refinement_name": self.refinement_name,
            "description": self.description,
            "affected_observables": self.affected_observables,
            "improvement_pct": self.improvement_pct,
            "topological_origin": self.topological_origin,
            "regression_tests_passed": self.regression_tests_passed,
            "symmetries_preserved": self.symmetries_preserved,
            "theory_reference": self.theory_reference,
            "notebook_reference": self.notebook_reference,
        }
    
    def to_markdown(self) -> str:
        """Convert to markdown format for changelog."""
        lines = [
            f"## Version {self.version} ({self.date})",
            "",
            f"### {self.refinement_name}",
            "",
            f"**Description:** {self.description}",
            "",
            f"**Topological Origin:** {self.topological_origin}",
            "",
            f"**Affected Observables:** {', '.join(self.affected_observables)}",
            "",
            f"**Improvement:** {self.improvement_pct:.2f}% average improvement",
            "",
            "**Validation:**",
            f"- Regression tests passed: {self.regression_tests_passed}",
            f"- Symmetries preserved: {', '.join(self.symmetries_preserved)}",
            "",
        ]
        
        if self.theory_reference:
            lines.append(f"**Theory Reference:** {self.theory_reference}")
            lines.append("")
        
        if self.notebook_reference:
            lines.append(f"**Notebook:** {self.notebook_reference}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        
        return "\n".join(lines)


class DocumentationUpdater:
    """
    Updates documentation when refinements are integrated.
    
    Manages:
    - CHANGELOG.md: History of theory refinements
    - Version tracking in theory documents
    - Integration reports
    - Refinement documentation
    """
    
    def __init__(self, repo_root: Optional[str] = None):
        """
        Initialize documentation updater.
        
        Args:
            repo_root: Path to repository root. Auto-detected if None.
        """
        if repo_root is None:
            # Try to find repository root
            current = Path(__file__).parent.parent
            if (current / ".git").exists():
                repo_root = str(current)
            else:
                repo_root = str(Path.cwd())
        
        self.repo_root = Path(repo_root)
        self.changelog_path = self.repo_root / "CHANGELOG.md"
        self.theory_changelog_path = self.repo_root / "docs" / "THEORY_CHANGELOG.md"
        self.integration_history_path = self.repo_root / "docs" / "integration_history.json"
        
        # Current theory version
        self._current_version: Optional[str] = None
    
    def get_current_version(self) -> str:
        """
        Get the current theory version from documentation.
        
        Returns:
            Current version string (e.g., "26.0")
        """
        if self._current_version:
            return self._current_version
        
        # Try to read from README.md
        readme_path = self.repo_root / "README.md"
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Look for version pattern in title or header
                import re
                version_match = re.search(r'v(\d+\.\d+(?:\.\d+)?)', content, re.IGNORECASE)
                if version_match:
                    self._current_version = version_match.group(1)
                    return self._current_version
        
        # Default version
        self._current_version = "26.0"
        return self._current_version
    
    def increment_version(self, current: str, release_type: str = "patch") -> str:
        """
        Increment version number.
        
        Args:
            current: Current version (e.g., "26.0" or "26.0.1").
            release_type: Type of release ("major", "minor", "patch").
        
        Returns:
            New version string.
        
        Raises:
            ValueError: If the current version string is not of the form "X.Y" or "X.Y.Z"
                with integer components.
        """
        parts = current.split(".")

        try:
            if len(parts) == 2:
                major, minor = int(parts[0]), int(parts[1])
                patch = 0
            elif len(parts) == 3:
                major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
            else:
                raise ValueError(
                    f"Invalid version string '{current}': expected 'X.Y' or 'X.Y.Z'."
                )
        except ValueError as exc:
            # Normalize any integer-conversion errors into a clear message
            raise ValueError(
                f"Invalid version string '{current}': expected 'X.Y' or 'X.Y.Z' "
                f"with integer components."
            ) from exc
        
        if release_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif release_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        if patch == 0:
            return f"{major}.{minor}"
        return f"{major}.{minor}.{patch}"
    
    def create_changelog_entry(
        self,
        result: 'IntegrationResult',
        suggestion: 'RefinementSuggestion',
        new_version: Optional[str] = None
    ) -> ChangelogEntry:
        """
        Create a changelog entry from an integration result.
        
        Args:
            result: IntegrationResult from successful integration
            suggestion: RefinementSuggestion that was integrated
            new_version: New version string (auto-incremented if None)
        
        Returns:
            ChangelogEntry ready for documentation
        """
        if new_version is None:
            current = self.get_current_version()
            new_version = self.increment_version(current, "patch")
        
        modification = suggestion.modification
        
        return ChangelogEntry(
            version=new_version,
            date=datetime.now().strftime("%Y-%m-%d"),
            refinement_name=modification.name,
            description=modification.expected_improvement,
            affected_observables=modification.affected_observables,
            improvement_pct=result.target_improvement_pct,
            topological_origin=modification.topological_basis.split('\n')[0].strip(),
            regression_tests_passed=len([t for t in result.regression_tests if t.passed]),
            symmetries_preserved=modification.symmetries_preserved,
            theory_reference=f"IRH v{new_version}",
            notebook_reference=f"notebooks/refinement_{modification.refinement_type.value}.ipynb",
        )
    
    def update_changelog(
        self,
        entry: ChangelogEntry,
        target_path: Optional[Path] = None
    ) -> bool:
        """
        Update the theory changelog with a new entry.
        
        Args:
            entry: ChangelogEntry to add
            target_path: Path to changelog file (default: docs/THEORY_CHANGELOG.md)
        
        Returns:
            True if successful, False if an I/O error occurred.
        """
        if target_path is None:
            target_path = self.theory_changelog_path
        
        try:
            # Ensure parent directory exists
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Read existing changelog or create header
            if target_path.exists():
                with open(target_path, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
            else:
                existing_content = self._create_changelog_header()
            
            # Find insertion point (after header)
            header_end = existing_content.find("\n## Version ")
            if header_end == -1:
                # No existing versions, append after header
                new_content = existing_content + "\n" + entry.to_markdown()
            else:
                # Insert new entry before existing versions
                new_content = (
                    existing_content[:header_end] +
                    "\n" +
                    entry.to_markdown() +
                    existing_content[header_end:]
                )
            
            # Write updated changelog
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        except (OSError, IOError) as e:
            # Surface a clear failure signal to callers without raising.
            # For richer diagnostics, callers can inspect logs or wrap this method.
            print(f"Failed to update changelog at {target_path}: {e}")
            return False
        
        return True
    
    def _create_changelog_header(self) -> str:
        """Create the changelog file header."""
        return """# IRH Theory Changelog

This document tracks all refinements integrated into the IRH theoretical framework
through the Theory Evolution System.

**Directive A Compliance:** All refinements have verified topological origin.
No phenomenological parameters have been introduced.

**Validation Protocol:** Each refinement passes regression testing to ensure
no degradation of existing predictions.

---

"""
    
    def update_integration_history(
        self,
        result: 'IntegrationResult',
        suggestion: 'RefinementSuggestion'
    ) -> bool:
        """
        Update the JSON integration history file.
        
        Args:
            result: IntegrationResult from integration attempt
            suggestion: RefinementSuggestion that was tested/integrated
        
        Returns:
            True if successful, False if an I/O or JSON error occurred.
        """
        try:
            # Load existing history
            if self.integration_history_path.exists():
                try:
                    with open(self.integration_history_path, 'r', encoding='utf-8') as f:
                        history = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Failed to parse integration history at {self.integration_history_path}: {e}")
                    # Start fresh if the file is corrupted
                    history = None
            else:
                history = None
            
            if history is None:
                history = {
                    "version": "1.0",
                    "generated": datetime.now().isoformat(),
                    "total_attempts": 0,
                    "total_integrated": 0,
                    "total_rejected": 0,
                    "entries": []
                }
            
            # Create new entry
            entry = {
                "timestamp": datetime.now().isoformat(),
                "refinement_name": suggestion.modification.name,
                "refinement_type": suggestion.modification.refinement_type.value,
                "status": result.status.value,
                "rejection_reason": result.rejection_reason.value if result.rejection_reason else None,
                "target_improved": result.target_improved,
                "improvement_pct": result.target_improvement_pct,
                "regressions_found": result.regressions_found,
                "symmetries_preserved": result.symmetries_preserved,
                "topological_verified": result.topological_origin_verified,
                "affected_observables": suggestion.modification.affected_observables,
            }
            
            # Update statistics
            history["total_attempts"] += 1
            if result.status.value == "integrated":
                history["total_integrated"] += 1
            elif result.status.value == "rejected":
                history["total_rejected"] += 1
            
            history["entries"].append(entry)
            history["last_updated"] = datetime.now().isoformat()
            
            # Ensure parent directory exists
            self.integration_history_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write updated history
            with open(self.integration_history_path, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2)
            
            return True
            
        except (OSError, IOError) as e:
            print(f"Failed to update integration history at {self.integration_history_path}: {e}")
            return False
        except (TypeError, ValueError) as e:
            print(f"Failed to serialize integration history entry: {e}")
            return False
    
    def generate_refinement_report(
        self,
        result: 'IntegrationResult',
        suggestion: 'RefinementSuggestion',
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate a detailed refinement report.
        
        Args:
            result: IntegrationResult from integration
            suggestion: RefinementSuggestion that was processed
            output_path: Optional path to write report
        
        Returns:
            Report as formatted string
        """
        modification = suggestion.modification
        
        lines = [
            "=" * 70,
            "IRH THEORY REFINEMENT REPORT",
            "=" * 70,
            "",
            f"Refinement: {modification.name}",
            f"Status: {result.status.value.upper()}",
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "-" * 70,
            "MODIFICATION DETAILS",
            "-" * 70,
            "",
            f"Type: {modification.refinement_type.value}",
            f"Formula: {modification.mathematical_formula}",
            "",
            "Topological Basis:",
            *[f"  {line.strip()}" for line in modification.topological_basis.strip().split('\n')[:10]],
            "",
            f"Affected Observables: {', '.join(modification.affected_observables)}",
            f"Expected Improvement: {modification.expected_improvement}",
            "",
            "Derivation Steps:",
            *[f"  {step}" for step in modification.derivation_steps],
            "",
            "Symmetries Preserved:",
            *[f"  - {sym}" for sym in modification.symmetries_preserved],
            "",
            "-" * 70,
            "VALIDATION RESULTS",
            "-" * 70,
            "",
            f"Target Improved: {'YES' if result.target_improved else 'NO'}",
            f"Improvement: {result.target_improvement_pct:.2f}%",
            "",
            f"Regression Tests: {len(result.regression_tests)} total",
            f"Regressions Found: {result.regressions_found}",
            "",
            "Symmetry Checks:",
        ]
        
        for check in result.symmetry_checks:
            status = "✓" if check.preserved else "✗"
            lines.append(f"  {status} {check.symmetry_name}")
        
        lines.extend([
            "",
            f"Topological Origin Verified: {'YES' if result.topological_origin_verified else 'NO'}",
            "",
        ])
        
        if result.notes:
            lines.extend([
                "-" * 70,
                "NOTES",
                "-" * 70,
                "",
                *[f"  • {note}" for note in result.notes],
                "",
            ])
        
        lines.extend([
            "=" * 70,
            "END OF REPORT",
            "=" * 70,
        ])
        
        report = "\n".join(lines)
        
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
        
        return report
    
    def generate_summary_statistics(self) -> Dict:
        """
        Generate summary statistics from integration history.
        
        Returns:
            Dictionary with statistics
        """
        if not self.integration_history_path.exists():
            return {
                "total_attempts": 0,
                "total_integrated": 0,
                "total_rejected": 0,
                "success_rate": 0.0,
                "by_refinement_type": {},
                "by_rejection_reason": {},
            }
        
        with open(self.integration_history_path, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        # Calculate statistics
        entries = history.get("entries", [])
        
        by_type = {}
        by_reason = {}
        total_improvement = 0.0
        improvement_count = 0
        
        for entry in entries:
            # By refinement type
            rtype = entry.get("refinement_type", "unknown")
            if rtype not in by_type:
                by_type[rtype] = {"total": 0, "integrated": 0, "rejected": 0}
            by_type[rtype]["total"] += 1
            if entry.get("status") == "integrated":
                by_type[rtype]["integrated"] += 1
            elif entry.get("status") == "rejected":
                by_type[rtype]["rejected"] += 1
            
            # By rejection reason
            reason = entry.get("rejection_reason")
            if reason:
                by_reason[reason] = by_reason.get(reason, 0) + 1
            
            # Average improvement
            if entry.get("status") == "integrated":
                total_improvement += entry.get("improvement_pct", 0)
                improvement_count += 1
        
        success_rate = (
            history.get("total_integrated", 0) / history.get("total_attempts", 1) * 100
            if history.get("total_attempts", 0) > 0 else 0.0
        )
        
        avg_improvement = (
            total_improvement / improvement_count
            if improvement_count > 0 else 0.0
        )
        
        return {
            "total_attempts": history.get("total_attempts", 0),
            "total_integrated": history.get("total_integrated", 0),
            "total_rejected": history.get("total_rejected", 0),
            "success_rate": success_rate,
            "average_improvement_pct": avg_improvement,
            "by_refinement_type": by_type,
            "by_rejection_reason": by_reason,
        }
    
    def print_summary(self):
        """Print a human-readable summary of integration history."""
        stats = self.generate_summary_statistics()
        
        print("=" * 60)
        print("IRH THEORY EVOLUTION SUMMARY")
        print("=" * 60)
        print()
        print(f"Total Integration Attempts:  {stats['total_attempts']}")
        print(f"Successfully Integrated:     {stats['total_integrated']}")
        print(f"Rejected:                    {stats['total_rejected']}")
        print(f"Success Rate:                {stats['success_rate']:.1f}%")
        print()
        
        if stats.get('average_improvement_pct', 0) > 0:
            print(f"Average Improvement:         {stats['average_improvement_pct']:.2f}%")
            print()
        
        if stats['by_refinement_type']:
            print("By Refinement Type:")
            for rtype, counts in stats['by_refinement_type'].items():
                print(f"  {rtype}: {counts['total']} attempts, "
                      f"{counts['integrated']} integrated, "
                      f"{counts['rejected']} rejected")
            print()
        
        if stats['by_rejection_reason']:
            print("Rejection Reasons:")
            for reason, count in stats['by_rejection_reason'].items():
                print(f"  {reason}: {count}")
            print()
        
        print("=" * 60)
    
    def to_dict(self) -> Dict:
        """Return updater configuration as dictionary."""
        return {
            "repo_root": str(self.repo_root),
            "changelog_path": str(self.theory_changelog_path),
            "history_path": str(self.integration_history_path),
            "current_version": self.get_current_version(),
        }
