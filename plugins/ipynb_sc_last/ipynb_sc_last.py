import datetime
import io
from functools import partial
from pathlib import Path

import nbconvert
import nbformat
from nbformat import NotebookNode

current_nbformat = nbformat.current_nbformat
NBCONVERT_VERSION_MAJOR = int(nbconvert.__version__.partition(".")[0])

import re
from typing import Dict

import fnc
import nikola.plugins.compile.ipynb as ipynb
import nikola.shortcodes as sc
from nikola.utils import LocaleBorg
from ruamel.yaml import YAML

TITLE_PATTERN = re.compile(r"#\s*(.*)$", re.MULTILINE)
DESCRIPTION_PATTERN = re.compile(
    r"""
    >\s*  # Description prefix
    (.*?) # Lazily grap everything into group until:
    (?:   # Start non-capturing group
      $   # cell source ends
      |   # OR
      \n$ # cell source ends with a newline
      |   # OR
      \n[\ \t\r]*\n # Until two consecutive _empty_ (whitespace only is allowed) newlines are processed.
    )
    """,
    re.DOTALL | re.VERBOSE,
)


def _escape_yml_string(s: str) -> str:
    escaped_str = s.replace("'", "''")
    return f"'{escaped_str}'"


def _md_title_to_yml(text: str) -> str:
    """
    Finds a markdown h1 header `#` and converts the data
    to a yaml element `-` (replaces the `#` with `- title: `)
    Auto-escapes string!
    """

    def _to_escaped_title(matchobj: re.Match) -> str:
        yml_str = _escape_yml_string(matchobj.group(1))
        return f"- title: {yml_str}"

    return TITLE_PATTERN.sub(_to_escaped_title, text)


def _md_description_to_yml(text: str) -> str:
    """
    Finds a markdown block-quote `>` and converts the data
    to a yaml element `-` (replaces the `>` with `- description: `)
    Auto-escapes string!
    """

    def _to_escaped_description(matchobj: re.Match) -> str:
        yml_str = _escape_yml_string(matchobj.group(1))
        # newline is eaten by regex
        return f"- description: {yml_str}\n"

    return DESCRIPTION_PATTERN.sub(_to_escaped_description, text)


def _read_custom_metadata_style(cell_text: str) -> Dict:
    y = YAML(typ="safe")
    dicts = fnc.compose(_md_title_to_yml, _md_description_to_yml, y.load)(cell_text)
    return {k: v for d in dicts for k, v in d.items()}


def _parse_modified_date(file_path):
    return fnc.compose(
        Path,
        lambda p: p.stat().st_mtime,
        datetime.datetime.fromtimestamp,
        lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S %Z"),
    )(file_path)


def _skip_first_md_cell(nb_node: NotebookNode):
    md_idx = fnc.findindex(lambda cell: cell.cell_type == "markdown", nb_node.cells)
    if md_idx == -1:
        return nb_node
    nb_node.cells.pop(md_idx)
    return nb_node


class CompileIPynbShortCode(ipynb.CompileIPynb):
    name = "ipynb_sc_last"
    friendly_name = "Jupyter Notebook Convert Shortcodes Last"
    default_kernel = "python3"
    demote_headers = False  # Assume that the title header is set!
    supports_metadata = True

    def compile_string(
        self, data, source_path=None, is_two_file=True, post=None, lang=None
    ):
        """Compile notebooks into HTML strings."""
        output = fnc.compose(
            partial(nbformat.reads, as_version=current_nbformat),
            _skip_first_md_cell,
            self._compile_string,
        )(data)
        # output = self._compile_string(nbformat.reads(data, current_nbformat))
        new_output, shortcodes = sc.extract_shortcodes(output)
        return self.site.apply_shortcodes_uuid(
            new_output, shortcodes, filename=source_path, extra_context={"post": post}
        )

    def read_metadata(self, post, lang=None):
        """
        Read metadata directly from ipynb file.
        Will read metadata from first markdown cell.
        Uses general yaml syntax, except for special syntax
        for title (h1 header with `#`) and description (block quote with `>`)
        """
        self._req_missing_ipynb()
        if lang is None:
            lang = LocaleBorg().current_lang
        source = post.translated_source_path(lang)

        with io.open(source, "r", encoding="utf-8-sig") as in_file:
            nb = nbformat.read(in_file, current_nbformat)
        md_cells = [cell for cell in nb.cells if cell["cell_type"] == "markdown"]
        if len(md_cells) == 0:
            return {}
        metadata_source = md_cells[0]["source"]
        default_metadata = {"date": _parse_modified_date(source)}
        return {**default_metadata, **_read_custom_metadata_style(metadata_source)}
