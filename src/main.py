from operator import itemgetter
from loguru import logger

from utils import (read_html_table_data, save_to_csv)


@logger.catch
def wrangle_data():
    """
    extract data from url, select what's needed and store the output in a csv
    format
    """

    raw_data = read_html_table_data()

    # save raw data to csv, for record keeping
    logger.info('saving raw table data to raw.csv')
    save_to_csv(raw_data, "../raw.csv")

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
    save_to_csv(required_data, '../output.csv')

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
    save_to_csv(required_data, '../output_header.csv')


if __name__ == '__main__':
    wrangle_data()
