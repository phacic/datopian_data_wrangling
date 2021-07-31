from typing import List, Generator
import pytest
from faker import Faker

fake = Faker()


@pytest.fixture(scope='session')
def html_table() -> Generator[str, None, None]:
    with open('./test_sample.html', 'rb') as f:
        content = f.read()
    yield content
