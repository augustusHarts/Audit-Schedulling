from dataclasses import dataclass, field
import pandas as pd
from datetime import datetime

@dataclass
class SystemData:
    auditors: pd.DataFrame
    holidays: pd.DataFrame
    branches: pd.DataFrame
    history: pd.DataFrame
    lat_long: pd.DataFrame

#-----Master Datasets-----
@dataclass
class CircleData:
    circle_id: str
    circle_name: str
    branch_count: int = 0
    auditor_count: int = 0
    present_in_auditors: bool = False
    present_in_branches: bool = False
    present_in_history: bool = False

@dataclass
class AuditorData:
    auditor_id: str
    parent_circle: str
    circles_worked_earlier: list[str]   

@dataclass
class BranchData:
    br_code: str
    br_name: str
    circle: str
    category: bool
    eligible_from_date: datetime
    latitude: float
    longitude: float

@dataclass
class AuditorHistoryData:
    auditor_id: str
    branch_code: str
    audit_start_date: datetime
    audit_end_date: datetime
    circle: str

@dataclass
class EligibilityContext:
    auditor_master: pd.DataFrame
    branch_master: pd.DataFrame
    auditor_history_master: pd.DataFrame
    working_calendar_master: pd.DataFrame

@dataclass
class MasterDatasets:
    circle_master: pd.DataFrame
    auditor_data: pd.DataFrame
    branch_data: pd.DataFrame
    history_data: pd.DataFrame
    duration_map: pd.DataFrame
    audit_job: pd.DataFrame

@dataclass
class EligibilityLookup:
    repeat_map: dict[str, set[str]]
    last5_map: dict[str, set[str]]

@dataclass
class DurationMap:
    category: str
    audit_days: int

@dataclass
class AuditJobData:
    job_id: str
    branch_code: str
    audit_type: str
    audit_days: int
    eligible_from_date: datetime

#-----Optimization-----
@dataclass(slots=True)
class AssignmentResult:
    auditor_id: str
    branch_code: str