import os
import pytest
import yaml

dir_path = os.path.dirname(os.path.realpath(__file__))
talks_path = os.path.join(dir_path, "../talks")
slides_path = os.path.join(dir_path, "../slides")

ids = []
for file in os.listdir(slides_path):
    if file.endswith(".pdf"):
        ids.append(file[:-4])


@pytest.mark.parametrize("i", ids)
def test_all_included(i):
        assert os.path.isfile(os.path.join(talks_path, f"{i}.yml"))
