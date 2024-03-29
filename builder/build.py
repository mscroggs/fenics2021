import os
import re
import yaml
import argparse
from markup import markup

dir_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description="Build fenics2021.com")

parser.add_argument(
    'destination', metavar='destination', nargs="?",
    default=os.path.join(dir_path, "../_html"),
    help="Destination of HTML files.")

args = parser.parse_args()
html_path = args.destination
files_path = os.path.join(dir_path, "../files")
talks_path = os.path.join(dir_path, "../talks")
slides_path = os.path.join(dir_path, "../slides")
pages_path = os.path.join(dir_path, "../pages")
evening_path = os.path.join(dir_path, "../evening")
template_path = os.path.join(dir_path, "../template")

if os.path.isdir(html_path):
    os.system(f"rm -rf {html_path}")
os.mkdir(html_path)
os.mkdir(os.path.join(html_path, "talks"))
os.mkdir(os.path.join(html_path, "slides"))
os.mkdir(os.path.join(html_path, "evening"))

os.system(f"cp -r {files_path}/* {html_path}")
os.system(f"cp -r {slides_path}/* {html_path}/slides")

with open(os.path.join(html_path, "CNAME"), "w") as f:
    f.write("fenics2021.com")

with open(os.path.join(talks_path, "_timetable.yml")) as f:
    timetable = yaml.load(f, Loader=yaml.FullLoader)

times = {1: "13:00&ndash;14:40", 2: "15:00&ndash;16:30", 3: "17:00&ndash;18:30",
         "evening": "19:30&ndash;21:00"}
daylist = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
extras = {
    "Monday": {"session 1": {"start": ("Welcome & Introduction", "")}},
    "Wednesday": {"session 2": {"start": ("Q&A with the FEniCS steering council", "")}},
    "Friday": {"session 3": {"end": ("Prizes & Conclusion", "")}}
}
prizes = {"phd1": "delaporte-mathurin", "phd2": "marsden",
          "postdoc": "hirschvogel"}

ntalks = {1: 6, 2: 5, 3: 5}
talk_starts = {}
break_positions = {}
for i in [1, 2, 3]:
    if i == 1:
        talk_starts[i] = 2
    else:
        talk_starts[i] = break_positions[i-1] + 1
    break_positions[i] = talk_starts[i] + ntalks[i]
talk_starts["evening"] = break_positions[3] + 1

empty_talks = {"Wednesday": {2: list(range(5))}, "Friday": {3: [3, 4]}}

country_emoji = {
    "Norway": "&#127475;&#127476;",
    "United States": "&#127482;&#127480;",
    "United Kingdom": "&#127468;&#127463;",
    "Sweden": "&#127480;&#127466;",
    "Luxembourg": "&#127473;&#127482;",
    "Canada": "&#127464;&#127462;",
    "Germany": "&#127465;&#127466;",
    "France": "&#127467;&#127479;",
    "Spain": "&#127466;&#127480;",
    "Brazil": "&#127463;&#127479;",
    "Poland": "&#127477;&#127473;",
    "Italy": "&#127470;&#127481;",
    "Switzerland": "&#127464;&#127469;",
    "India": "&#127470;&#127475;",
    "Ireland": "&#127470;&#127466;",
    "Colombia": "&#127464;&#127476;",
    "Morocco": "&#127474;&#127462;",
    "Qatar": "&#127478;&#127462;",
    "Turkey": "&#127481;&#127479;",
    "Finland": "&#127467;&#127470;",
    "French Polynesia": "&#127477;&#127467;",
}


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


def markup_author(authorinfo, bold=False):
    info = ""
    if bold:
        info += "<b>"
    info += authorinfo["name"]
    if bold:
        info += "</b>"
    if "website" in authorinfo:
        info += (f" <a href='{authorinfo['website']}' class='falink'>"
                 "<i class='fab fa-internet-explorer'></i></a>")
    if "github" in authorinfo:
        info += (f" <a href='https://github.com/{authorinfo['github']}' class='falink'>"
                 "<i class='fab fa-github'></i></a>")
    if "twitter" in authorinfo:
        info += (f" <a href='https://twitter.com/{authorinfo['twitter']}' class='falink'>"
                 "<i class='fab fa-twitter'></i></a>")

    if "affiliation" in authorinfo:
        info += f" ({authorinfo['affiliation']}"
        if "country" in authorinfo:
            info += f", {country_emoji[authorinfo['country']]}"
        info += ")"
    return info


def write_page(url, content, title=None):
    if title is None:
        title = "FEniCS 2021"
    else:
        title = "FEniCS 2021: " + title
    with open(os.path.join(html_path, url), "w") as f:
        with open(os.path.join(template_path, "intro.html")) as f2:
            f.write(f2.read().replace("{{pagetitle}}", title))
        f.write(content)
        with open(os.path.join(template_path, "outro.html")) as f2:
            f.write(f2.read())


def get_title_and_speaker(t_id):
    with open(os.path.join(talks_path, f"{t_id}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)
    return tinfo["title"], tinfo["speaker"]["name"]


def make_talk_page(t_id, day, session_n, prev, next):
    with open(os.path.join(talks_path, f"{t_id}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)

    authors = [markup_author(tinfo["speaker"], True)]
    authornames = [tinfo["speaker"]["name"]]
    if "coauthor" in tinfo:
        authors += [markup_author(a) for a in tinfo["coauthor"]]
        authornames += [a["name"] for a in tinfo["coauthor"]]
    authortxt = "".join([f"<div class='authors'>{i}</div>" for i in authors])

    content = ""
    content += f"<h1>{tinfo['title']}</h1>"
    content += f"<div>{authortxt}</div>"
    if day is not None:
        content += (f"<div style='margin-top:5px'>"
                    f"<a href='/talks/list-{day}.html'>{day}</a>"
                    f" session {session_n} (Zoom) ({times[session_n]} GMT)</div>")
    if t_id == prizes["phd1"]:
        content += ("<div style='margin-top:10px'>"
                    "<i class='fas fa-award'></i> This talk won a prize:"
                    " Best talk by a PhD student or undergraduate</div>")
    if t_id == prizes["phd2"]:
        content += ("<div style='margin-top:10px'>"
                    "<i class='fas fa-award'></i> This talk won a prize:"
                    " Best talk by a PhD student or undergraduate (runner up)</div>")
    if t_id == prizes["postdoc"]:
        content += ("<div style='margin-top:10px'>"
                    "<i class='fas fa-award'></i> This talk won a prize:"
                    " Best talk by a postdoc</div>")
    if os.path.isfile(os.path.join(slides_path, f"{t_id}.pdf")):
        content += (f"<div style='margin-top:10px'><a href='/slides/{t_id}.pdf'>"
                    "<i class='fas fa-file-powerpoint'></i> View slides (pdf)</a>")
        if "slide-license" not in tinfo:
            raise RuntimeError(f"Slide license not found ({t_id})")
        content += " (available under a "
        if tinfo["slide-license"] == "CC BY 4.0":
            content += "<a href='https://creativecommons.org/licenses/by/4.0/'>CC BY 4.0</a>"
        elif tinfo["slide-license"] == "CC BY-NC-ND 4.0":
            content += "<a href='https://creativecommons.org/licenses/by-nc-nd/4.0/'>"
            content += "CC BY-NC-ND 4.0</a>"
        else:
            raise ValueError(f"Unknown license for {t_id}: {tinfo['slide-license']}")
        content += " license)"
        content += "</div>"
    if "doi" in tinfo:
        content += (f"<div style='margin-top:10px'><a href='https://dx.doi.org/{tinfo['doi']}'>"
                    f"<i class='fas fa-link'></i> {tinfo['doi']}</a></div>")
    if "slides" in tinfo:
        content += (f"<div style='margin-top:10px'><a href='{tinfo['slides']['url']}'>"
                    "<i class='fas fa-file-powerpoint'></i> View slides on "
                    f"{tinfo['slides']['where']}</a></div>")

    content += ("<div id='cite1' style='margin-top:10px'>"
                "<a href='javascript:show_citation()'>"
                "<i class='fas fa-arrow-down'></i> Cite this talk</a></div>")
    content += ("<div id='cite2' style='margin-top:10px;display:none'>"
                "<p>You can cite this talk by using the following BibTe&Chi;:</p>"
                "<p class='pcode'>"
                f"@incollection{{fenics2021-{t_id},<br />"
                f"&nbsp;&nbsp;&nbsp;&nbsp;title = {{{to_tex(tinfo['title'])}}},<br />"
                "&nbsp;&nbsp;&nbsp;&nbsp;author = {"
                f"{' and '.join([to_tex(i) for i in authornames])}"
                "},<br />"
                "&nbsp;&nbsp;&nbsp;&nbsp;year = {2021},<br />"
                "&nbsp;&nbsp;&nbsp;&nbsp;url = "
                f"{{http://mscroggs.github.io/fenics2021/talks/{t_id}.html}},<br />"
                "&nbsp;&nbsp;&nbsp;&nbsp;booktitle = {Proceedings of FEniCS 2021, online,"
                " 22--26 March},<br />"
                "&nbsp;&nbsp;&nbsp;&nbsp;editor = {Igor Baratta and J{\\o}rgen S. Dokken"
                " and Chris Richarson and Matthew W. Scroggs},<br />")
    if "doi" in tinfo:
        content += f"&nbsp;&nbsp;&nbsp;&nbsp;doi = {{{tinfo['doi']}}},<br />"
    if "pages" in tinfo:
        content += "&nbsp;&nbsp;&nbsp;&nbsp;pages = {"
        content += str(tinfo['pages']).replace('-', '--')
        content += "}<br />"
    content += ("}"
                "</p>"
                "<a href='javascript:hide_citation()'>"
                "<i class='fas fa-arrow-up'></i> Hide citation info</a>"
                "</div>")
    content += ("<script type='text/javascript'>\n"
                "function show_citation(){\n"
                "  document.getElementById('cite1').style.display = 'none';"
                "  document.getElementById('cite2').style.display = 'block';"
                "}\n"
                "function hide_citation(){\n"
                "  document.getElementById('cite2').style.display = 'none';"
                "  document.getElementById('cite1').style.display = 'block';"
                "}\n"
                "</script>")

    content += "<div class='abstract'>"
    abstract = []
    if isinstance(tinfo['abstract'], list):
        for parag in tinfo['abstract']:
            abstract.append(parag)
    else:
        abstract.append(tinfo['abstract'])
    content += markup("\n\n".join(abstract))
    content += "</div>"

    if prev is not None or next is not None:
        content += "<div class='prevnext'>"
        if prev is not None:
            content += "<div class='prevlink'>"
            if prev[0] is not None:
                content += f"<a href='/talks/{prev[0]}.html'>&larr; previous talk"
                if prev[1] is not None:
                    content += f" ({prev[1]})"
                content += "</a>"
            else:
                content += "<i>this is the first talk</i>"
            content += "</div>"
        if next is not None:
            content += "<div class='nextlink'>"
            if next[0] is not None:
                content += f"<a href='/talks/{next[0]}.html'>next talk"
                if next[1] is not None:
                    content += f" ({next[1]})"
                content += " &rarr;</a>"
            else:
                content += "<i>this is the final talk</i>"
            content += "</div>"
        content += "</div>"

    write_page(f"talks/{t_id}.html", content, tinfo['title'])

    short_content = ""
    short_content += "<div class='talktitle'>"
    if t_id in list(prizes.values()):
        short_content += "<i class='fas fa-award'></i> "
    short_content += f"<a href='/talks/{t_id}.html'>{tinfo['title']}</a></div>"
    short_content += f"<div class='timetablelistauthor'>{authortxt}</div>"

    return short_content


for file in os.listdir(pages_path):
    if file.endswith(".md"):
        fname = file[:-3]
        with open(os.path.join(pages_path, file)) as f:
            content = markup(f.read(), False)
        write_page(f"{fname}.html", content)

evenings = {}

for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
    with open(os.path.join(evening_path, f"{day.lower()}.yml")) as f:
        evening_info = yaml.load(f, Loader=yaml.FullLoader)
    content = f"# {evening_info['title']}\n"
    content += f"<div style='margin-top:5px'><a href='/talks/list-{day}.html'>{day}</a>"
    if day == "Friday":
        content += " evening (18:30&ndash; GMT)</div>\n"
    else:
        content += f" evening ({times['evening']} GMT)</div>\n"
    content += "<div class='abstract'>\n"
    content += "\n\n".join(evening_info["desc"])
    content += "</div>"
    write_page(f"evening/{day.lower()}.html", markup(content))

    evening_short = ""
    bracket_open = False
    first = True
    for i in evening_info['desc']:
        if "img" in i:
            continue
        if first:
            first = False
        elif not bracket_open:
            evening_short += "<br /><br />"
        if i.startswith("## "):
            if bracket_open:
                evening_short += ", "
            evening_short += i[3:]
            bracket_open = True
        elif not bracket_open:
            evening_short += i
    if bracket_open:
        bracket_open = False
        evening_short += "."
    evenings[day] = (evening_info['title'], evening_short)

content = "<h1>Timetable</h1>"
content += "<div class='timetablegrid'>\n"

for s in [1, 2, 3]:
    content += "<div class='gridcell timetableheading rotated' style='grid-column: 1 / span 1; "
    content += f"grid-row: {talk_starts[s]} / span {ntalks[s]};'>Session {s} (Zoom) "
    content += f"({times[s]} GMT)</div>"

    if s == 3:
        content += "<div class='gridcell timetableheading' style='grid-column: 2 / span 4; "
    else:
        content += "<div class='gridcell timetableheading' style='grid-column: 2 / span 5; "
    content += f"grid-row: {break_positions[s]} / span 1;padding:10px'>"
    content += " &nbsp; &nbsp; &nbsp; ".join([i for i in "BREAK"])
    content += "</div>"

content += "<div class='gridcell timetableheading rotated' style='grid-column: 1 / span 1; "
content += f"grid-row: {talk_starts['evening']} / span 2;'>"
content += f"Evening session (Gather Town) ({times['evening']} GMT)</div>"


content += "<div class='gridcell timetabletalk' "
content += f"style='grid-column: 4 / span 1; grid-row: {talk_starts[2]} / span {ntalks[2]};'>"
content += f"<div class='timetabletalktitle'>{extras['Wednesday']['session 2']['start'][0]}</div>"
content += f"<div class='timetabletalkspeaker'>{extras['Wednesday']['session 2']['start'][1]}</div>"
content += "</div>"

content += "<div class='gridcell timetabletalk' "
content += "style='grid-column: 2 / span 1; grid-row: 2 / span 1;'>"
content += f"<div class='timetabletalktitle'>{extras['Monday']['session 1']['start'][0]}</div>"
content += f"<div class='timetabletalkspeaker'>{extras['Monday']['session 1']['start'][1]}</div>"
content += "</div>"

content += "<div class='gridcell timetabletalk' "
content += "style='grid-column: 6 / span 1; grid-row: 18 / span 2;'>"
content += f"<div class='timetabletalktitle'>{extras['Friday']['session 3']['end'][0]}</div>"
content += f"<div class='timetabletalkspeaker'>{extras['Friday']['session 3']['end'][1]}</div>"
content += "</div>"

for i, day in enumerate(daylist):
    content += f"<div class='gridcell timetableheading' style='grid-column: {i + 2} / span 1; "
    content += f"grid-row: 1 / span 1;'><a href='/talks/list-{day}.html'>{day}</a></div>"

    content += "<a class='gridcell timetabletalk' "
    content += f"style='grid-column: {i + 2} / span 1; "
    if day == "Friday":
        content += f"grid-row: {talk_starts['evening'] - 1} / span 2;'"
    else:
        content += f"grid-row: {talk_starts['evening']} / span 2;'"
    content += f"href='/evening/{day.lower()}.html'>"
    content += f"<div class='timetabletalktitle'>{evenings[day][0]}</div>"
    content += f"<div class='timetabletalkspeaker'>{evenings[day][1]}</div>"

    content += "</a>"

    for s in [1, 2, 3]:
        add = 0
        if day == "Monday" and s == 1:
            add = 1
        for talk_n in range(ntalks[s] - add):
            if day in empty_talks and s in empty_talks[day] and talk_n in empty_talks[day][s]:
                continue
            talkpos = f"grid-column: {i + 2} / span 1; "
            talkpos += f"grid-row: {talk_starts[s] + add + talk_n} / span 1"
            sess = f"session {s}"
            if sess in timetable[day] and len(timetable[day][sess]["talks"]) > talk_n:
                talk_id = timetable[day][sess]["talks"][talk_n]
                content += (f"<a class='gridcell timetabletalk' href='/talks/{talk_id}.html' "
                            f"style='{talkpos}'>")
                title, speaker = get_title_and_speaker(talk_id)
                content += f"<div class='timetabletalktitle'>{title}</div>"
                content += f"<div class='timetabletalkspeaker'>{speaker}</div>"
                icons = []
                if talk_id in list(prizes.values()):
                    icons.append("<i class='fas fa-award'></i>")

                content += " ".join(icons)
                content += "</a>"

content += "</div>"

write_page("talks/index.html", content)

next_talks = {}
prev_talks = {}
prev = None
prev_note = None
next_note = None
for day in daylist:
    for s in [1, 2, 3]:
        if f"session {s}" in timetable[day] and "talks" in timetable[day][f"session {s}"]:
            talks = timetable[day][f"session {s}"]["talks"]
            for t in talks:
                prev_talks[t] = (prev, prev_note)
                if prev is not None:
                    next_talks[prev] = (t, next_note)
                prev = t
                next_note = None
                prev_note = None
        next_note = "after a break"
        prev_note = "before a break"
    next_note = "on the following day"
    prev_note = "on the previous day"
next_talks[prev] = (None, None)

for t in timetable["other"]:
    content += make_talk_page(t, None, None, None, None)

daytalks = {}
for day in daylist:
    content = ""
    for s in [1, 2, 3]:
        content += f"<h3>Session {s} (Zoom) ({times[s]} GMT)</h3>"
        sess = f"session {s}"
        if sess in timetable[day] and "chair" in timetable[day][sess]:
            chair = timetable[day][sess]["chair"]
            content += "<div class='authors' style='margin-top:-10px;margin-bottom:10px'>"
            content += f"Chair: {markup_author(chair)}"
            content += "</div>"
        if day in extras and sess in extras[day] and "start" in extras[day][sess]:
            content += "<div class='timetablelisttalk'>"
            content += "<div class='talktitle'>" + extras[day][sess]["start"][0] + "</div>"
            content += "<div class='timetablelistauthor'>"
            content += "<div class='authors'>" + extras[day][sess]["start"][1] + "</div>"
            content += "</div></div>"

        if sess in timetable[day] and "talks" in timetable[day][sess]:
            talks = timetable[day][sess]["talks"]
            for t in talks:
                print(t)
                content += "<div class='timetablelisttalk'>"
                content += make_talk_page(t, day, s, prev_talks[t], next_talks[t])
                content += "</div>"

        if day in extras and sess in extras[day] and "end" in extras[day][sess]:
            content += "<div class='timetablelisttalk'>"
            content += "<div class='talktitle'>" + extras[day][sess]["end"][0] + "</div>"
            content += "<div class='timetablelistauthor'>"
            content += "<div class='authors'>" + extras[day][sess]["end"][1] + "</div>"
            content += "</div></div>"

    content += "<h3>Evening session (Gather Town): "
    content += f"<a href='/evening/{day.lower()}.html'>{evenings[day][0]}"
    if day == "Friday":
        content += "</a> (18:30&ndash; GMT)</h3>"
    else:
        content += f"</a> ({times['evening']} GMT)</h3>"
    content += f"<div class='timetablelisttalk'>{evenings[day][1]}</div>"
    daytalks[day] = content

content = "<h1>List of talks</h1>"
for day in daylist:
    content += f"<h2>{day}</h2>{daytalks[day]}"
write_page("talks/list.html", content)

for day in daylist:
    write_page(f"talks/list-{day}.html",
               f"<h1>Talks on {day}</h1>"
               "<div style='margin-top:-15px;font-size:80%'>"
               "<a href='/talks'>(view all days)</a></div>"
               f"{daytalks[day]}")
