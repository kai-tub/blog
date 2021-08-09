import re

from traitlets import List, Unicode, Bool
from nbconvert.preprocessors import Preprocessor

class StringsToMetaDataGroupPreprocessor(Preprocessor):
    strings = List(Unicode(), default_value=[]).tag(config=True)
    prefix = Unicode(default_value="#").tag(config=True)
    metadata_group = Unicode(default_value="tags").tag(config=True)
    remove_line = Bool(default_value=True).tag(config=True)

    def _write_pattern_as_tag(self, pattern, cell):
        m = pattern.search(cell.source)
        if m is not None:
            tag = m.group(1)
            tags = cell.setdefault("metadata", {}).setdefault(self.metadata_group, [])
            if tag not in tags:
                tags.append(tag)
            cell["metadata"][self.metadata_group] = tags
        return cell

    def _build_regex_patterns(self):
        prefix = re.escape(self.prefix)
        escaped_strings = [re.escape(s) for s in self.strings]
        patterns = [
            re.compile(
                rf"""
                ^ # match start of each line
                \s*{prefix}\s* # allow whitespace before and after prefix
                ({string}) # pattern to capture
                \s* # allow any number of whitespaces after command
                $ # match end of each line (excludes \n in MULTILINE)
                [\r\n]* # Capture current and all following empty newlines
            """,
                re.VERBOSE | re.MULTILINE,
            )
            for string in escaped_strings
        ]
        return patterns

    def preprocess_cell(self, cell, resource, index):
        if cell["cell_type"] == "markdown":
            return cell, resource
        for pattern in self._build_regex_patterns():
            cell = self._write_pattern_as_tag(pattern, cell)
            if self.remove_line:
                cell.source = pattern.sub("", cell.source)
        return cell, resource

class ConvertBlockNotesToShortCodes(Preprocessor):
    # In my personal opinion all block-notes cells
    # should be converted to a raw cell to get full
    # control over the output
    # Otherwise there is a difference between the markdown
    # and ipynb compiler pipelines!
    # Use something like python-markdown2 as postprocessor
    # To then reconvert the data part to html if necessary
    short_code_names = List(Unicode(), default_value=[]).tag(config=True)
    to_raw_cell = Bool(default_value=True).tag(config=False)

    def _pattern_to_short_code(self, pattern, cell):
        subbed_source = pattern.sub(r"{{% \1 %}}\2{{% /\1 %}}", cell.source)
        if subbed_source != cell.source:
            cell.source = subbed_source
            if self.to_raw_cell:
                cell.cell_type = "raw"
        return cell

    def _build_regex_patterns(self):
        escaped_sc_names = [re.escape(s) for s in self.short_code_names]
        patterns = [
            re.compile(
                rf"""
                ^\s*>\s*     # allow whitespaces before and after >
                ({sc_name})      # Short-code name
                :\s*         # : then any number of whitespace
                ([^\n]*)     # Catching group for anything but a new line character
                (?:\n|$)     # Non-catching group for either a new line or the end of the text
                """, re.VERBOSE | re.MULTILINE
            )
            for sc_name in escaped_sc_names
        ]
        return patterns

    def preprocess_cell(self, cell, resource, index):
        if cell.cell_type == "code":
            return cell, resource
        for pattern in self._build_regex_patterns():
            cell = self._pattern_to_short_code(pattern, cell)
        return cell, resource
