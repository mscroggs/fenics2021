import os
import yaml


def test_all_included():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    talks_path = os.path.join(dir_path, "../talks")

    with open(os.path.join(talks_path, "timetable.yml")) as f:
        timetable = yaml.load(f, Loader=yaml.FullLoader)

    ids1 = set()
    for i in timetable.values():
        for j in i.values():
            for k in j:
                ids1.add(k)

    ids2 = set()
    for file in os.listdir(talks_path):
        if file.endswith(".yml") and file != "timetable.yml":
            ids2.add(file[:-4])

    assert ids1 == ids2
