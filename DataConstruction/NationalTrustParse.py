"""
Purpose: Extract official links via BeautifulSoup from a set of saved html files from Wikipedia.
Note: If you are going to use this file, you will also need to set the env variable nat_trust_links to the directory
      of the downloaded data
"""
from bs4 import BeautifulSoup
from miscSupports import directory_iterator, load_yaml, write_json
from pathlib import Path
from typing import Tuple


def extract_link(root: str, file: str) -> Tuple[str, str]:
    """
    Extract the links and place name from the html file.

    We search for an official link to a national trust website, but failing that use the default link to this site on
    Wikipedia. Name is just sliced from the file name.
    """
    # Extract the file name by slicing the file name, then load the context in BeautifulSoup
    place_name = file.split("-")[0]
    html_file = BeautifulSoup(open(Path(root, file), "rb"), features="html.parser")
    print(place_name)

    # Extract all the links, then filter on web address of the href
    official_links = [link.get("href") for link in html_file.find_all("a", attrs={"class": "external text"})
                      if link.string and 'national trust' in link.string.lower()]
    official_links = [link for link in official_links if "www.nationaltrust.org.uk" in link]

    # If we fail to find a link, use the Wikipedia one
    if len(official_links) == 0:
        return place_name, html_file.find("link", attrs={"rel": "canonical"}).get("href")

    # If we find one or more links, use the first one in the list
    else:
        return place_name, official_links[0]


def construct_link_database():
    """Construct a json file of links to national trust properties to match against locations"""
    root = load_yaml(Path(Path(__file__).parent.parent, "env.yaml"))['nat_trust_links']
    links_list = [extract_link(root, file) for file in directory_iterator(root)]

    links_database = {name: link for name, link in links_list}

    write_json(links_database, str(Path(Path(__file__).parent.parent, 'Data').absolute()), 'NationalTrustLinks')


if __name__ == '__main__':
    construct_link_database()
