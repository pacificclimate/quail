# Installation
- [Install from Github](#install-from-github)
- [Start `quail` PyWPS service](#start-quail-pywps-service)
- [Run `quail` as Docker container](#run-quail-as-docker-container)
- [Use Ansible to deploy `quail` on your System](#use-ansible-to-deploy-quail-on-your-system)

## Install from GitHub

Check out code from the quail GitHub repo and start the installation:
```
$ git clone https://github.com/pacificclimate/quail.git
$ cd quail
```

Create Python environment named `venv`:
```
$ python3 -m venv venv
$ source venv/bin/activate
```

Install requirements:
```
(venv)$ pip install -r requirements.txt
```

Install quail app:
```
(venv)$ pip install -e .
# OR
$ make install
```

For development you can use this command:
```
$ pip install -e .[dev]
# OR
$ make develop
```

## Start `quail` PyWPS service
After successful installation you can start the service using the `quail` command-line.

```
(venv)$ quail --help # show help
(venv)$ quail start  # start service with default configuration

# OR

(venv)$ quail start --daemon # start service as daemon
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

You can also use the `Makefile` to start and stop the service:
```
$ make start
$ make status
$ tail -f pywps.log
$ make stop
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
