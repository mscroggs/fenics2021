FEniCS 2021
===========

This repo contains code to build the website for the FEniCS 2021 conference.

Building locally
----------------
To build [fenics2021.com](https://fenics2021.com), clone this repository
and run:

```bash
python3 builder/build.py
```

By default, this will build the website in a folder called `_html` in the
root folder of the repo. You can optionally set the location of the build
by running:

```bash
python3 builder/build.py /path/to/html/folder
```

Updating the website
--------------------
When changes are pushed to the main branch, the website will automatically
be built and updated.

License
-------
The code to generate the FEniCS 2021 (contained in the folders `builder/`,
`template/`, and `test/`, as well as the file `files/sty.css`) is released
under an [MIT license](/LICENSE). Copyright of other files is held by the
presenters of the talks that the files are relevant to.
