from typing import List
import urllib.request
from operator import itemgetter
from functools import reduce
from csv import writer as csv_writer
from bs4 import BeautifulSoup
from loguru import logger


def read_data_from_source() -> List[List]:
    """
    extract data from html table
    :return: table content
    """

    # read html content
    url = "https://en.wikipedia.org/wiki/Road_safety_in_Europe"
    content = urllib.request.urlopen(url).read()

    logger.info(f"fetching content of {url}...")

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
    save table data to csv file
    """
    with open(file=filename, mode="w") as f:
        write_head = csv_writer(f)
        write_head.writerows(data)


@logger.catch
def wrangle_data():
    """
    extract data from url, select what's needed and store the output in a csv
    format
    """

    raw_data = read_data_from_source()

    # save raw data to csv, for record keeping
    logger.info('saving raw table data to raw.csv')
    save_to_csv(raw_data, "raw.csv")

    # remove title and summary (footer) rows
    # to be added later
    title_row = raw_data.pop(0)
    raw_data.pop()

    # required columns
    # Country 0, Year (new), Area 1, Population 2, GDP per capita 3, Population density 4,
    # vehicle ownership 5, total deaths 7, Road deaths per million inhabitants (new)
    # negative value (-1) are the new columns which are currently not available in the table
    required_column_indexes = [0, -1, 1, 2, 3, 4, 5, 7, 8]
    required_column_count = len(required_column_indexes)
    last_column_index = required_column_count - 1

    required_data = []
    for k in range(len(raw_data)):
        row = raw_data[k]

        # new row placeholder values
        new_row = [0] * required_column_count
        for i in range(required_column_count):
            if required_column_indexes[i] < 0:
                if i == 1:
                    # insert year, always 2018 (if the year is always the same it should probably be ignored)
                    new_row[i] = 2018
            else:
                new_row[i] = row[required_column_indexes[i]]

        required_data.append(new_row)

    # sort by deaths per million (last index)
    required_data = sorted(required_data, key=itemgetter(last_column_index))

    # save sorted required data
    logger.info('saving required data')
    save_to_csv(required_data, 'output.csv')

    # add titles (headers) and fooer
    new_titles = [''] * required_column_count

    for k in range(required_column_count):
        if required_column_indexes[k] < 0:
            if k == 1:
                new_titles[k] = 'Year'
            elif k == last_column_index:
                new_titles[k] = "Road deaths per Million Inhabitants"
        else:
            new_titles[k] = title_row[required_column_indexes[k]]

    required_data.insert(0, new_titles)

    logger.info('saving required data with header')
    save_to_csv(required_data, 'output_header.csv')


if __name__ == '__main__':
    wrangle_data()
