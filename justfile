# builds and serves a site; automatically detects site changes, rebuilds, and optionally refreshes a browse
env_name := "blog"
env_run_cmd := "mamba run --name " + env_name

# Install environment, build theme files and build-website
all: install-all build-theme clean build

run:
	{{env_run_cmd}} nikola auto --browser

run-clean: clean run

clean:
	{{env_run_cmd}} nikola clean -a -c --forget

# build nikola website
build:
	{{env_run_cmd}} nikola build

build-theme:
	{{env_run_cmd}} just {{justfile_directory()}}/themes/tailwind/

# Install all dependencies with mamba and install nbstripout filter to clean notebooks
install-all: install-base install-poetry

install-poetry:
	{{env_run_cmd}} python -m poetry install
	{{env_run_cmd}} python -m ipykernel install --user
	{{env_run_cmd}} nbstripout --install

install-base:
	mamba env create --file {{justfile_directory()}}/env.yml --name {{env_name}} --force
