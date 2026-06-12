from src.utils.models import SystemData, MasterDatasets
from src.utils.decorators.logger import log_stage
from src.master.circle_master import CircleMasterBuilder
from src.master.working_calendar import CalendarBuilder
from src.master.duration_map import DurationMasterBuilder
from src.master.auditor_data import AuditorMasterBuilder
from src.master.branch_data import BranchMasterBuilder
from src.master.history_data import AuditorHistoryMasterBuilder
from src.master.audit_job import AuditJobBuilder

class MasterPipeline:

    @log_stage("Master Pipeline")
    def run(
        self,
        data: SystemData
    ):

        circle_master = CircleMasterBuilder().build(
            auditors=data.auditors,
            branches=data.branches,
            history=data.history,
        )

        auditor_master = AuditorMasterBuilder().build(
            auditors=data.auditors
        )

        branch_master = BranchMasterBuilder().build(
            branches=data.branches,
            lat_long=data.lat_long
        )

        history_master = AuditorHistoryMasterBuilder().build(
            history=data.history
        )

        duration_map_master = DurationMasterBuilder().build()

        audit_job_master = AuditJobBuilder().build(
            branches=data.branches,
            duration_master=duration_map_master
        )
        
        return MasterDatasets(
            circle_master=circle_master,
            auditor_data=auditor_master,
            branch_data=branch_master,
            history_data=history_master,
            duration_map=duration_map_master,
            audit_job=audit_job_master
        )