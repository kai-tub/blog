# builds and serves a site; automatically detects site changes, rebuilds, and optionally refreshes a browse
auto-build:
	nikola auto --browser

clean-auto-build:
	nikola clean -a -c --forget
	nikola auto --browser

# build nikola website
build-website:
	nikola build

build-theme:
	just {{justfile_directory()}}/themes/tailwind/

# Install environment, build theme files and build-website
build-all-clean: install build-theme build-website

# Install all dependencies with mamba and install nbstripout filter to clean notebooks
install: install-base install-poetry

install-poetry:
	mamba run --name blog python -m poetry install
	mamba run --name blog python -m ipykernel install --user
	mamba run --name blog nbstripout --install

install-base:
	mamba env create --file {{justfile_directory()}}/env.yml --name blog --force
