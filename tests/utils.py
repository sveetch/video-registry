"""
Test utilities
"""
from pyquery import PyQuery as pq


def html_pyquery(content):
    """
    Shortand to use Pyquery parsing on given content.

    This is more useful to dig in advanced HTML content. PyQuery is basically a
    wrapper around ``lxml.etree`` it helps with a more intuitive API (alike
    Jquery) to traverse elements but when reaching a node content it will
    return ``lxml.html.HtmlElement`` object which have a less intuitive API
    but with more features and more flexible with whitespaces.

    Arguments:
        content (TemplateResponse or string): HTML content to parse.

    Returns:
        pyquery.PyQuery: A PyQuery object.
    """
    return pq(
        content,
        parser="html"
    )
