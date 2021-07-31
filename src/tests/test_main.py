from src.main import wrangle_data


def test_wrangle_data(mocker, html_table):
    """ """

    # mock fetch_html() to return desired html table
    mocker.patch(
        "src.utils.fetch_html", return_value=html_table
    )

    # mock save_to_csv so csv files are not created
    mocker.patch(
        "src.utils.save_to_csv", return_value=None
    )

    data = wrangle_data()
    assert len(data) > 0
