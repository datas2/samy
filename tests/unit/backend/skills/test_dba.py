from backend.skills.dba.backup_restore import BackupRestoreSkill
from backend.skills.dba.clustering import ClusteringSkill
from backend.skills.dba.indexes import IndexesSkill
from backend.skills.dba.migration import MigrationSkill
from backend.skills.dba.modeling import ModelingSkill
from backend.skills.dba.partitioning import PartitioningSkill
from backend.skills.dba.postgres import PostgresSkill
from backend.skills.dba.replication import ReplicationSkill
from backend.skills.dba.vaccum import VacuumSkill


def test_indexes_skill_review_architecture_basic():
    skill = IndexesSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.review_architecture(
        description="Tabela de logs com colunas (id, user_id, created_at, action).",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_backup_restore_skill_review_architecture_basic():
    skill = BackupRestoreSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.review_architecture(
        description="Cluster com necessidade de RPO de 5 minutos e RTO de 30 minutos.",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_clustering_skill_review_architecture_basic():
    skill = ClusteringSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.review_architecture(
        description="Ambiente distribuído com sharding por região.",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_migration_skill_review_architecture_basic():
    skill = MigrationSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.review_architecture(
        description="Migração de Oracle para Postgres em ambiente crítico.",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_modeling_skill_review_architecture_basic():
    skill = ModelingSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.review_architecture(
        description="Modelo OLTP para sistema de e-commerce.",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_partitioning_skill_review_architecture_basic():
    skill = PartitioningSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.review_architecture(
        description="Tabela de eventos particionada por mês com alto volume de inserts.",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_postgres_skill_review_architecture_basic():
    skill = PostgresSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.review_architecture(
        description="Arquitetura multi-tenant usando Postgres como banco principal.",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_replication_skill_review_architecture_basic():
    skill = ReplicationSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.review_architecture(
        description="Replica assíncrona entre duas zonas de disponibilidade.",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_vacuum_skill_review_architecture_basic():
    skill = VacuumSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.review_architecture(
        description="Base com problemas de bloat e autovacuum desabilitado.",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0