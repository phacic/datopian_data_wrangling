from typing import List
import urllib.request
from pprint import pprint
from csv import writer as csv_writer
from bs4 import BeautifulSoup


def read_data_from_source() -> List[List]:
    # read html content
    url = "https://en.wikipedia.org/wiki/Road_safety_in_Europe"
    content = urllib.request.urlopen(url).read()

    # extract table with beautiful soup
    s = BeautifulSoup(content, 'html.parser')
    table = s.find('table', {"class": "wikitable sortable"})

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

    pprint(data)
    return data


def save_to_csv(data: List[List], filename: str) -> None:
    """ save data to csv"""
    with open(file=filename, mode="w") as f:
        write_head = csv_writer(f)
        write_head.writerows(data)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


if __name__ == '__main__':
    # print_hi('PyCharm')
    data = read_data_from_source()
    save_to_csv(data, 'raw.csv')
