# -- IMPORTS --

# -- Standard libraries --
import importlib
import json
import os
import sys

from datetime import datetime

# -- 3rd party libraries --

# -- Internal libraries --


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
#
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath('.')), 'src'))

import continuedfractions

from continuedfractions.__version__ import __version__

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

author = 'S. R. Murthy'
copyright = f'S. R. Murthy, {datetime.now().year}'
description = """
              Object-oriented continued fractions with Python.
              """
github_url = 'https://github.com'
github_repo = f'{github_url}/sr-murty/continuedfractions'
github_version = 'main'
pypi_project = 'https://pypi.org/project/continuedfractions/'
project = continuedfractions.__name__
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Define master TOC
master_doc = 'index'

# Native docs language
language = 'en'

# Minimum required version of Sphinx - not required ATM
#needs_sphinx >= '7.2.5'

# Set primary domain to null
primary_domain = None

# Global substitutions - not all used
rst_epilog = f"""
.. |author|                 replace:: **{author}**
.. |copyright|              replace:: **{copyright}**
.. |docs_url|               replace:: ''
.. |project|                replace:: **{project}**
.. |project_description|    replace:: {description}
.. |release|                replace:: **{release}**
.. |github_release_target|  replace:: https://github.com/sr-murthy/continuedfractions/releases/tag/{release}
.. |pypi_release_target|    replace:: https://pypi.org/project/continuedfractions/{release}
"""

# Publish author(s)
show_authors = True

# Sphinx extensions - not all are used or required, but still listed
# in case they may be required at some point.
extensions = ['jupyter_sphinx',
              'matplotlib.sphinxext.plot_directive',
              'myst_parser',
              'nb2plots',
              'numpydoc',
              'sphinx.ext.autodoc',
              #'sphinx.ext.autosectionlabel',
              #'sphinx.ext.autosummary',
              'sphinx.ext.coverage',
              'sphinx.ext.doctest',
              'sphinx.ext.duration',
              'sphinx.ext.extlinks',
              'sphinx.ext.graphviz',
              'sphinx.ext.inheritance_diagram',
              'sphinx.ext.intersphinx',
              #'sphinx.ext.linkcode',
              'sphinx.ext.mathjax',
              'sphinx.ext.napoleon',
              'sphinx.ext.todo',
              'sphinx.ext.viewcode',
              'sphinx_copybutton',
              'sphinx_design',]

# Autodoc settings -
#     For more on all available autodoc defaults see
#         https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_default_options
autodoc_default_options = {
    'exclude-members': '__call__,__weakref__,__slots__,__match_args__,elements,from_elements',
    'member-order': 'bysource',
    'private-members': True,
    'special-members': ''
}

# Sphinx autodoc autosummary settings
autosummary_generate = False

# Numpydoc settings
numpydoc_show_class_members = True
numpydoc_show_inherited_class_members = False
numpydoc_class_members_toctree = False
numpydoc_attributes_as_param_list = False
numpydoc_xref_param_type = False

# Intersphinx mappings to reference external documentation domains
intersphinx_mapping = {
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'networkx': ('https://networkx.org/documentation/stable/', None),
    'numpy':  ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'pdm': ('https://pdm-project.org/latest/', None),
    'pygraphviz': ('https://pygraphviz.github.io/documentation/stable/', None),
    'python': ('https://docs.python.org/3', None),
    'sympy': ('https://docs.sympy.org/latest/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build',
                    'Thumbs.db',
                    '.DS_Store',]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of prefixes that are ignored when creating the module index.
modindex_common_prefix = ["continuedfractions."]

doctest_global_setup = "import continuedfractions"

# If this is True, the ``todo`` and ``todolist`` extension directives
# produce output, else they produce nothing. The default is ``False``.
todo_include_todos = True

# -- Project file data variables ---------------------------------------------

# HTML global context for templates
html_context = {
    'authors': author,
    'copyright': copyright,
    'default_mode': 'dark',
    'display_github': True,
    'github_url': 'https://github.com',
    'github_user': 'sr-murthy',
    'github_repo': 'continuedfractions',
    'github_version': 'main',
    'doc_path': 'docs',
    'conf_path': 'docs/conf.py',
    'project': project,
    'project_description': description,
    'release': release,
    'release_target': f'https://github.com/sr-murthy/continuedfractions/releases/tag/{release}'
}

# -- Options for HTML output ----------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# General (non-theme) HTML output options
html_baseurl = 'https://continuedfractions.readthedocs.io/en/latest/'

html_sidebars = {
    "sources/continued-fractions": [],
    "sources/sequences": [],
    "sources/rational-points": [],
    "sources/continuedfractions/*": ["sidebar-nav-bs"],
    "sources/contributing": [],
}

# HTML theme options
html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    'collapse_navigation': False,
    'footer_end': ['author'],
    'footer_start': ['copyright', 'sphinx-version', 'theme-version'],
    'icon_links': [
        {
            'name': 'continuedfractions@GitHub',
            'url': f'https://github.com/sr-murthy/continuedfractions',
            'icon': 'fa-brands fa-github',
        },
    ],
    'navbar_persistent': ['search-button'],
    'navbar_align': 'content',
    'navbar_center': ['navbar-nav'],
    'navbar_end': ['theme-switcher', 'navbar-icon-links'],
    'navbar_start': ['navbar-logo'],
    'navigation_depth': 4,
    "primary_sidebar_end": ["indices", "sidebar-ethical-ads"],
    'secondary_sidebar_items': ['page-toc', 'edit-this-page', 'sourcelink'],
    'show_nav_level': 2,
    'show_toc_level': 2,
    'use_edit_page_button': False,
}

html_logo = '_static/logo.png'

# Relative path (from the ``docs`` folder) to the static files folder - so
# ``_static`` should be one level below ``docs``.
html_static_path = ['_static']

# Custom CSS file(s) - currently source the Font Awesome CSS classes to support
# Font Awesome icons. for more information see:
#
#     https://sphinx-design.readthedocs.io/en/latest/badges_buttons.html#fontawesome-icons
#
html_css_files = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css',
]

# Timestamp format for the last page updated time
html_last_updated_fmt = '%b %d, %Y'

# Show link to ReST source on HTML pages
html_show_sourcelink = True

# If true, the reST sources are included in the HTML build as _sources/<name>.
html_copy_source = True

# Output file base name for HTML help builder - use the project name
htmlhelp_basename = 'continuedfractions'
