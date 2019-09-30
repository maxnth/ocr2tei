from ast import literal_eval
import os
from pathlib import Path

from lxml import etree

from django.conf import settings
from toolkit import utils


base_path = os.path.join(settings.MEDIA_ROOT, "projects/")

pagexml_text_region_types = [
    "paragraph", "heading", "caption", "header", "footer", "page-number",
     "drop-capital", "credit", "floating", "signature-mark", "catch-word",
     "marginalia", "footnote", "footnote-continued", "endnote", "TOC-entry",
     "list-label", "other"
]


def set_page_options(project, page, ignore="False"):
    """
    Writes user supplied page options into the PAGE XML page element and saves the changes in the original file
    :param project:
    :param page:
    :param region:
    :param element:
    :param ignore:
    :return:
    """

    path = str(Path(base_path, project, "input", page).with_suffix(".xml").resolve())
    nsmap = utils.generate_ns_dict(path)
    tree = utils.parse_xml(path)

    elem = tree.xpath("//px:Page", namespaces=nsmap)[0]

    if len(elem):
        try:
            comment_dict = literal_eval(elem.attrib["comments"])
            comment_dict["ignore"] = str(ignore)
            elem.set("comments", str(comment_dict))
        except KeyError:
            elem.set("comments", str({"ignore": str(ignore)}))

    with open(path, "w") as file:
        file.write(etree.tostring(tree, encoding='unicode'))


def set_region_options(project, page, region, element="", ignore="False"):
    """
    Writes user supplied region options into the PAGE XML region element and saves the changes in the original file
    :param project:
    :param page:
    :param region:
    :param element:
    :param ignore:
    :return:
    """
    path = str(Path(base_path, project, "input", page).with_suffix(".xml").resolve())
    nsmap = utils.generate_ns_dict(path)
    tree = utils.parse_xml(path)

    elem = tree.xpath("//px:*[@id='" + region + "']", namespaces=nsmap)[0]

    if element:
        try:
            comment_dict = literal_eval(elem.attrib["comments"])
            comment_dict["forced"] = element
            comment_dict["ignore"] = ignore
            elem.set("comments", str(comment_dict))
        except KeyError:
            elem.set("comments", str({"forced": element, "ignore": "False"}))
    if ignore == "True":
        try:
            comment_dict = literal_eval(elem.attrib["comments"])
            comment_dict["ignore"] = ignore
            elem.set("comments", str(comment_dict))
        except KeyError:
            elem.set("comments", str({"forced": "", "ignore": ignore}))

    with open(path, "w") as file:
        file.write(etree.tostring(tree, encoding='unicode'))