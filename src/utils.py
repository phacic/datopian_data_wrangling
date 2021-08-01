from typing import List
import urllib.request
from csv import writer as csv_writer
from bs4 import BeautifulSoup

from loguru import logger


def fetch_html():
    """
    pull html content
    :return html content
    """

    url = "https://en.wikipedia.org/wiki/Road_safety_in_Europe"
    logger.info(f"fetching content of {url}...")

    response = urllib.request.urlopen(url)
    content = response.read()
    return content


def read_html_table_data() -> List[List]:
    """
    extract data from html table
    :return: List of Lists of the table content
    """

    # read html content
    content = fetch_html()

    # extract table with beautiful soup
    s = BeautifulSoup(content, 'html.parser')
    table = s.find('table', {"class": "wikitable sortable"})

    logger.info(f'Parsing html content for table data')

    data = []
    rows = table.find_all("tr")
    for r in rows:
        # extra cells data
        row_data = []
        for cell in r.find_all(['td', 'th']):
            # get content of cell
            text = cell.get_text().strip()
            row_data.append(text)

        data.append(row_data)

    logger.info(f'{len(data)} rows of data extracted')
    return data


def save_to_csv(data: List[List], filename: str) -> None:
    """
    save table data to csv file.
    Not passing a filename will not create any file
    """
    if filename:
        with open(file=filename, mode="w") as f:
            write_head = csv_writer(f)
            write_head.writerows(data)
