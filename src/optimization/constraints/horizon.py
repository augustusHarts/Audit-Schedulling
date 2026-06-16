from __future__ import annotations

from ortools.sat.python import cp_model


def add_horizon_constraint(
    model: cp_model.CpModel,
    end_vars: dict,
    horizon: int,
) -> None:

    for end_var in end_vars.values():

        model.Add(
            end_var <= horizon
        )