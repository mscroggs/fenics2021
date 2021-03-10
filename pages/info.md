# Useful information

## Components of FEniCS
Throughout the conference, you will hear people refer to the different packages that make up FEniCS.
For useful reference, these components are:

### {{icon:DOLFIN}} 
DOLFIN is a C++/Python finite element library, and is the main component that most users interact with.

### {{icon:FFC}} 
FFC (the FEniCS Form Compiler) is a library that generates C++ code that can be used in assembly.

### {{icon:FIAT}}
FIAT (the FInite element Automatic Tabulator) contains the definitions of finite element spaces, and can evaluate basis functions.

### {{icon:UFL}}
UFL (Unified Form Language) is the language in which forms can be written. These can then be interpreted by FFC and used to
generate code.

## Components of FEniCSx
FEniCSx is the new version of FEniCS that is currently actively developed. New features in DOLFINx include:

<ul>
<li>Variational formulations with complex numbers</li>
<li>Higher order mesh support</li>
<li>Support for quadrilateral and hexahedral elements</li>
</ul>

For useful reference, the components of FEniCSx are:

### {{icon:DOLFINx}} 
DOLFINx is the new version of DOLFIN.

### {{icon:FFCx}} 
FFCx (the FEniCSx Form Compiler) is the new version of FFC.

### {{icon:Basix}}
Basix is FEniCSx's new element tabulator.

### {{icon:UFL}}
<i>(see above)</i>

## Communication channels and Q&A
There are a few ways that developers and users of FEniCS communicate online.

### Slack
The [FEniCS Slack channel](https://app.slack.com/client/T1AFBGYP2/C1AFSEWKU) is used for chat and discussions between developers and users.
You might like to use this channel to follow up on discussions started at FEniCS 2021.
To sign up for the slack channel, register your email [here](https://fenicsproject-slack-invite.herokuapp.com/).

### Discourse
Questions about usage of FEniCS can be posted on the [FEnics Discourse group](http://fenicsproject.discourse.group).

### GitHub issue tracker
Bugs and errors in FEniCSx are posted on the [GitHub issue tracker](https://github.com/FEniCS/dolfinx/issues).

### Q&A forum (deprecated)
Before moving to Discourse, the FEniCS Q&A forum was used for asking questions about usage. New questions cannot be posted, but
some users may find [the archives](https://fenicsproject.org/qa/) helpful.

## Useful links
[The DOLFINx tutorial](https://jorgensd.github.io/dolfinx-tutorial/){fenics.png} is an interactive guide to the features of FEniCSx.
The tutorial uses Jupyter notebooks (hosted with Binder) that can be run online without any installation required.

[DefElement](https://defelement.com){defelement.png} is an encyclopedia of finite element definitions. It contains information about common (and less common)
finite element basis functions are defined.
