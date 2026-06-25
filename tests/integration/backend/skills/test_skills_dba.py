import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


@pytest.mark.integration
def test_dba_indexes_review_architecture_endpoint_smoke():
    payload = {
        "description": "Tabela de pedidos com colunas (id, cliente_id, data, total).",
        "context": {"db": "postgres"},
    }

    response = client.post("/skills/dba/indexes/review_architecture", json=payload)

    assert response.status_code in {501, 400, 200}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_dba_backup_restore_review_architecture_endpoint_smoke():
    payload = {
        "description": "Cluster Postgres com backups diários e necessidade de PITR.",
        "context": {"db": "postgres"},
    }

    response = client.post("/skills/dba/backup_restore/review_architecture", json=payload)

    assert response.status_code in {501, 400, 200}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_dba_clustering_review_architecture_endpoint_smoke():
    payload = {
        "description": "Arquitetura com sharding para base de clientes.",
        "context": {"db": "postgres"},
    }

    response = client.post("/skills/dba/clustering/review_architecture", json=payload)

    assert response.status_code in {501, 400, 200}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_dba_migration_review_architecture_endpoint_smoke():
    payload = {
        "description": "Migração de on-prem para cloud gerenciada.",
        "context": {"db": "postgres"},
    }

    response = client.post("/skills/dba/migration/review_architecture", json=payload)

    assert response.status_code in {501, 400, 200}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_dba_modeling_review_architecture_endpoint_smoke():
    payload = {
        "description": "Modelagem de dados para sistema de billing recorrente.",
        "context": {"db": "postgres"},
    }

    response = client.post("/skills/dba/modeling/review_architecture", json=payload)

    assert response.status_code in {501, 400, 200}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_dba_partitioning_review_architecture_endpoint_smoke():
    payload = {
        "description": "Tabela de eventos com bilhões de linhas particionada por data.",
        "context": {"db": "postgres"},
    }

    response = client.post("/skills/dba/partitioning/review_architecture", json=payload)

    assert response.status_code in {501, 400, 200}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_dba_postgres_review_architecture_endpoint_smoke():
    payload = {
        "description": "Arquitetura multi-tenant usando Postgres como banco principal.",
        "context": {"db": "postgres"},
    }

    response = client.post("/skills/dba/postgres/review_architecture", json=payload)

    assert response.status_code in {501, 400, 200}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_dba_replication_review_architecture_endpoint_smoke():
    payload = {
        "description": "Replica assíncrona entre duas zonas de disponibilidade.",
        "context": {"db": "postgres"},
    }

    response = client.post("/skills/dba/replication/review_architecture", json=payload)

    assert response.status_code in {501, 400, 200}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_dba_vacuum_review_architecture_endpoint_smoke():
    payload = {
        "description": "Base OLTP com problemas de bloat e autovacuum desconfigurado.",
        "context": {"db": "postgres"},
    }

    response = client.post("/skills/dba/vacuum/review_architecture", json=payload)

    assert response.status_code in {501, 400, 200}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)