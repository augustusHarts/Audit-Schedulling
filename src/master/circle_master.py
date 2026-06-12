from src.utils.models import CircleData
from src.utils.decorators.save_output import save_output
from src.utils.config import MASTER_DIR
import pandas as pd


class CircleMasterBuilder:

    def __init__(self):
        pass

    @save_output('circle_master', MASTER_DIR)
    def build(
        self,
        auditors: pd.DataFrame,
        branches: pd.DataFrame,
        history: pd.DataFrame,
    ) -> pd.DataFrame:

        circles = {}

        # -------------------------
        # Auditor circles
        # -------------------------

        auditor_counts = (
            auditors
            .groupby("parent_circle")
            .size()
            .to_dict()
        )

        for circle_name, count in auditor_counts.items():

            circles[circle_name] = CircleData(
                circle_id="",
                circle_name=str(circle_name),
                auditor_count=count,
                present_in_auditors=True,
            )

        # -------------------------
        # Branch circles
        # -------------------------

        branch_counts = (
            branches
            .groupby("circle")
            .size()
            .to_dict()
        )

        for circle_name, count in branch_counts.items():

            if circle_name not in circles:

                circles[circle_name] = CircleData(
                    circle_id="",
                    circle_name=str(circle_name),
                )

            circles[circle_name].branch_count = count
            circles[circle_name].present_in_branches = True

        # -------------------------
        # History circles
        # -------------------------

        history_circles = (
            history["circle"]
            .dropna()
            .unique()
        )

        for circle_name in history_circles:

            if circle_name not in circles:

                circles[circle_name] = CircleData(
                    circle_id="",
                    circle_name=circle_name
                )

            circles[circle_name].present_in_history = True

        # -------------------------
        # Generate IDs
        # -------------------------

        rows = []

        for idx, circle_name in enumerate(
            sorted(circles.keys()),
            start=1,
        ):

            circle = circles[circle_name]

            circle.circle_id = f"C{idx:03d}"

            rows.append(
                {
                    "circle_id": circle.circle_id,
                    "circle_name": circle.circle_name,
                    "branch_count": circle.branch_count,
                    "auditor_count": circle.auditor_count,
                    "present_in_auditors": circle.present_in_auditors,
                    "present_in_branches": circle.present_in_branches,
                    "present_in_history": circle.present_in_history,
                }
            )

        circle_master = pd.DataFrame(rows)

        return circle_master