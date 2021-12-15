# builds and serves a site; automatically detects site changes, rebuilds, and optionally refreshes a browse
env_name := "blog"
env_run_cmd := "mamba run --live-stream --name " + env_name

# Install environment, build theme files and build-website
all: install build-theme clean build

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
install:
	mamba env create --file {{justfile_directory()}}/lock.yml --name {{env_name}} --force
	{{env_run_cmd}} python -m ipykernel install --user
	{{env_run_cmd}} nbstripout --install
	# get bleeding edge of Nikola, as I am waiting for a bug-fix...
	{{env_run_cmd}} python -m pip install --ignore-installed -U git+https://github.com/getnikola/nikola.git

update-dependencies: install-no-lock build write-lock

install-no-lock:
	mamba env create --file {{justfile_directory()}}/env.yml --name {{env_name}} --force
	{{env_run_cmd}} python -m ipykernel install --user
	{{env_run_cmd}} nbstripout --install
	# get bleeding edge of Nikola, as I am waiting for a bug-fix...
	# --no-deps doesn't fix the issue.
	{{env_run_cmd}} python -m pip install --ignore-installed -U git+https://github.com/getnikola/nikola.git

sync-nikola-master:
	# get bleeding edge of Nikola, as I am waiting for a bug-fix...
	# --no-deps doesn't fix the issue.
	{{env_run_cmd}} python -m pip install --ignore-installed -U git+https://github.com/getnikola/nikola.git


write-lock:
	mamba env export > lock.yml
