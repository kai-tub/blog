import nbconvert
import nbformat

current_nbformat = nbformat.current_nbformat
NBCONVERT_VERSION_MAJOR = int(nbconvert.__version__.partition(".")[0])

import nikola.shortcodes as sc
import nikola.plugins.compile.ipynb as ipynb


class CompileIPynbShortCode(ipynb.CompileIPynb):
    name = "ipynb_sc_last"
    friendly_name = "Jupyter Notebook Convert Shortcodes Last"
    default_kernel = "python3"
    demote_headers = True
    supports_metadata = True

    def compile_string(
        self, data, source_path=None, is_two_file=True, post=None, lang=None
    ):
        """Compile notebooks into HTML strings."""
        output = self._compile_string(nbformat.reads(data, current_nbformat))
        new_output, shortcodes = sc.extract_shortcodes(output)
        return self.site.apply_shortcodes_uuid(
            new_output, shortcodes, filename=source_path, extra_context={"post": post}
        )
