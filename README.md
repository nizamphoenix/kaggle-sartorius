# MK Project Template
A template repo for new MK ML projects.

![skeleton](https://i.giphy.com/media/3o6fJ5z2bgCLBshZUA/giphy.webp)

Usage
-----
To use this template, either follow the documentation in [this confluence page](https://maxkelsen.atlassian.net/wiki/spaces/MAXK/pages/3874095156/Git+Repo+Creation) or hit the green `Use this template` button next to the clone repo button on this page, and continue as normal.

1. Rename the `src` folder to something more project specific (e.g. `edt`/`sst`/`rav`).
    * Ensure you also change this in `pyproject.toml` and `containers/base/Dockerfile` as well!
    * This will affect how you import things in your code - e.g. `from edt.helpers.s3 import download_file`
2. Change the container name in `containers/base`.
3. Delete any `.gitkeep` files in the empty directories once actual files are created in them.
4. Remove any redundant/unwanted sections of this README and replace with project-specific documentation.

Installation
------------
Install poetry as per [the documentation](https://python-poetry.org/docs/#installation).

Poetry can be configured to either create it's own virtual environments, or install packages into a already existing virtual environment (e.g. created with pythons `venv` or conda). To prevent poetry from creating it's own venvs, run `poetry config virtualenvs.create false` - in this case, just running poetry commands while a virtualenv is active will cause it to use that env. If you opt to let poetry handle the virtual environments, you can run `poetry config virtualenvs.in-project true` to create them in the root of your project folder, instead of poetrys default location (something like `/Users/you/Library/Caches/pypoetry`).

The poetry virtual environment can be activated easily with this command: `source $(poetry env info --path)/bin/activate` (or `source (poetry env info --path)/bin/activate.fish` if you are running fish shell). Creating an alias/abbreviation in your terminal for this purpose is quite useful to avoid having to remember/type out the full command every time.

After all this, running `poetry install` should install all dependencies into the configured virtual environment - running with the `--no-dev` flag will withold any specified dev dependencies.

Dependencies
------------
`poetry add numpy` will add `numpy` to `pyproject.toml` and install it into the active virtual environment. Adding a `-D` flag before the package name add it instead as a dev dependency - libraries/packages that might be useful while developing locally/remotely but aren't necessary for the code in production. Linting and formatting libraries are good examples of dev dependencies.

Committing the `poetry.lock` file to the repository will essentially lock the exact versions of everything that is installed - and if another developer clones the repo and runs `poetry install`, poetry will look for the lock file initially to ensure replication across machines.

Precommits
------------
A couple of formatting/linting pre commit hooks are set up already with config files in the root of the repo.

1. After setting up your virtualenv with poetry, run `poetry run pre-commit install` in the repo root
2. Everytime you commit it should run a bunch of linting/formatting tools over the files being committed - if it makes changes you will have to `git add` again once fixed and then `git commit` with the same message that you wanted
3. You can skip specific hooks on specific commits by adding a `SKIP` env variable before your git commit command e.g. to skip the black formatter on a commit run `SKIP="black" git commit -m "message"`
4. You can exclude files from all pre-commits with either their specific file path, or a regex that matches the file name, put at the top of `.pre-commit-config.yaml`
   Multiline example:
   ```
   exclude: >
   (?x)^(
   README.md|
   terraform\/?(?:[^\/]+\/?)*$|
   )$
   ```
5. Specific requirements for Black - be aware that in some repositories this is set to use python3.8 as the interpreter in others this may be python3.7 - if you get an error saying ```no executable python3.7 found``` then you're going to have to either change your ```.pre-commit-config.yaml``` to use an interpreter you DO have by setting ```language_version```. Alternatively... install that version of python that it's set to and Black will find it - no need for it to be your default interpreter.
6. Specific requirements for gitleaks - you will have to install golang and may have to set its modules environment variable on (I did it in my ~/.bashrc):
   Linux:
   ```
   sudo apt install golang
   export GO111MODULE="on"
   ```
   
   MacOS:
   ```
   brew install golang
   ```
   You may also need a python3.7 installed for this to work.

Jupyter Notebook Output Stripping
------------
It's often the case on a project that we don't want to be commiting the output of our jupyter notebook into git. Sometimes it's too big, but more often and more importantly there's a risk of sensitive information being in the output (PII, sensitive customer information, etc.). We could try to remember to clear the output before every commit, but it's easy to forget, and we might not want to clear the output of the working copy.

Instead, we can use `nbstripout` as a git filter to filter the output from notebooks before it gets into git, without changing our working copy.

It's easy to install, just run `poetry run nbstripout --install`


Directory Structure
-------------------
```
├── README.md               <- Top level README file
│
├── data
│   ├── external            <- Data from third party sources (not the client).
│   ├── raw                 <- Original immutable data dump (no code should alter this)
│   ├── interim             <- Intermediate data that has been transformed.
│   └── processed           <- Final processed data used for modelling.
│
├── containers
│   └── base                <- Container with the module & its dependencies
│
├── models                  <- Trained/serialized model files, model predictions and
│                              model summaries
│
├── notebooks               <- All jupyter notebooks. Naming convention is a number
│   │                          (for ordering execution) along with authors name
│   │                          or initials and short '-' delimited description
│   │
│   └── 1.0-mk-initial-notebook-example.ipynb
│
├── src                     <- Source code for use in this project
│   ├── helpers             <- Directory containing helper functions/files for project-wide use
│   ├── data                <- Scripts for downloading/generating data
│   ├── preprocessing       <- Scripts for preprocessing
│   ├── feature_engineering <- Scripts for engineering features
│   └── modelling           <- Scripts for training/evaluating models
│
└── pyproject.toml          <- Project configuration file
```

To Do
----------
- [ ] Possibly implement an automatic documentation generator for the source code folder (sphinx?)
- [ ] Add CI build for docker image.
