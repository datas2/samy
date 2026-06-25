from __future__ import annotations

from typing import Any, Dict, Type

from backend.llm.ollama_client import OllamaClient
from backend.rag.retriever import KnowledgeRetriever
from backend.services.telemetry_service import TelemetryService

# SQL
from backend.skills.sql.explain import SQLExplainSkill
from backend.skills.sql.review import SQLReviewSkill
from backend.skills.sql.optimize import SQLOptimizeSkill

# Python
from backend.skills.python.refactor import PythonRefactorSkill
from backend.skills.python.review import PythonReviewSkill
from backend.skills.python.tests import PythonTestsSkill
from backend.skills.python.docstring import PythonDocstringSkill
from backend.skills.python.code import PythonCodeGenerationSkill
from backend.skills.python.fastapi import PythonFastAPISkill

# Go
from backend.skills.golang.tests import GoTestsSkill
from backend.skills.golang.review import GoReviewSkill
from backend.skills.golang.concurrency import GoConcurrencySkill

# GCP
from backend.skills.gcp.bigquery import BigQuerySkill
from backend.skills.gcp.cloudrun import CloudRunSkill
from backend.skills.gcp.cloudsql import CloudSQLSkill
from backend.skills.gcp.composer import ComposerSkill
from backend.skills.gcp.dataflow import DataflowSkill
from backend.skills.gcp.datastream import DatastreamSkill
from backend.skills.gcp.iam import IAMSkill
from backend.skills.gcp.pubsub import PubSubSkill
from backend.skills.gcp.security import GcpSecuritySkill
from backend.skills.gcp.monitoring import GcpMonitoringSkill
from backend.skills.gcp.observability import GcpObservabilitySkill
from backend.skills.gcp.cost_analysis import GcpCostAnalysisSkill

# DBA
from backend.skills.dba.clustering import ClusteringSkill
from backend.skills.dba.indexes import IndexesSkill
from backend.skills.dba.modeling import ModelingSkill
from backend.skills.dba.partitioning import PartitioningSkill
from backend.skills.dba.postgres import PostgresSkill
from backend.skills.dba.vaccum import VacuumSkill
from backend.skills.dba.replication import ReplicationSkill
from backend.skills.dba.backup_restore import BackupRestoreSkill
from backend.skills.dba.migration import MigrationSkill

# Analytics
from backend.skills.analytics.dashboard import DashboardSkill
from backend.skills.analytics.kpi import KpiSkill
from backend.skills.analytics.metrics import MetricsSkill


class SkillRegistry:
    """Central registry for all Samy skills.

    This registry maps (domain, skill) names to concrete skill classes and
    provides a factory to instantiate them with shared dependencies.
    """

    def __init__(self) -> None:
        self._retriever = KnowledgeRetriever()
        self._llm_client = OllamaClient()
        self._telemetry = TelemetryService()

        # (domain, skill) -> class
        self._registry: Dict[tuple[str, str], Type[Any]] = {
            # SQL
            ("sql", "explain"): SQLExplainSkill,
            ("sql", "review"): SQLReviewSkill,
            ("sql", "optimize"): SQLOptimizeSkill,
            
            # Python
            ("python", "refactor"): PythonRefactorSkill,
            ("python", "review"): PythonReviewSkill,
            ("python", "tests"): PythonTestsSkill,
            ("python", "docstring"): PythonDocstringSkill,
            ("python", "code"): PythonCodeGenerationSkill,
            ("python", "fastapi"): PythonFastAPISkill,
            
            # Go
            ("go", "tests"): GoTestsSkill,
            ("go", "review"): GoReviewSkill,
            ("go", "concurrency"): GoConcurrencySkill,
            
            # GCP
            ("gcp", "bigquery"): BigQuerySkill,
            ("gcp", "cloudrun"): CloudRunSkill,
            ("gcp", "cloudsql"): CloudSQLSkill,
            ("gcp", "composer"): ComposerSkill,
            ("gcp", "dataflow"): DataflowSkill,
            ("gcp", "datastream"): DatastreamSkill,
            ("gcp", "iam"): IAMSkill,
            ("gcp", "pubsub"): PubSubSkill,
            ("gcp", "security"): GcpSecuritySkill,
            ("gcp", "monitoring"): GcpMonitoringSkill,
            ("gcp", "observability"): GcpObservabilitySkill,
            ("gcp", "cost_analysis"): GcpCostAnalysisSkill,
            
            # DBA
            ("dba", "clustering"): ClusteringSkill,
            ("dba", "indexes"): IndexesSkill,
            ("dba", "modeling"): ModelingSkill,
            ("dba", "partitioning"): PartitioningSkill,
            ("dba", "postgres"): PostgresSkill,
            ("dba", "vacuum"): VacuumSkill,
            ("dba", "replication"): ReplicationSkill,
            ("dba", "backup_restore"): BackupRestoreSkill,
            ("dba", "migration"): MigrationSkill,
            
            # Analytics
            ("analytics", "dashboard"): DashboardSkill,
            ("analytics", "kpi"): KpiSkill,
            ("analytics", "metrics"): MetricsSkill,
        }

    def get_skill(self, domain: str, skill: str) -> Any:
        """Instantiate a skill for a given domain and name."""
        key = (domain.lower(), skill.lower())
        cls = self._registry.get(key)
        if cls is None:
            raise ValueError(f"Skill not found for domain='{domain}', skill='{skill}'")

        # domains that use retriever
        domains_with_retriever = {"sql", "gcp", "dba", "analytics"}

        init_kwargs: Dict[str, Any] = {
            "llm_client": self._llm_client,
            "telemetry": self._telemetry,
        }

        if domain.lower() in domains_with_retriever:
            init_kwargs["retriever"] = self._retriever

        return cls(**init_kwargs)