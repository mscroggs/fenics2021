import shlex
import re
from datetime import datetime
from citations import markup_citation

page_references = []


def markup(content):
    global page_references
    out = ""
    popen = False
    code = False
    is_python = False
    for line in content.split("\n"):
        if line.startswith("#"):
            if popen:
                out += "</p>\n"
                popen = False
            i = 0
            while line.startswith("#"):
                line = line[1:]
                i += 1
            out += f"<h{i}>{line.strip()}</h{i}>\n"
        elif line == "":
            if popen:
                out += "</p>\n"
                popen = False
        elif line == "```":
            code = not code
            is_python = False
        elif line == "```python":
            code = not code
            is_python = True
        else:
            if not popen and not line.startswith("<") and not line.startswith("\\["):
                if code:
                    out += "<p class='pcode'>"
                else:
                    out += "<p>"
                popen = True
            if code:
                if is_python:
                    out += python_highlight(line.replace(" ", "&nbsp;"))
                else:
                    out += line.replace(" ", "&nbsp;")
                out += "<br />"
            else:
                out += line
                out += " "
    page_references = []

    out = re.sub(r" *<ref ([^>]+)>", add_citation, out)
    out = insert_links(out)

    out = re.sub(r"`([^`]+)`", r"<span style='font-family:monospace'>\1</span>", out)

    if len(page_references) > 0:
        out += "<h2>References</h2>"
        out += "<ul class='citations'>"
        out += "".join([f"<li><a class='refid' id='ref{i+1}'>[{i+1}]</a> {j}</li>"
                        for i, j in enumerate(page_references)])
        out += "</ul>"

    return insert_dates(out)


def insert_links(txt):
    txt = re.sub(r"\(([^\)]+)\.md\)", r"(/\1.html)", txt)
    txt = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", r"<a href='\2'>\1</a>", txt)
    return txt


def add_citation(matches):
    global page_references
    ref = {}
    for i in shlex.split(matches[1]):
        a, b = i.split("=")
        ref[a] = b
    page_references.append(markup_citation(ref))
    return f"<sup><a href='#ref{len(page_references)}'>[{len(page_references)}]</a></sup>"


def insert_dates(txt):
    now = datetime.now()
    txt = txt.replace("{{date:Y}}", now.strftime("%Y"))
    txt = txt.replace("{{date:D-M-Y}}", now.strftime("%d-%B-%Y"))

    return txt


def python_highlight(txt):
    txt = txt.replace(" ", "&nbsp;")
    out = []
    for line in txt.split("\n"):
        comment = ""
        if "#" in line:
            lsp = line.split("#", 1)
            line = lsp[0]
            comment = f"<span style='color:#FF8800'>#{lsp[1]}</span>"

        lsp = line.split("\"")
        line = lsp[0]

        for i, j in enumerate(lsp[1:]):
            if i % 2 == 0:
                line += f"<span style='color:#DD2299'>\"{j}"
            else:
                line += f"\"</span>{j}"

        out.append(line + comment)
    return "<br />".join(out)
