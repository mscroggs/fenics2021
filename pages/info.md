# Useful information

## The FEniCS project
The [FEniCS project](https://fenicsproject.org/) consists of a large collection of softwares. The current stable version of FEniCS (often called dolfin) is a C++/Python package for solving finite element problems. The dolfin package uses several other libraries:
- [FFC](https://bitbucket.org/fenics-project/ffc/)  (FEniCS Form Compiler)
- [FIAT](https://github.com/FEniCS/fiat/) (FInite element Automatic Tabulator)
- [UFL](https://github.com/FEniCS/ufl/) (Unified Form Language)

If you are using the python interface, you will not notice any of these packages, as they are automatically called by dolfin when required. A large variety of documente demos can be found [here](https://fenicsproject.org/olddocs/dolfin/latest/python/demos.html).

However, if you are using the C++ interface of dolfin, you have to use FFC to compile a UFL file containing your variational formulation before calling the main program. See the following page for [documented demos](https://bitbucket.org/fenics-project/dolfin/src/master/demo/).

## Communication channels and Q&A
To communicate with developers of FEniCS, you can use the Slack [channel](https://app.slack.com/client/T1AFBGYP2/C1AFSEWKU). To sign of for the slack channel, register your email [here](https://fenicsproject-slack-invite.herokuapp.com/).

For general questions about usage and problems/error messages, please use our [Discourse forum](fenicsproject.discourse.group/).

## FEniCSx/DOLFINx
[FEniCSx/DOLFINx](https://github.com/FEniCS/dolfinx/) is the actively developed version of the FEniCS project. It consists of reimplementations of FFC, namely [FFCx](https://github.com/FEniCS/ffcx/) and FIAT, namely [Basix](https://github.com/FEniCS/basix/).

A highlight of new features in DOLFINx include:
- Variational formulations with complex numbers
- Higher order mesh support
- Support for quadrilateral and hexahedral elements

## The DOLFINx tutorial
As the user-api of DOLFINx is quite different from previous releases of dolfin, an interactive tutorial (no installation required) can be found [here](https://github.com/jorgensd/dolfinx-tutorial/).

The tutorial uses interactive Jupyter notebooks (hosted with Binder) such that any used on any computer can run the tutorial.