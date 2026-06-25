from backend.skills.gcp.bigquery import BigQuerySkill
from backend.skills.gcp.cloudrun import CloudRunSkill
from backend.skills.gcp.cloudsql import CloudSQLSkill
from backend.skills.gcp.composer import ComposerSkill
from backend.skills.gcp.cost_analysis import GcpCostAnalysisSkill
from backend.skills.gcp.dataflow import DataflowSkill
from backend.skills.gcp.datastream import DatastreamSkill
from backend.skills.gcp.iam import IAMSkill
from backend.skills.gcp.monitoring import GcpMonitoringSkill
from backend.skills.gcp.observability import GcpObservabilitySkill
from backend.skills.gcp.pubsub import PubSubSkill
from backend.skills.gcp.security import GcpSecuritySkill


def test_bigquery_skill_optimize_basic():
    skill = BigQuerySkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.optimize(
        description="Consulta com CROSS JOIN sem filtro.",
        context={"dataset": "analytics"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_cloudrun_skill_optimize_basic():
    skill = CloudRunSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.optimize(
        description="Serviço HTTP com alta latência sob carga.",
        context={"service": "api-gateway"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_cloudsql_skill_optimize_basic():
    skill = CloudSQLSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.optimize(
        description="Instância com CPU alta e muitas conexões.",
        context={"engine": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_composer_skill_optimize_basic():
    skill = ComposerSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.optimize(
        description="DAGs longas com dependências complexas.",
        context={"env": "prod"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_cost_analysis_skill_optimize_basic():
    skill = GcpCostAnalysisSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.optimize(
        description="Gastos concentrados em BigQuery e Dataflow.",
        context={"project": "meu-projeto"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_dataflow_skill_optimize_basic():
    skill = DataflowSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.optimize(
        description="Job de streaming com alto custo e latência variável.",
        context={"job_name": "events-stream"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_datastream_skill_optimize_basic():
    skill = DatastreamSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.optimize(
        description="Replicação de base OLTP para BigQuery via Datastream.",
        context={"source": "mysql"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_iam_skill_optimize_basic():
    skill = IAMSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.optimize(
        description="Muitos owners em um único projeto.",
        context={"project": "meu-projeto"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_monitoring_skill_optimize_basic():
    skill = GcpMonitoringSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.optimize(
        description="Alertas disparando com muito ruído.",
        context={"project": "meu-projeto"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_observability_skill_optimize_basic():
    skill = GcpObservabilitySkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.optimize(
        description="Muito volume de logs em Cloud Logging.",
        context={"project": "meu-projeto"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_pubsub_skill_optimize_basic():
    skill = PubSubSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.optimize(
        description="Tópico com muitos consumidores lentos e fila crescendo.",
        context={"topic": "events"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_security_skill_optimize_basic():
    skill = GcpSecuritySkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.optimize(
        description="Múltiplos projetos com poucas barreiras entre ambientes.",
        context={"org": "minha-org"},
    )

    assert isinstance(result, str)
    assert len(result) > 0