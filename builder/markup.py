import shlex
import re
from datetime import datetime
from citations import markup_citation

page_references = []


def markup(content):
    global page_references
    while "{{if " in content:
        pre, rest = content.split("{{if ", 1)
        condition, rest = rest.split("}}", 1)
        optional, post = rest.split("{{fi}}", 1)
        condition, options = condition.split(" ", 1)
        content = pre
        if condition in ["before", "after"]:
            options = [int(i) for i in options.split(",")]
            if condition == "before" and datetime.now() < datetime(*options):
                content += optional
            if condition == "after" and datetime.now() > datetime(*options):
                content += optional
        else:
            raise ValueError(f"Unknown condition: {condition}")
        content += post

    while "<person>" in content:
        a, b = content.split("<person>", 1)
        b, c = b.split("</person>", 1)
        content = a + markup_person(b) + c

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


def markup_person(details):
    out = "<div class='person'>"
    info = {}
    for line in details.strip().split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            info[key.strip()] = value.strip()

    if "img" in info:
        out += f"<div class='imgwrap'><img src='{info['img']}'></div>\n"
    out += "<div class='innertext'>\n"
    out += f"<h3>{info['name']}</h3>\n{info['about']}"
    out += "<ul class='sociallist'>"
    if "email" in info:
        out += f"<li><a href='mailto:{info['email']}'><i class='far fa-envelope'></i>&nbsp;"
        out += info["email"]
        out += "</a></li>"
    if "website" in info:
        out += f"<li><a href='{info['website']}'><i class='fab fa-internet-explorer'></i>&nbsp;"
        out += info["website"].split("://")[1]
        out += "</a></li>"
    if "github" in info:
        out += f"<li><a href='https://github.com/{info['github']}'>"
        out += "<i class='fab fa-github'></i>&nbsp;"
        out += info["github"]
        out += "</a></li>"
    if "twitter" in info:
        out += f"<li><a href='https://twitter.com/{info['twitter']}'>"
        out += "<i class='fab fa-twitter'></i>&nbsp;"
        out += "@" + info["twitter"]
        out += "</a></li>"

    out += "</ul></div></div>"
    return out
