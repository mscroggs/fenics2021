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
    if "website" in authorinfo:
        info += f" <a href='{authorinfo['website']}'><i class='fa fa-internet-explorer' aria-hidden='true'></i></a>"
    if "github" in authorinfo:
        info += f" <a href='https://github.com/{authorinfo['github']}'><i class='fa fa-github' aria-hidden='true'></i></a>"
    if "twitter" in authorinfo:
        info += f" <a href='https://twitter.com/{authorinfo['twitter']}'><i class='fa fa-twitter' aria-hidden='true'></i></a>"
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
    content += f"<div>{day} session {session_n}</div>"
    content += "<div class='abstract'>"
    if isinstance(tinfo['abstract'], list):
        for parag in tinfo:
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

timetable_content = "<h1>Timetable</h1>"

times = {1: "1:00-2:30", 2: "3:00-4:30", 3: "5:00-6:30"}

#timetable_content += "<table class='timetable'>\n"
#
#timetable_content += "<tr><td class='heading'></td><td class='heading'>Monday</td><td class='heading'>Tuesday</td><td class='heading'>Wednesday</td><td class='heading'>Thursday</td><td class='heading'>Friday</td></tr>\n"
#
#for s in [1, 2, 3]:
#    for talk_n in range(4):
#        timetable_content += "<tr>"
#        if talk_n == 0:
#            timetable_content += f"<td rowspan=4 class='rotated heading'><span>Session {s} ({times[s]})</span></td>"
#        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
#            if s == 2 and day == "Tuesday":
#                if talk_n == 0:
#                    timetable_content += "<td rowspan=4>"
#                    timetable_content += "<div class='timetabletalktitle'>Q&A with the FEniCS steering council</div>"
#                    timetable_content += "</td>"
#            else:
#                if f"session {s}" in timetable[day] and len(timetable[day][f"session {s}"]) > talk_n:
#                    talk_id = timetable[day][f"session {s}"][talk_n]
#                    timetable_content += f"<a href='/talks/{talk_id}.html' class='timetablelink'>"
#                    title, speaker = get_title_and_speaker(talk_id)
#                    timetable_content += f"<div class='timetabletalktitle'>{title}</div>"
#                    timetable_content += f"<div class='timetabletalkspeaker'>{speaker}</div>"
#                    timetable_content += "</a>"
#                else:
#                    timetable_content += "<td>?</td>"
#
#        timetable_content += "</tr>"
#    if s in [1, 2]:
#        timetable_content += "<tr><td class='heading'></td><td style='padding-top:10px;padding-bottom:10px' colspan=5 class='heading'>B &nbsp; &nbsp; R &nbsp; &nbsp; E &nbsp; &nbsp; A &nbsp; &nbsp; K</td></tr>"
#
#timetable_content += "</table>"

daylist = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

timetable_content += "<div class='timetablegrid'>\n"

for s in [1, 2, 3]:
    timetable_content += f"<div class='gridcell timetableheading rotated' style='grid-column: 1 / span 1; "
    timetable_content += f"grid-row: {5 * s - 3} / span 4;'>Session {s} ({times[s]})</div>"

timetable_content += f"<div class='gridcell timetableheading rotated' style='grid-column: 1 / span 1; "
timetable_content += f"grid-row: 17 / span 1;'>Evening session (7:30-9:00)</div>"

timetable_content += "<div class='gridcell timetabletalk' "
timetable_content += f"style='grid-column: 2 / span 1; grid-row: 17 / span 1;'>"
timetable_content += f"<div class='timetabletalktitle'>Drinks reception</div></div>"
timetable_content += "<div class='gridcell timetabletalk' "
timetable_content += f"style='grid-column: 3 / span 1; grid-row: 17 / span 1;'>"
timetable_content += f"<div class='timetabletalktitle'>Discussion tables</div></div>"
timetable_content += "<div class='gridcell timetabletalk' "
timetable_content += f"style='grid-column: 4 / span 1; grid-row: 17 / span 1;'>"
timetable_content += f"<div class='timetabletalktitle'>FEnicS quiz night</div></div>"
timetable_content += "<div class='gridcell timetabletalk' "
timetable_content += f"style='grid-column: 5 / span 1; grid-row: 17 / span 1;'>"
timetable_content += f"<div class='timetabletalktitle'>Conference dinner</div></div>"
timetable_content += "<div class='gridcell timetabletalk' "
timetable_content += f"style='grid-column: 6 / span 1; grid-row: 17 / span 1;'>"
timetable_content += f"<div class='timetabletalktitle'>Hang out and goodbyes</div></div>"

for row in [6, 11, 16]:
    timetable_content += f"<div class='gridcell timetableheading' style='grid-column: 2 / span 5; "
    timetable_content += f"grid-row: {row} / span 1;padding:10px'>"
    timetable_content += " &nbsp; &nbsp; &nbsp; ".join([i for i in "BREAK"])
    timetable_content += "</div>"

timetable_content += "<div class='gridcell timetabletalk' "
timetable_content += "style='grid-column: 3 / span 1; grid-row: 7 / span 4;'>"
timetable_content += "<div class='timetabletalktitle'>"
timetable_content += "Q&A with the FEniCS steering council</div></div>"

for i, day in enumerate(daylist):
    timetable_content += f"<div class='gridcell timetableheading' style='grid-column: {i + 2} / span 1; "
    timetable_content += f"grid-row: 1 / span 1;'>{day}</div>"
    for s in [1, 2, 3]:
        if s == 2 and day == "Tuesday":
            continue
        for talk_n in range(4):
            talkpos = f"grid-column: {i + 2} / span 1; grid-row: {5 * s - 3 + talk_n} / span 1"
            if f"session {s}" in timetable[day] and len(timetable[day][f"session {s}"]) > talk_n:
                talk_id = timetable[day][f"session {s}"][talk_n]
                timetable_content += f"<a class='gridcell timetabletalk' href='/talks/{talk_id}.html' style='{talkpos}'>"
                title, speaker = get_title_and_speaker(talk_id)
                timetable_content += f"<div class='timetabletalktitle'>{title}</div>"
                timetable_content += f"<div class='timetabletalkspeaker'>{speaker}</div>"
                timetable_content += "</a>"
            else:
                timetable_content += f"<div class='gridcell timetabletalk' style='{talkpos}'>?</div>"

timetable_content += "</div>"

write_page("talks/index.html", timetable_content)

timetable_content = "<h1>List of talks</h1>"

for day in daylist:
    timetable_content += f"<h2>{day}</h2>"
    for s in [1, 2, 3]:
        timetable_content += f"<h3>Session {s} ({times[s]})</h3>"
        if f"session {s}" in timetable[day]:
            talks = timetable[day][f"session {s}"]
            for t in talks:
                timetable_content += "<div class='timetablelisttalk'>"
                timetable_content += make_talk_page(t, day, s)
                timetable_content += "</div>"

write_page("talks/list.html", timetable_content)
