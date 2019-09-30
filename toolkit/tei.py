import os
from ast import literal_eval

from lxml import etree

from toolkit import tei_resources
from toolkit import utils
from projects.models import Project

from django.conf import settings
from django.forms.models import model_to_dict
from rules.models import SimpleRule, IgnoreRule

base_path = os.path.join(settings.MEDIA_ROOT, "projects/")


def get_tei_elements():
    return tei_resources.tei_dict


def build_tei(project, files, simple_rules, ignore_rules) -> str:
    """
    Builds the global output TEI file from the given parameters
    :param project:
    :param files:
    :param simple_rules:
    :param ignore_rules:
    :return: str
    """
    nsmap = {"tei": "http://www.tei-c.org/ns/1.0"}

    s_rules, i_rules = get_rules(simple_rules, ignore_rules)

    header = build_tei_header(project)
    body = ""

    for file in files:
        body += generate_page_tei(project, file, ignore_list=i_rules, simple_rules=s_rules)

    built_tei = build_from_template(header, body)

    try:
        tree = etree.parse(built_tei, etree.XMLParser(remove_blank_text=True))
        pretty_built_tei = etree.tostring(tree, pretty_print=True)
        return pretty_built_tei
    except:
        return built_tei


def build_tei_header(pid) -> str:
    """
    Builds TEI header from the metadata instance of the loaded project
    :param pid:
    :return: str
    """
    try:
        prj = Project.objects.get(title=pid)
    except Project.DoesNotExist as e:
        return ""
    try:
        metadata = prj.metadata
    except:
        return ""

    meta_dict = model_to_dict(metadata)

    file_desc_tempalte = """
    <fileDesc>
      <titleStmt>
       <title>{title_statement}</title>
      </titleStmt>
      <publicationStmt>
       <p>{publication_statement}</p>
      </publicationStmt>
      <sourceDesc>
       <bibl><title>{source_description}</title></bibl>
      </sourceDesc>
      <editionStmt>
        <edition>{edition_statement}</edition>
      </editionStmt>
      <notesStmt>
        <note>{notes_statement}</note>
      </notesStmt>
      <seriesStmt>
        <title>{series_statement}</title>
      </seriesStmt>
      <extent>
        {extent}
      </extent>
     </fileDesc>
    """.format(**meta_dict)

    return file_desc_tempalte


def generate_page_tei(project, page, ignore_list=None, simple_rules=None) -> str:
    """
    Generated output string for a single page while taking rules and region/page options in consideration
    :param project:
    :param page:
    :param ignore_list:
    :param simple_rules:
    :return: str
    """

    path = ".".join([os.path.join(base_path, project, "input", page), "xml"])

    page_dict = dict(sorted(utils.build_dict(path).items()))

    print(page_dict)

    ignore = utils.get_page_options(path)

    out = ""

    if ignore == "False":
        for key, val in page_dict.items():
            _out = list()
            elem = "p"

            if ignore_list:
                if val["rType"] in ignore_list:
                    print(True)
                    continue

            if val["comments"]:
                comments = literal_eval(val["comments"])
                if comments["ignore"] == "True":
                    continue
                elif comments["forced"]:
                    elem = comments["forced"]
            if simple_rules:
                for rule in simple_rules:
                    if val["rType"] == rule["base"]:
                        print("Yes")
                        elem = rule["target"]
                        continue

            for line in val["lines"]:
                _out.append(line["lText"])

            out += "<{0}>{1}</{0}>".format(elem, "\n".join(_out))

        out += "<pb/>"

    return out


def get_rules(simple_rules, ignore_rules):
    """
    Retrieves the information from the chosen rule instances for the conversion
    :param simple_rules:
    :param ignore_rules:
    :return:
    """
    s_rules = list()
    i_rules = list()
    if simple_rules:
        for rule in simple_rules:
            try:
                r = SimpleRule.objects.get(name=rule)
                s_rules.append(model_to_dict(r))
            except SimpleRule.DoesNotExist:
                continue
    if ignore_rules:
        for rule in ignore_rules:
            try:
                r = IgnoreRule.objects.get(name=rule)
                i_rules.append(model_to_dict(r))
            except SimpleRule.DoesNotExist:
                continue

    _i_rules = list()
    for rule in i_rules:
        _i_rules.append(rule["ignore"])

    return s_rules, _i_rules


def build_from_template(tei_header, tei_body) -> str:
    """
    Puts all retrieved text information in a TEI template
    :param tei_header:
    :param tei_body:
    :return: str
    """
    tei_template = """
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" 
    schematypens="http://relaxng.org/ns/structure/1.0"?>
    <?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" 
    schematypens="http://purl.oclc.org/dsdl/schematron"?>
    <TEI xmlns="http://www.tei-c.org/ns/1.0">
       <teiHeader>
          {tei_header}
       </teiHeader>
       <text>
          <body>
             {tei_body}
          </body>
       </text>
    </TEI>
    """.format(tei_header=tei_header, tei_body=tei_body)

    return tei_template
