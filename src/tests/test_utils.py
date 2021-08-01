import pytest
import pytest_mock
import os
from unittest.mock import Mock, patch

from src.utils import (read_html_table_data, save_to_csv)


def test_read_html_table(html_table, mocker):
    mocker.patch(
        "src.utils.fetch_html", return_value=html_table
    )

    d = read_html_table_data()
    assert len(d) > 0


def test_to_save_csv(table_data):
    filename = 'test1.csv'
    save_to_csv(table_data, filename)
    assert os.path.exists(filename)

    # clean up
    os.remove(filename)




