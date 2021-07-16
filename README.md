[![DeepSource](https://deepsource.io/gh/StephD/CJ8-blessed-badgers.svg/?label=active+issues&show_trend=true&token=s8xqRUdIFJeB-Cd-zTynrJIw)](https://deepsource.io/gh/StephD/CJ8-blessed-badgers/?ref=repository-badge)
[![CodeFactor](https://www.codefactor.io/repository/github/stephd/cj8-blessed-badgers/badge?s=a5743e65f580e29c6f82336dbcf4703b2b835113)](https://www.codefactor.io/repository/github/stephd/cj8-blessed-badgers)

# Python Discord - Code Jam 8 Summmer 2021
# Team Blessed Badgers

# Story line
Good morning. Do you know where you are? See around you, everything here is square.
Look this door, look this floor, look above your hear and in the corners. What does it mean? Yes you're right, you are inside a box..

I am sorry to let you know that you are stuck here.

Mmhh...

That's no entirely true, you might be able to get away. But can you ?!

# How to play with me?

It need python 3.9 to run

1. `pip install -r dev-requirements.txt`
2. `python run start`


# Team stuff, remove everything below later

## First run of code :

1. pip install -r dev-requirements.txt
2. pre-commit run --all-file

Explaning my mind :

## Todo :
https://www.notion.so/8f9c7260f0d6423684cfaab1f5df09d9?v=acf25f78046f4eff8baa63b54a3e5d0d

Fews sections:
- <b>F</b>ile management
- <b>U</b>ser interactions
- <b>L</b>evel design
- <b>S</b>tory telling + puzzle
- <b>G</b>ame interaction
- <b>D</b>atabase design


# Event information README

## Style line to follow /!\

[Event style guide](https://pythondiscord.com/events/code-jams/code-style-guide/) to get more information about what we consider a maintainable code style.

### flake8: general style rules

Our first and probably most important tool is flake8. It will run a set of plugins on your codebase and warn you about any non-conforming lines.
Here is a sample output:
```
~> flake8
./app.py:1:1: D100 Missing docstring in public module
./app.py:1:6: N802 function name 'helloWorld' should be lowercase
./app.py:1:16: E201 whitespace after '('
./app.py:1:17: ANN001 Missing type annotation for function argument 'name'
./app.py:1:23: ANN201 Missing return type annotation for public function
./app.py:2:1: D400 First line should end with a period
./app.py:2:1: D403 First word of the first line should be properly capitalized
./app.py:3:19: E225 missing whitespace around operator
```

Each line corresponds to an error. The first part is the file path, then the line number, and the column index.
Then comes the error code, a unique identifier of the error, and then a human-readable message.

If, for any reason, you do not wish to comply with this specific error on a specific line, you can add `# noqa: CODE` at the end of the line.
For example:
```python
def helloWorld():  # noqa: N802
    ...
```
will pass linting. Although we do not recommend ignoring errors unless you have a good reason to do so.

It is run by calling `flake8` in the project root.

#### Plugin List:

- `flake8-annotations`: Checks your code for the presence of [type-hints](https://docs.python.org/3/library/typing.html).
- `flake8-bandit`: Checks for common security breaches.
- `flake8-docstring`: Checks that you properly documented your code.
- `flake8-isort`: Makes sure you ran ISort on the project.

### ISort: automatic import sorting

This second tool will sort your imports according to the [PEP8](https://www.python.org/dev/peps/pep-0008/#imports). That's it! One less thing for you to do!

It is run by calling `isort .` in the project root. Notice the dot at the end, it tells ISort to use the current directory.

### Pre-commit: run linting before committing

This third tool doesn't check your code, but rather makes sure that you actually *do* check it.

It makes use of a feature called [Git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) which allow you to run a piece of code before running `git commit`.
The good thing about it is that it will cancel your commit if the lint doesn't pass. You won't have to wait for Github Actions to report and have a second fix commit.

It is *installed* by running `pre-commit install` and can be run manually by calling only `pre-commit`.

[Lint before you push!](https://soundcloud.com/lemonsaurusrex/lint-before-you-push)

#### Hooks List:

- `check-toml`: Lints and corrects your TOML files.
- `check-yaml`: Lints and corrects your YAML files.
- `end-of-file-fixer`: Makes sure you always have an empty line at the end of your file.
- `trailing-whitespaces`: Removes whitespaces at the end of each line.
- `python-check-blanket-noqa`: Forbids you from using noqas on large pieces of code.
- `isort`: Runs ISort.
- `flake8`: Runs flake8.
- `pylint`: Runs pylint
- `black`: Runs black formater

The last two hooks won't ship with their own environment but will rather run shell commands. You will have to modify them if you change your dependency manager.

## If you want to run a virtual environment

### Using the Default Pip Setup

Our default setup includes a bare requirement file to be used with a [virtual environment](https://docs.python.org/3/library/venv.html).

We recommend this if you never have used any other dependency manager, although if you have, feel free to switch to it. More on that below.

#### Creating the environment
Create a virtual environment in the folder `.venv`.
```shell
$ python -m venv .venv
```

#### Enter the environment
It will change based on your operating system and shell.
```shell
# Linux, Bash
$ source .venv/bin/activate
# Linux, Fish
$ source .venv/bin/activate.fish
# Linux, Csh
$ source .venv/bin/activate.csh
# Linux, PowerShell Core
$ .venv/bin/Activate.ps1
# Windows, Bash
$ source .venv/Scripts/activate
# Windows, cmd.exe
> .venv\Scripts\activate.bat
# Windows, PowerShell
> .venv\Scripts\Activate.ps1
```

#### Installing the Dependencies
Once the environment is created and activated, use this command to install the development dependencies.
```shell
$ pip install -r dev-requirements.txt
```

#### Exiting the environment
Interestingly enough, it is the same for every platform
```shell
$ deactivate
```

Once the environment is activated, all the commands listed previously should work. We highly recommend that you run `pre-commit install` as soon as possible.
