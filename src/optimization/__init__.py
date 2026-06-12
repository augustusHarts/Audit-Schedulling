"""Optimization module for audit assignment scheduling.

This module contains the constraint satisfaction problem (CSP) solver
for optimally assigning auditors to branches with balanced workloads.

Main components:
- variables: Decision variables for auditor-branch assignments
- constraints: Business logic constraints (eligibility, one auditor per branch)
- objectives: Optimization objectives (workload balancing)
- optimizer: Main orchestrator that builds and solves the model
- solver: Wrapper around OR-Tools solver
"""

from src.optimization.optimizer import AssignmentOptimizer

__all__ = ["AssignmentOptimizer"]
