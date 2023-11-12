"""Sphinx configuration."""
project = "drf-base64-binaryfield"
author = "Storm Heg"
copyright = "2023, Storm Heg"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
