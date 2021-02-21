import os
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
pages_path = os.path.join(dir_path, "../pages")
template_path = os.path.join(dir_path, "../template")

if os.path.isdir(html_path):
    os.system(f"rm -rf {html_path}")
os.mkdir(html_path)
os.mkdir(os.path.join(html_path, "talks"))

os.system(f"cp -r {files_path}/* {html_path}")

with open(os.path.join(html_path, "CNAME"), "w") as f:
    f.write("fenics2021.com")


def markup_author(authorinfo, bold=False):
    info = ""
    if bold:
        info += "<b>"
    info += authorinfo["name"]
    if bold:
        info += "</b>"
    icons = []
    if "website" in authorinfo:
        icons.append(f"<a href='{authorinfo['website']}'>"
                     "<i class='fa fa-fw fa-internet-explorer' aria-hidden='true'></i></a>")
    if "github" in authorinfo:
        icons.append(f"<a href='https://github.com/{authorinfo['github']}'>"
                     "<i class='fa fa-fw fa-github' aria-hidden='true'></i></a>")
    if "twitter" in authorinfo:
        icons.append(f"<a href='https://twitter.com/{authorinfo['twitter']}'>"
                     "<i class='fa fa-fw fa-twitter' aria-hidden='true'></i></a>")
        info += " " + "".join(icons)

    if "affiliation" in authorinfo:
        info += f" ({authorinfo['affiliation']})"
    return info


def write_page(url, content):
    with open(os.path.join(html_path, url), "w") as f:
        with open(os.path.join(template_path, "intro.html")) as f2:
            f.write(f2.read())
        f.write(content)
        with open(os.path.join(template_path, "outro.html")) as f2:
            f.write(f2.read())


def get_title_and_speaker(t_id):
    with open(os.path.join(talks_path, f"{t_id}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)
    return tinfo["title"], tinfo["speaker"]["name"]


def make_talk_page(t_id, day, session_n):
    with open(os.path.join(talks_path, f"{t_id}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)

    authors = [markup_author(tinfo["speaker"], True)]
    if "coauthor" in tinfo:
        authors += [markup_author(a) for a in tinfo["coauthor"]]
    authortxt = ", ".join(authors[:-1])
    if len(authors) > 1:
        if len(authors) > 2:
            authortxt += ","
        authortxt += " and "
    authortxt += authors[-1]

    content = ""
    content += f"<h1>{tinfo['title']}</h1>"
    content += f"<div>{authortxt}.</div>"
    content += (f"<div style='margin-top:5px'>"
                f"<a href='/talks/list-{day}.html'>{day}</a>"
                f" session {session_n} ({times[session_n]})</div>")
    content += "<div class='abstract'>"
    if isinstance(tinfo['abstract'], list):
        for parag in tinfo['abstract']:
            content += f"<p>{parag}</p>"
    else:
        content += f"<p>{tinfo['abstract']}</p>"
    content += "</div>"

    write_page(f"talks/{t_id}.html", content)

    short_content = ""
    short_content += f"<a href='/talks/{t_id}.html'>"
    short_content += f"<div class='talktitle'>{tinfo['title']}</div>"
    short_content += f"</a>"
    short_content += f"<div class='timetablelistauthor'>{authortxt}.</div>"

    return short_content


for file in os.listdir(pages_path):
    if file.endswith(".md"):
        fname = file[:-3]
        with open(os.path.join(pages_path, file)) as f:
            content = markup(f.read())
        write_page(f"{fname}.html", content)

with open(os.path.join(talks_path, "timetable.yml")) as f:
    timetable = yaml.load(f, Loader=yaml.FullLoader)

times = {1: "13:00-14:30", 2: "15:00-16:30", 3: "17:00-18:30"}
daylist = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

content = "<h1>Timetable</h1>"
content += "<div class='timetablegrid'>\n"

for s in [1, 2, 3]:
    content += f"<div class='gridcell timetableheading rotated' style='grid-column: 1 / span 1; "
    content += f"grid-row: {5 * s - 3} / span 4;'>Session {s} ({times[s]})</div>"

content += f"<div class='gridcell timetableheading rotated' style='grid-column: 1 / span 1; "
content += f"grid-row: 17 / span 1;'>Evening session (19:30-21:00)</div>"

content += "<div class='gridcell timetabletalk' "
content += f"style='grid-column: 2 / span 1; grid-row: 17 / span 1;'>"
content += f"<div class='timetabletalktitle'>Drinks reception</div></div>"
content += "<div class='gridcell timetabletalk' "
content += f"style='grid-column: 3 / span 1; grid-row: 17 / span 1;'>"
content += f"<div class='timetabletalktitle'>Discussion tables</div></div>"
content += "<div class='gridcell timetabletalk' "
content += f"style='grid-column: 4 / span 1; grid-row: 17 / span 1;'>"
content += f"<div class='timetabletalktitle'>FEniCS quiz night</div></div>"
content += "<div class='gridcell timetabletalk' "
content += f"style='grid-column: 5 / span 1; grid-row: 17 / span 1;'>"
content += f"<div class='timetabletalktitle'>Conference dinner</div></div>"
content += "<div class='gridcell timetabletalk' "
content += f"style='grid-column: 6 / span 1; grid-row: 17 / span 1;'>"
content += f"<div class='timetabletalktitle'>Hang out and goodbyes</div></div>"

for row in [6, 11, 16]:
    content += f"<div class='gridcell timetableheading' style='grid-column: 2 / span 5; "
    content += f"grid-row: {row} / span 1;padding:10px'>"
    content += " &nbsp; &nbsp; &nbsp; ".join([i for i in "BREAK"])
    content += "</div>"

content += "<div class='gridcell timetabletalk' "
content += "style='grid-column: 3 / span 1; grid-row: 7 / span 4;'>"
content += "<div class='timetabletalktitle'>"
content += "Q&A with the FEniCS steering council</div></div>"

for i, day in enumerate(daylist):
    content += f"<div class='gridcell timetableheading' style='grid-column: {i + 2} / span 1; "
    content += f"grid-row: 1 / span 1;'>{day}</div>"
    for s in [1, 2, 3]:
        if s == 2 and day == "Tuesday":
            continue
        for talk_n in range(4):
            talkpos = f"grid-column: {i + 2} / span 1; grid-row: {5 * s - 3 + talk_n} / span 1"
            if f"session {s}" in timetable[day] and len(timetable[day][f"session {s}"]) > talk_n:
                talk_id = timetable[day][f"session {s}"][talk_n]
                content += (f"<a class='gridcell timetabletalk' href='/talks/{talk_id}.html' "
                            f"style='{talkpos}'>")
                title, speaker = get_title_and_speaker(talk_id)
                content += f"<div class='timetabletalktitle'>{title}</div>"
                content += f"<div class='timetabletalkspeaker'>{speaker}</div>"
                content += "</a>"
            else:
                content += f"<div class='gridcell timetabletalk' style='{talkpos}'>?</div>"

content += "</div>"

write_page("talks/index.html", content)

daytalks = {}
for day in daylist:
    content = ""
    for s in [1, 2, 3]:
        content += f"<h3>Session {s} ({times[s]})</h3>"
        if f"session {s}" in timetable[day]:
            talks = timetable[day][f"session {s}"]
            for t in talks:
                content += "<div class='timetablelisttalk'>"
                content += make_talk_page(t, day, s)
                content += "</div>"
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
