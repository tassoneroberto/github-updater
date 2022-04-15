from git_remote_progress import GitRemoteProgress
import configparser
import git
import json
import logging
import os
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('GithubUpdater')
config = configparser.ConfigParser()

REPOS_API_URL = 'https://api.github.com/user/repos'


def main():
    repo_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..'))
    config_file_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'config.ini')
    os.chdir(repo_path)
    logger.info('Checking for Github access token...')
    if os.path.isfile(config_file_path):
        try:
            config.read(config_file_path)
        except configparser.MissingSectionHeaderError:
            logger.error(
                f"""Malformed configuration file: {config_file_path}. Please remove the file and run the script again.""")
            return
        token = config['auth']['token']
        logger.info('Token loaded!')
    else:
        token = input('Insert token: ')
        # TODO: check if token is correct
        if input('Do you want to save the access token? [y/n] ').lower() == 'y':
            config['auth'] = {'token': token}
            with open(config_file_path, 'w') as configfile:
                config.write(configfile)
            logger.info('Access token saved!')
        else:
            logger.info('Access token not saved!')

    logger.info('Repositories folder: ' + repo_path)

    headers = {
        'Authorization': f'token {token}',
        'accept': 'application/vnd.github.v3+json'
    }
    params = {
        'per_page': 100,
        'affiliation': 'owner'
    }

    # TODO: Loop over all the pages if repos are more than 100 (limit per page)
    for repo in json.loads(requests.get(REPOS_API_URL, headers=headers, params=params).content):
        repo_name = repo['name']
        if not os.path.isdir(repo_path + "/" + repo_name):
            logger.info('Cloning ' + repo_name)
            try:
                git.Repo.clone_from(
                    repo['clone_url'], repo_path+"/"+repo_name, progress=GitRemoteProgress())
            except git.exc.GitCommandError:
                logger.error(
                    f'Error occurred cloning the repository: {repo_name}'
                )
        else:
            logger.info('Pulling ' + repo_name)
            try:
                repo = git.Repo(os.path.join(repo_path, repo_name))
                o = repo.remotes.origin
                o.pull()
            except git.exc.GitCommandError:
                logger.error(
                    f'Error occurred pulling the repository: {repo_name}'
                )


if __name__ == "__main__":
    main()
