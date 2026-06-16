# Audit Scheduling Optimization System

## Purpose

This project optimizes quarterly audit assignments and scheduling for internal auditors.

The optimization is performed in multiple phases:

1. Data Ingestion
2. Data Preprocessing
3. Master Dataset Construction
4. Eligibility Engine
5. Assignment Optimization
6. Scheduling Optimization
7. Future Iterative Improvements

---

# Project Principles

## 1. Keep Business Logic Separate

Never place business rules inside pipelines.

Business rules belong in:

* preprocessing/
* master/
* eligibility/
* optimization/

Pipelines should only orchestrate execution.

---

## 2. Prefer Small Builders

Each master dataset should have its own builder.

Examples:

* CircleMasterBuilder
* BranchMasterBuilder
* AuditJobBuilder
* DurationMasterBuilder
* CalendarBuilder

Avoid large monolithic builders.

---

## 3. Optimization Architecture

Optimization must be decomposed into:

optimization/

* variables.py
* constraints/
* objectives/
* solver.py
* optimizer.py

Constraints and objectives should never be embedded directly inside optimizer.py.

---

## 4. Iterative Improvement Strategy

Do NOT solve the entire business problem in one optimization model.

Implement optimization in phases.

### Phase 1

Assignment Optimization

Goal:

Assign auditors to branches.

Constraints:

* Auditor eligibility
* One auditor per branch
* Auditor workload capacity

Objective:

* Balance workload

Output:

audit_assignment.csv

---

### Phase 2

Scheduling Optimization

Goal:

Create audit start and end dates.

Constraints:

* No overlap per auditor
* Respect commencement date
* Respect schedule horizon
* Respect working calendar

Output:

audit_schedule.csv

---

### Phase 3

Travel Optimization

Goal:

Reduce travel cost and travel time.

Possible objectives:

* Minimize total travel distance
* Minimize circle switching
* Cluster nearby branches

---

### Phase 4

Business Preference Optimization

Examples:

* Auditor familiarity
* Circle preference
* Branch priority
* Auditor seniority

---

# Data Naming Standards

Use standardized names everywhere.

## Branch

branch_code
branch_name
circle

Never use:

* br_code
* brn_code
* brnch_nbr
* circle_vertical
* circlename

outside preprocessing.

---

## Auditor

auditor_id

Never use:

* auditorid

outside preprocessing.

---

## Dates

Use pandas timestamps.

Examples:

deadline
commencement_date
start_date
end_date

Avoid raw string dates.

---

# Scheduling Rules

Quarter Horizon:

Q1:

2025-04-01
to
2025-06-30

Scheduling uses day offsets from quarter start.

Example:

2025-04-01 -> 0
2025-04-02 -> 1

---

# Capacity Rules

Assignment optimization must always respect scheduling feasibility.

Before scheduling:

sum(audit_days assigned to auditor)
<=
available auditor capacity

Never assign more work than can be scheduled.

---

# Coding Standards

## Logging

Use:

@log_stage

for pipeline stages.

Avoid excessive logging inside loops.

---

## Error Handling

Use:

@error_handling

for pipeline entry points.

Raise domain-specific exceptions.

Examples:

EmptyDatasetError
MissingColumnError
DuplicateValueError
DataValidationError

---

## Saving Outputs

Use:

@save_output

for generated datasets.

Avoid manual CSV exports inside business logic.

---

# Development Workflow

Whenever adding a new feature:

1. Define business rule.
2. Create master dataset if needed.
3. Create validation.
4. Add optimization constraint/objective.
5. Test feasibility.
6. Add KPI output.

Never skip feasibility checks.

---

# Current Optimization Roadmap

Completed:

* Data ingestion
* Data preprocessing
* Master datasets
* Eligibility engine
* Assignment optimization
* Workload balancing

In Progress:

* Scheduling optimization

Future:

* Travel optimization
* Holiday-aware scheduling
* Distance matrix
* Multi-objective optimization
* Iterative improvement framework
