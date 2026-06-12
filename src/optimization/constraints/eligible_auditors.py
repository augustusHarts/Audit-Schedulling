from __future__ import annotations
from ortools.sat.python import cp_model
import pandas as pd

def add_eligibility_constraint(
    model: cp_model.CpModel,
    variables: dict,
    eligibility_df: pd.DataFrame,
) -> None:
    """
    Eligibility is enforced by only creating
    variables for eligible pairs.

    This function exists to keep the
    optimization architecture consistent.
    """

    return