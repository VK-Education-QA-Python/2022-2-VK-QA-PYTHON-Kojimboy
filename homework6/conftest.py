import os

import pytest
from sqlalchemy.orm import close_all_sessions

from mysql.client import MysqlClient


def pytest_configure(config):
    mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_SQL')
    if not hasattr(config, 'workerinput'):
        mysql_client.create_db()
    mysql_client.connect(db_created=True)
    if not hasattr(config, 'workerinput'):
        mysql_client.create_tables()

    config.mysql_client = mysql_client


def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client

    close_all_sessions()  # закрываем все сессии
    if not hasattr(request.config, 'workerinput'):
        client.drop_db()  # дропаем всю базу после тестов
        # (не дропает в параллельном режиме)
