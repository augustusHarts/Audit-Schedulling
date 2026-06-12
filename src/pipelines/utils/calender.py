from __future__ import annotations

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


class CalendarBuilder:

    def __init__(
        self,
        holidays_df: pd.DataFrame,
        start_date: pd.Timestamp,
        end_date: pd.Timestamp,
    ) -> None:

        self.holidays_df = holidays_df.copy()
        self.start_date = pd.Timestamp(start_date)
        self.end_date = pd.Timestamp(end_date)

    # ---------------------------------------------------------
    @staticmethod
    def _is_second_saturday(date: pd.Timestamp) -> bool:

        return (
            date.weekday() == 5
            and 8 <= date.day <= 14
        )

    # ---------------------------------------------------------
    @staticmethod
    def _is_fourth_saturday(date: pd.Timestamp) -> bool:

        return (
            date.weekday() == 5
            and 22 <= date.day <= 28
        )

    # ---------------------------------------------------------
    def build_base_calendar(self) -> pd.DataFrame:

        logger.info(
            "Building base calendar from %s to %s",
            self.start_date.date(),
            self.end_date.date(),
        )

        dates = pd.date_range(
            self.start_date,
            self.end_date,
            freq="D",
        )

        calendar = pd.DataFrame(
            {"date": dates}
        )

        calendar["weekday"] = calendar["date"].dt.day_name()

        calendar["is_sunday"] = (
            calendar["date"].dt.weekday == 6
        )

        calendar["is_second_sat"] = (
            calendar["date"]
            .apply(self._is_second_saturday)
        )

        calendar["is_fourth_sat"] = (
            calendar["date"]
            .apply(self._is_fourth_saturday)
        )

        return calendar

    # ---------------------------------------------------------
    def build_circle_calendar(self) -> pd.DataFrame:

        base = self.build_base_calendar()

        circles = (
            self.holidays_df["Calendr_Group"]
            .dropna()
            .str.upper()
            .str.strip()
            .unique()
        )

        logger.info(
            "Building working calendar for %s circles",
            len(circles),
        )

        frames = []

        for circle in circles:

            temp = base.copy()

            temp["state"] = circle

            holidays = set(
                self.holidays_df.loc[
                    self.holidays_df["Calendr_Group"]
                    .str.upper()
                    .str.strip()
                    .eq(circle),
                    "HolidayDate_dt",
                ]
            )

            temp["is_circle_holiday"] = (
                temp["date"].isin(holidays)
            )

            temp["is_working_day"] = ~(
                temp["is_sunday"]
                | temp["is_second_sat"]
                | temp["is_fourth_sat"]
                | temp["is_circle_holiday"]
            )

            frames.append(temp)

        calendar = pd.concat(
            frames,
            ignore_index=True,
        )

        logger.info(
            "Working calendar created: %s rows",
            len(calendar),
        )

        return calendar