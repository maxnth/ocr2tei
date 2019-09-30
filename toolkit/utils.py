import os
from ast import literal_eval
import regex as re
import json

from lxml import etree

from django.conf import settings

base_path = os.path.join(settings.MEDIA_ROOT, "projects/")


def generate_ns_dict(file) -> dict:
    """
    Automatically extracts the namespace out of the PAGE XML and generates a namespace mapping for lxml
    :param file:
    :return: dict
    """
    namespaces = {
        "2016": {"px": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2016-07-15"},
        "2017": {"px": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15"},
        "2018": {"px": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2018-07-15"},
        "2019": {"px": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15"}
    }

    with open(file, "r") as text:
        for line in text.readlines():
            ver = re.search("http://schema.primaresearch.org/PAGE/gts/pagecontent/([0-9]{4})", line)
            if ver:
                version = ver.groups()[0]
            else:
                version = "2019"

    return namespaces[version]


def parse_xml(file):
    """
    Parses file using the lxml.etree parser
    :param file:
    :return: lxml tree
    """
    return etree.parse(file)


def get_pages(tree, nsmap):
    """
    Gets all Page Elements from the PAGE XML in case more than one page was encoded in the XML file
    :param tree:
    :param nsmap:
    :return:
    """
    return tree.xpath("//px:Page", namespaces=nsmap)


def get_page_options(file) -> bool:
    nsmap = generate_ns_dict(file)
    tree = parse_xml(file)
    pages = get_pages(tree, nsmap)

    try:
        comment_dict = literal_eval(pages[0].attrib["comments"])
        ignore = comment_dict["ignore"]
    except KeyError:
        ignore = "False"

    return ignore


def get_reading_order(page, nsmap) -> dict:
    """
    Extracts reading order element from the XML tree and turns it into a dictionary with the format
    {Reading Order Position: Region ID}
    :param page:
    :param nsmap:
    :return: dict
    """
    ro_dict = dict()
    reading_order = page.xpath("//px:ReadingOrder/px:OrderedGroup//px:RegionRefIndexed", namespaces=nsmap)
    for region in reading_order:
        ro_dict[region.xpath("@index")[0]] = region.xpath("@regionRef")[0]
    return ro_dict


def get_text_regions(tree, nsmap) -> list:
    """
    Extracts a list of Text Regions from a given page element
    :param tree:
    :param nsmap:
    :return: list
    """
    return [analyze_region(region, nsmap) for region in tree.xpath("//px:TextRegion", namespaces=nsmap)]


def analyze_region(text_region, nsmap) -> dict:
    """
    Extracts all useful information from a given text region elements and turns it into a dictionary
    :param text_region:
    :param nsmap:
    :return: dict
    """
    region_id = text_region.xpath("@id")[0]
    region_type = text_region.xpath("@type")[0]
    comments = ""
    if text_region.xpath("@comments"):
        comments = text_region.xpath("@comments")[0].replace("'", '"')
    _region_coords = [coord.split(" ") for coord in text_region.xpath("./px:Coords/@points", namespaces=nsmap)][0]
    region_coords = list()
    for coord in _region_coords:
        region_coords.append({"x": int(coord.split(",")[0]), "y": int(coord.split(",")[1])})

    lines = [analyze_line(line, nsmap) for line in text_region.xpath(".//px:TextLine", namespaces=nsmap)]

    return {"rID": region_id, "rType": region_type, "rCoords": region_coords, "lines": lines, "comments": comments}


def analyze_line(line, nsmap) -> dict:
    """
    Extracts all useful information from a given text line elements and turns it into a dictionary
    :param text_region:
    :param nsmap:
    :return: dict
    """
    line_id = line.xpath("@id")
    _line_coords = [coord.split(" ") for coord in line.xpath("./px:Coords/@points", namespaces=nsmap)][0]
    line_coords = list()
    for coord in _line_coords:
        line_coords.append({"x": int(coord.split(",")[0]), "y": int(coord.split(",")[1])})
    line_text = "".join(line.xpath("./px:TextEquiv/px:Unicode/text()", namespaces=nsmap))
    return {"lID": line_id, "lCoords": line_coords, "lText": line_text}


def get_text_content(node) -> str:
    """
    Gets all text content from a given node
    :param node:
    :return:
    """
    return " ".join(node.itertext())


def build_dict(file) -> dict:
    """
    Builds a dictionary from a given file which ultimately gets supplied as JSON element to the REST API
    :param file:
    :return:
    """
    page_dict = dict()

    nsmap = generate_ns_dict(file)
    tree = parse_xml(file)
    pages = get_pages(tree, nsmap)
    for page in pages:
        ro = get_reading_order(page, nsmap)
        text_regions = get_text_regions(page, nsmap)
        for region in text_regions:
            _region_dict = region
            _region_ro = next((key for key, val in ro.items() if val == _region_dict["rID"]), None)
            if _region_ro:
                _region_ro = int(_region_ro)
            page_dict[_region_ro] = _region_dict
    return page_dict


def build_page_json(file):
    """
    Helper to build a JSON file from a dictionary
    :param file:
    :return:
    """
    d = build_dict(file)
    return json.dumps(d)

