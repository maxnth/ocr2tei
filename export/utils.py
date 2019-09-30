import os

from django.conf import settings

base_path = os.path.join(settings.MEDIA_ROOT, "projects/")


def save_output(project, page=None, text=""):
    if page:
        print(page)
        with open(os.path.join(base_path, project, "output", page) + ".xml", "w") as out:
            out.write(text)
    else:
        with open(os.path.join(base_path, project, "output", project) + ".output", "w") as out:
            out.write(text)
