# JVM Graph

A tool to generate a visualization from the [plugin installation trend JVMs JSON](https://stats.jenkins.io/plugin-installation-trend/jvms.json):

<img src="https://ci.jenkins.io/job/Reporting/job/jvm-graph/job/master/lastSuccessfulBuild/artifact/jvm-graph.png">

This tool:

* Downloads the plugin installation trend JVMs JSON from `stats.jenkins.io`.
* Generates the visualization.
* Opens the visualization in a new tab in your web browser.

## Setup

This tool requires a Python 3 virtual environment:

```sh
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -U pip setuptools
$ pip install -r requirements.txt
```

## Usage

```sh
$ python jvm-graph.py -h
usage: jvm-graph.py [-h] [-o OUTPUT] [-j JVMS_JSON] [--open | --no-open]

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        The name of the output file to create. (default: jvm-graph.png)
  -j JVMS_JSON, --jvms-json JVMS_JSON
                        The plugin installation trend JVMs JSON file to fetch. (default: https://stats.jenkins.io/plugin-installation-trend/jvms.json)
  --open, --no-open     Open the output file after creating it. (default: True)
```
