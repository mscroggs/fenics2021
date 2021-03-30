import os
import pytest
import yaml


def test_all_included():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    talks_path = os.path.join(dir_path, "../talks")

    with open(os.path.join(talks_path, "_timetable.yml")) as f:
        timetable = yaml.load(f, Loader=yaml.FullLoader)

    ids1 = set()
    for day, i in timetable.items():
        if day == "other":
            for k in i:
                ids1.add(k)
        else:
            for j in i.values():
                if "talks" in j:
                    for k in j["talks"]:
                        ids1.add(k)

    ids2 = set()
    for file in os.listdir(talks_path):
        if file.endswith(".yml") and file != "_timetable.yml":
            ids2.add(file[:-4])

    assert ids1 == ids2


def test_email_list():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    talks_path = os.path.join(dir_path, "../talks")
    emails_path = os.path.join(dir_path, "../emails")

    if not os.path.isdir(emails_path) or not os.path.isfile(os.path.join(emails_path,
                                                                         "email_list")):
        pytest.skip()

    ids1 = set()
    with open(os.path.join(emails_path, "email_list")) as f:
        for line in f:
            if not line.startswith("  "):
                ids1.add(line.strip())

    ids2 = set()
    for file in os.listdir(talks_path):
        if file.endswith(".yml") and file != "_timetable.yml":
            ids2.add(file[:-4])

    assert ids1 == ids2
