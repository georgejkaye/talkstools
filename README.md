# talkstools

Tools for interacting with `talks@bham` (and presumably also `talks@cam` and other derivatives)

## Prerequisites

This project uses [Poetry](https://python-poetry.org/) to manage dependencies.
Poetry uses *virtual environments* (virtualenvs) to isolate dependencies for different projects.
To create a virtualenv for this project and install the dependencies, run the following:

```sh
poetry install
```

## Usage

To run scripts with the right dependenices, run them in the root directory prefixed with `poetry run`.

### Credentials

For some operations you will need to provide credentials.
By default, the scripts will look for a `credentials.json` file where the script is run, but this can be overriden by setting the `TALKSTOOLS_CREDENTIALS` environment variable.

```json
{
    "talks": {
        "user": "george@georgejkaye.com",
        "password": "qwertyuiop"
    }
}

```

### Adding a talk

```sh
poetry run python src/talktools/talks/populate.py -l 1234 -d 1970-01-01 -t 11:00 11:50
```

### Adding talks over a range

```sh
poetry run python src/talktools/talks/populate.py -l 1234 -r 1970-01-01 1970-02-01 -t 11:00 11:50
```
