import os
import re
import shlex
import yaml
from markup import iconlist

dir_path = os.path.dirname(os.path.realpath(__file__))

talks_path = os.path.join(dir_path, "../talks")
slides_path = os.path.join(dir_path, "../slides")
tex_path = os.path.join(dir_path, "../_tex")
pdf_path = os.path.join(dir_path, "../_pdf")

if os.path.isdir(tex_path):
    os.system(f"rm -rf {tex_path}")
if os.path.isdir(pdf_path):
    os.system(f"rm -rf {pdf_path}")

os.mkdir(tex_path)
os.mkdir(pdf_path)


def insert_icons(txt):
    for t, icon, url in iconlist:
        txt = re.sub(
            r"(^|[>\s.!?\(\/])" + t + r"([\s.!?\)\/,']|(?:-based))",
            r"\1\\href{" + url + "}{" + t + r"}\2",
            txt, 1)
    return txt


def insert_links(txt):
    txt = re.sub(r"([^\('])(https?:\/\/)([^\s]+)", r"\1\\url{\2}", txt)
    txt = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)\{([^\}]+)\}", r"\\href{\2}{\1}", txt)
    return txt


def to_tex(txt):
    txt = txt.replace("<ul>", "\\begin{itemize}")
    txt = txt.replace("</ul>", "\\end{itemize}")
    txt = txt.replace("<ol>", "\\begin{enumerate}")
    txt = txt.replace("</ol>", "\\end{enumerate}")
    txt = txt.replace("<li>", "\\item ")
    txt = txt.replace("</li>", "")
    txt = txt.replace("<i>", "\\emph{")
    txt = txt.replace("</i>", "}")
    txt = txt.replace("<b>", "\\textbf{")
    txt = txt.replace("</b>", "}")

    txt = re.sub(r"&(.)uml;", r'\\"{\1}', txt)
    txt = re.sub(r"&(.)tilde;", r"\\~{\1}", txt)
    txt = re.sub(r"&(.)ring;", r"\\r{\1}", txt)
    txt = re.sub(r"&(.)acute;", r"\\'{\1}", txt)
    txt = re.sub(r"&(.)circ;", r"\\^{\1}", txt)
    txt = txt.replace("&oslash;", "{\\o}")
    txt = txt.replace("&Oslash;", "{\\O}")
    txt = txt.replace("&ndash;", "--")
    txt = txt.replace("&mdash;", "---")
    txt = txt.replace("&szlig;", "{\\ss}")
    txt = txt.replace("&", "\\&")
    txt = re.sub(r"`([^`]+)`", r"\\texttt{\1}", txt)
    txt = txt.replace("_", "\\_")
    txt = txt.replace(' "', ' ``')
    txt = txt.replace(" '", " `")
    return txt


def tex_author(info, speaker=False):
    out = ""
    if speaker:
        out += "\\textbf{"
    out += to_tex(info["name"])
    if speaker:
        out += "}"
    urls = []
    if "website" in info:
        urls.append(f"\\url{{{info['website']}}}")
    if "github" in info:
        urls.append(f"\\href{{https://github.com/{info['github']}}}{{\\github{{{info['github']}}}}}")
    if "twitter" in info:
        urls.append(f"\\href{{https://twitter.com/{info['twitter']}}}{{\\twitter{{{info['twitter']}}}}}")

    if len(urls) > 0:
        out += " (" + ", ".join(urls)+ ")"
    if "affiliation" in info:
        out += ", " + to_tex(info["affiliation"])
        if "country" in info:
            out += ", " + to_tex(info["country"])
    return out


citations = {}
has_citations = False
has_citations_dict = {}


def write_citations():
    global citations
    bib = []
    for i, j in citations.items():
        ref = {}
        for k in shlex.split(i):
            a, b = k.split("=", 1)
            ref[a] = b

        if "journal" in ref:
            item = "@article{"
        else:
            item = "@unpublished{"
        item += j + ",\n";
        item += "author = {" + to_tex(" and ".join(ref["author"].replace(", and ", ", ").split(", "))) + "},\n"
        item += "title = {" + to_tex(ref["title"]) + "},\n"
        if "year" in ref:
            item += "year = {" + ref["year"] + "},\n"
        if "journal" not in ref and "arxiv" in ref:
            item += "note = {\\url{https://arxiv.org/abs/" + ref["arxiv"] + "}},\n"
        if "journal" not in ref and "url" in ref:
            item += "note = {\\url{" + ref["url"] + "}},\n"
        if "journal" in ref:
            item += "journal = {" + to_tex(ref["journal"]) + "},\n"
        if "volume" in ref:
            item += "volume = {" + ref["volume"] + "},\n"
        if "number" in ref:
            item += "number = {" + ref["number"] + "},\n"
        if "doi" in ref:
            item += "doi = {" + ref["doi"] + "},\n"
        if "pagestart" in ref:
            item += "pages = {{" + ref["pagestart"]
            if "pageend" in ref:
                item += "--" + ref["pageend"]
            item += "}},\n"
        item += "}"
        bib.append(item)

    with open(os.path.join(tex_path, "references.bib"), "w") as f:
        f.write("\n\n".join(bib))

def add_citation(matches):
    global citations
    global has_citations
    has_citations = True
    if matches[1] not in citations:
        citations[matches[1]] = f"ref{len(citations)}"
    return f"\\cite{{{citations[matches[1]]}}}"


def add_ghost_citation(matches):
    global citations
    global has_citations
    has_citations = True
    if matches[1] not in citations:
        citations[matches[1]] = f"ref{len(citations)}"
    return f"\\nocite{{{citations[matches[1]]}}}"


def tex_abstract(a):
    a = re.sub(r"<ref ([^>]+)>", add_citation, a)
    a = re.sub(r"<ghostref ([^>]+)>", add_ghost_citation, a)
    return insert_icons(insert_links(to_tex(a)))


def make_tex(tid, day, session):
    global has_citations
    global has_citations_dict
    has_citations = False

    with open(os.path.join(talks_path, f"{tid}.yml")) as f:
        tdata = yaml.load(f, Loader=yaml.FullLoader)

    authors = [tex_author(tdata["speaker"], True)]
    authorlist = tdata["speaker"]["name"]
    if "coauthor" in tdata:
        for i in tdata["coauthor"]:
            authorlist += ", " + i["name"]
        authors += [tex_author(i) for i in tdata["coauthor"]]
    authors = "\n\n\\smallskip\n\n".join(["\\hangindent=1cm " + i for i in authors])

    tex = f"\\talktitle{{{to_tex(tdata['title'])}}}\n"
    tex += f"\\addcontentsline{{toc}}{{section}}{{{to_tex(tdata['title'])} ({to_tex(authorlist)})}}\n"
    tex += f"\\talkauthor{{{authors}}}\n"
    tex += f"\\talkdate{{{dates[day]} 2021}}\n"

    tex += "\n\\medskip\n"
    tex += "\\begin{refsection}\n"

    if isinstance(tdata["abstract"], str):
        tex += tex_abstract(tdata["abstract"])
    else:
        tex += tex_abstract("\n\n".join(tdata["abstract"]))

    has_citations_dict[tid] = has_citations
    if has_citations:
        tex += "\n\n\\vfill\n\n\\printbibliography[heading=subbibliography]\n"

    tex += "\\end{refsection}\n"

    if os.path.isfile(os.path.join(slides_path, f"{tid}.pdf")):
        tex += "\\clearpage\n"
        tex += f"\\includepdf[pages=-,fitpaper,width=210mm]{{../slides/{tid}.pdf}}\n"
    return tex


def write_tex(tid, inner_tex):
    with open(os.path.join(dir_path, "tex/preamble.tex")) as f:
        tex = f.read()
    if tid == "all":
        tex = tex.replace("{article}", "{report}")
    tex += "\\begin{document}\n"
    tex += inner_tex
    tex += "\\end{document}"
    with open(os.path.join(tex_path, f"{tid}.tex"), "w") as f:
        f.write(tex)


with open(os.path.join(talks_path, "_timetable.yml")) as f:
    timetable = yaml.load(f, Loader=yaml.FullLoader)

daylist = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
dates = {"Monday": "22 March", "Tuesday": "23 March", "Wednesday": "24 March",
         "Thursday": "25 March", "Friday": "26 March"}

with open(os.path.join(dir_path, "tex/intro.tex")) as f:
    all_tex = f.read()

for day in daylist:
    talks = []
    for i in [1, 2, 3]:
        sess = f"session {i}"
        if sess in timetable[day] and "talks" in timetable[day][sess]:
            for tid in timetable[day][sess]["talks"]:
                tex = make_tex(tid, day, sess)
                talks.append(tex)
    all_tex += "\n\\clearpage\n"
    all_tex += f"\\addcontentsline{{toc}}{{chapter}}{{{day} {dates[day]}}}\n"
    all_tex += "\n\\clearpage\n".join(talks)

write_tex("all", all_tex)

write_citations()

assert os.system(f"cd {tex_path} && xelatex all.tex && biber all"
                 f" && xelatex all.tex && xelatex all.tex && mv all.pdf {pdf_path}") == 0
