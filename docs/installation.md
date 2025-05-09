# Installation

- [Install poethepoet](#install-poethepoet)
- [Install from Github](#install-from-github)
- [Start `quail` PyWPS service](#start-quail-pywps-service)
- [Run `quail` as Docker container](#run-quail-as-docker-container)
- [Use Ansible to deploy `quail` on your System](#use-ansible-to-deploy-quail-on-your-system)

## Poethepoet tasks

[Poethepoet](https://github.com/nat-n/poethepoet) is a task runner that integrates smoothly with [Poetry](https://python-poetry.org/), serving as a modern alternative to Makefiles.

### Install poethepoet

```
$ python3 -m pip install --user pipx
$ python3 -m pipx ensurepath # Ensure directory where pipx stores apps is in your PATH environment variable
$ pipx install poethepoet # Install globally
```

### Usage

Once installed, you can list all available tasks using:

```
poe --help
```

This will output a list of predefined tasks from your pyproject.toml. Example:

```
 # View all tasks
 poe --help
  install-apt           Install required system libraries for R packages
  install-r-pkgs        Install required R packages
  install               Install Python project dependencies using Poetry
  develop               Install development dependencies using Poetry
  start                 Start the Quail service in detached mode
  stop                  Stop the quail service
  restart               Restart the Quail service
  status                Show the status of the Quail service
  dist                  Build a distribution package for the project
  test                  Run fast, offline unit tests
  test-all              Run all tests, including online ones
  lint                  Check code formatting using Black
  prepare-notebooks     Download the output sanitizer config for notebook tests
  test-notebooks        Run all local notebook tests with sanitized output
  test-notebooks-local  Run notebook tests locally using nbval with sanitization
  docs                  Convert notebooks to HTML for documentation
```

You can run any task with:

```
poe <task-name>
# Example:
poe test
```

## Install from GitHub

Check out code from the quail GitHub repo and start the installation:

```
$ git clone https://github.com/pacificclimate/quail.git
$ cd quail
```

Install requirements:

```
poe install-apt
poe install-r-pkgs
poe install
```

For development you can use this command:

```
poe develop
```

## Start `quail` PyWPS service

After successful installation you can start the service using the `quail` command-line.

```
poetry run quail --help # show help
poe start  # start service with default configuration

# OR

poetry run quail start --daemon # start service as daemon
loading configuration
forked process id: 42
```

The deployed WPS service is by default available on:

http://localhost:5000/wps?service=WPS&version=1.0.0&request=GetCapabilities.

NOTE:: Remember the process ID (PID) so you can stop the service with `kill PID`.

You can find which process uses a given port using the following command (here for port `5000`):

```
$ netstat -nlp | grep :5000
```

Check the log files for errors:

```
$ tail -f  pywps.log
```

... or do it the lazy way

You can also use `Poe` to start and stop the service:

```
$ poe start
$ poe status
$ tail -f pywps.log
$ poe stop
```

## Run `quail` as Docker container

You can also run `quail` as a Docker container.

```
$ docker-compose build
$ docker-compose up
```

`quail` will be available on port `8103`.

## Use Ansible to deploy `quail` on your System

Use the [Ansible playbook](http://ansible-wps-playbook.readthedocs.io/en/latest/index.html) for PyWPS to deploy `quail` on your system.
