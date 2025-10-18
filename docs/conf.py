import os
import sys

import datawrapper

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("_ext"))

extensions = [
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "myst_parser",
    "parameter_table",
    "enum_table",
]

templates_path = ["_templates"]
source_suffix = [".rst", ".md"]
master_doc = "index"

project = "Datawrapper"
copyright = "2023, Sergio Sánchez Zavala"
author = "Sergio Sánchez Zavala"

version = datawrapper.__version__
release = datawrapper.__version__

language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

pygments_style = "sphinx"

html_static_path = ["static"]
html_theme = "sphinx_rtd_theme"
html_title = "datawrapper"

autodoc_default_flags = ["members", "inherited-members"]
autodoc_member_order = "groupwise"
autosummary_generate = True
