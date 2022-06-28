# github-updater

Keep your Github repositories updated.

## Instructions

Clone the project:

```bash
git clone https://github.com/tassoneroberto/github-updater.git
cd github-updater
```

Install pip libraries:

```bash
python -m pip install -r requirements.txt
```

Create a Github access token with repository permissions. More information here: <https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token>

Run the script and enter the token when required:

```bash
python github_updater.py
```

### Note

This script will use the parent folder containing ```github-updater``` as the repositories path.
