# builds and serves a site; automatically detects site changes, rebuilds, and optionally refreshes a browse
auto-build:
	nikola auto --browser

# build nikola website
build-website:
	nikola build

# Install all dependencies with mamba and install nb-clean filter to ensure that commits aren't dirty
install:
	mamba env create --file {{justfile_directory()}}/env.yml --force
	nb-clean add-filter --preserve-cell-metadata
