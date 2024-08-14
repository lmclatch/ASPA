# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
project = 'ASPA WUDR'
copyright = '2024, Liza McLatchy & Chris Shuler'
author = 'Liza McLatchy & Chris Shuler'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',        # Automatically document your code
    'sphinx.ext.viewcode',       # Add links to highlighted source code
    'sphinx.ext.githubpages',    # Support for publishing via GitHub Pages
    'sphinx.ext.napoleon',       # Support for Google and NumPy style docstrings
    'sphinx.ext.todo',           # Support for TODO notes
    'sphinx.ext.coverage',       # Coverage checker for documentation
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'  # Use the popular Read the Docs theme
html_static_path = ['_static']

# -- Sidebar Configuration ---------------------------------------------------
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'searchbox.html',
        'relations.html',  # Links to previous/next chapters
        'sourcelink.html', # Link to view the source
        'versions.html',   # Version control dropdown
        'localtoc.html',   # Local table of contents
        'globaltoc.html',  # Global table of contents
        'sidebarlinks.html' # Custom sidebar links
    ],
    'background': [
        'localtoc.html',   # Local table of contents for Background section
        'relations.html',
    ],
    'serverless': [
        'localtoc.html',   # Local table of contents for Serverless Functions
        'relations.html',
    ],
    'pipeline': [
        'localtoc.html',   # Local table of contents for Data Pipeline
        'relations.html',
    ],
}

# -- Extension Configuration -------------------------------------------------
# Enable TODOs to be shown in the output
todo_include_todos = True
