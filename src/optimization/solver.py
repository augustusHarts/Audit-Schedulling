from ortools.sat.python import cp_model

def solve_model(
    model
):

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30
    solver.parameters.num_search_workers = 8
    
    status = solver.Solve(
        model
    )

    return solver, status