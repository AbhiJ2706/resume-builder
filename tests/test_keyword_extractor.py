import pytest

from resume_builder.keyword_extractor import __reconstruct_keywords


@pytest.fixture
def default_keywords():
    return [
        'Air', '##flow', 
        'Snow', '##f', '##lake', 
        'C', '##lick', '##H', '##ouse', 
        'Ka', '##f', '##ka', 
        'data processing', 
        'machine', 
        'work', '##flow orchestra', '##tors', 
        'Air', '##flow', 
        'Da', '##gs', '##ter', 
        'Pre', '##fect', 
        'A', '##WS', 
        'G', '##CP', ',', 
        'A', '##zure', 
        'S', '##QL', 
        'Snow', '##f', '##lake', 
        'Reds', '##hi', '##ft', 
        'Big', '##Q', '##uer', '##y', 
        'anal', '##ytics', 
        'machine learning', 
        'Python programming', 
        'data storage', 
        'A', '##WS', 
        'Terra', '##form', 
        'Data', '##dog', 
        'streaming'
    ]

@pytest.fixture
def hyphens():
    return [
        'Python', 
        'Fast', '##AP', '##I', 
        'Re', '##act', 
        'Type', '##Script', 
        'front', '##end', 
        'client', '-', 'side', 'Snow', '##f', '##lake', 'data', 
        'end', '-', 'to', '-', 'end', 
        'back', '##end'
    ]

@pytest.fixture
def slashes():
    return [
        'G', '##rap', '##h', '##QL', 
        'Dock', '##er', '/', 'Ku', '##ber', '##net', '##es', 
        'cloud services', 
        'A', '##WS,',
        'ci', '/', 'cd'
    ]


def postprocess(results):
    return [x.lower() for x in results]


def test_slashes(slashes):
    result = postprocess(__reconstruct_keywords(slashes))
    assert result == [
        "graphql",
        "docker",
        "docker/kubernetes",
        "kubernetes",
        "cloud services",
        "aws,",
        "ci",
        "ci/cd",
        "cd"
    ]


def test_hyphens(hyphens):
    result = postprocess(__reconstruct_keywords(hyphens))
    assert result == [
        'python', 
        'fastapi', 
        'react', 
        'typescript', 
        'frontend', 
        'client-side', 
        'snowflake', 
        'data', 
        'end-to-end', 
        'backend'
    ]

def test_default(default_keywords):
    result = postprocess(__reconstruct_keywords(default_keywords))
    assert result == [
        'airflow', 
        'snowflake', 
        'clickhouse', 
        'kafka', 
        'data processing', 
        'machine', 
        'workflow orchestrators', 
        'airflow', 
        'dagster', 
        'prefect', 
        'aws', 
        'gcp', ',', 
        'azure', 
        'sql', 
        'snowflake', 
        'redshift', 
        'bigquery', 
        'analytics', 
        'machine learning', 
        'python programming', 
        'data storage', 
        'aws', 
        'terraform', 
        'datadog', 
        'streaming'
    ]