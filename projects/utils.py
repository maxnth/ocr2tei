import os
from pathlib import Path

from lxml import etree

from projects.models import Project
from toolkit.utils import build_page_json
from django.conf import settings

base_path = os.path.join(settings.MEDIA_ROOT, "projects/")


def retrieve_pages(pid, page=None) -> list:
    file_list = list()

    if page:
        path = sorted(Path(base_path, pid).glob("./input/{0}*".format(page)))
    else:
        path = sorted(Path(base_path, pid).glob("./input/*"))

    for file in [file for file in path if file.is_file()]:
        if not any(f["title"] == file.stem for f in file_list):
            file_list.append({"title": file.stem, "xml": None, "xml_text": None, "xml_data": None, "image": None,
                              "output": None, "output_text": None})
        if file.suffix in [".xml"]:
            next(d for d in file_list if d["title"] == file.stem)["xml"] = relative_path(str(file.resolve()))
            next(d for d in file_list if d["title"] == file.stem)["xml_text"] = etree.tostring(etree.parse(
                str(file.resolve())), pretty_print=True)
            next(d for d in file_list if d["title"] == file.stem)["xml_data"] = build_page_json(str(file.resolve()))
        elif file.suffix in [".jpg", ".jpeg", ".png", ".gif"]:
            next(d for d in file_list if d["title"] == file.stem)["image"] = relative_path(str(file.resolve()))

    for file in [file for file in sorted(Path(base_path, pid).glob("./output/*xml")) if file.is_file()]:
        if not any(f["title"] == file.stem for f in file_list):
            file_list.append(
                {"title": file.stem, "xml": None, "xml_text": None, "xml_data": None, "image": None, "output": None,
                 "output_text": None})
        next(d for d in file_list if d["title"] == file.stem)["output"] = relative_path(str(file.resolve()))
        try:
            next(d for d in file_list if d["title"] == file.stem)["output_text"] = etree.tostring(etree.parse(
                str(file.resolve())), pretty_print=True)
        except etree.XMLSyntaxError as e:
            with open(str(file.resolve()), 'r') as data:
                next(d for d in file_list if d["title"] == file.stem)["output_text"] = data.read().replace('\n', '')

    return file_list


def get_pages(pid) -> list:
    project = Project.objects.get(title=pid)

    pages = retrieve_pages(pid)

    project.pages = len(pages)

    corrected_pages = [x["output"] for x in pages if x["output"]]
    if pages:
        project.percent_corrected = round(len(corrected_pages) / len(pages), 2) * 100
    else:
        project.percent_corrected = 0

    project.save()

    return pages


def get_page(pid, page) -> dict:
    _page = retrieve_pages(pid, page)[0]

    _page["previous"], _page["next"] = get_previous_next(pid, page)

    return _page


def get_previous_next(pid, page):
    page_list = sorted({s.stem for s in sorted(Path(base_path, pid).glob("./input/*"))})
    try:
        if page_list.index(page) == 0:
            previous = None
        else:
            previous = page_list[page_list.index(page) - 1]
    except IndexError:
        previous = None

    try:
        _next = page_list[page_list.index(page) + 1]
    except IndexError:
        _next = None

    return previous, _next


def read_directory(path=base_path):
    for dir in Path(path).iterdir():
        if dir.is_dir():
            if not Project.objects.filter(title=dir.stem):
                project = Project(title=dir.stem)
                project.save()
                get_pages(dir.stem)


def relative_path(path):
    return "/" + "/".join(path.split("/")[-5:])


def update_project_list():
    read_directory()
