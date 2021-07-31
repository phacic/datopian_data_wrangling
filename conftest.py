from typing import List, Generator
import pytest
from faker import Faker

fake = Faker()


@pytest.fixture(scope='session')
def html_table() -> Generator[str, None, None]:
    """ fixture for html with table """
    with open('./test_sample.html', 'rb') as f:
        content = f.read()
    yield content


@pytest.fixture(scope="function")
def table_data() -> Generator[List[List], None, None]:
    """ fixture for data from html table """
    data = []
    # create 3 rows of data
    for _ in range(3):
        data.append(fake.pylist(5))

    yield data
