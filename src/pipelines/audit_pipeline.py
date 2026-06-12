from src.utils.logger import get_logger
from src.utils.decorators.logger import log_stage
from src.utils.decorators.error_handling import error_handling
from src.utils.models import SystemData
from src.ingestion.load_excel import load
from src.utils.config import FILE_MAP
from src.pipelines.preprocess_pipeline import preprocess_data
from src.pipelines.master_pipeline import MasterPipeline
from src.pipelines.optimization_pipeline import OptimizationPipeline
from src.eligibility.engine import EligibilityEngine
from src.eligibility.lookup_builder import LookupBuilder
from src.utils.models import SystemData

logger = get_logger(__name__)

class AuditPipeline:  

    @error_handling
    def load_data(self) -> SystemData:
        data = SystemData(
            **{
                key: load(file_name)
                for key, file_name in FILE_MAP.items()
            }
        )
        return data

    @log_stage('Audit Pipeline')
    def run_pipeline(self) -> None:

        raw_data = self.load_data()
        
        clean_data = preprocess_data(raw_data)

        master_data = MasterPipeline().run(clean_data)

        lookup = LookupBuilder().build(
            master_data.history_data
        )

        eligibility = (
            EligibilityEngine(
                lookup
            )
            .build(
                master_data.auditor_data,
                master_data.branch_data,
            )
        )

        optimization = OptimizationPipeline().run(
                            eligibility,
                            master_data.audit_job)

