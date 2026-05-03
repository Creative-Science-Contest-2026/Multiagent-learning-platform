from deeptutor.services.db.postgres import AuthDatabaseSettings


def test_auth_database_settings_require_postgres_url() -> None:
    settings = AuthDatabaseSettings(database_url="postgresql+psycopg://user:pass@localhost/app")
    assert settings.database_url.startswith("postgresql+psycopg://")
