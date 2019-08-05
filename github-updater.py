import os
import json
import git
from github import Github
import urllib.parse
import getpass

def main():
    repo_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..'))
    credentials_file = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'config.ini')
    os.chdir(repo_path)
    print('Checking Github credentials...')
    if os.path.isfile(credentials_file):
        credentials = json.loads(open(credentials_file, 'r').read())
        username = credentials['username']
        password = credentials['password']
        print('Credentials loaded!')
    else:
        username = input('Insert username: ')
        password = getpass.getpass('Insert password: ')
        # TODO: check if credentials are correct
        if input('Do you want to save your credentials? [y/n] ').lower() == 'y':
            credentials = {'username': username, 'password': password}
            credentials_file = open(credentials_file, 'w')
            credentials_file.write(json.dumps(credentials))
            credentials_file.close()
            print('Credentials saved!')
        else:
            print('Credentials not saved!')
    g = Github(username, password)

    print('Repositories folder: '+repo_path)
    for repo in g.get_user().get_repos():
        if not os.path.isdir(repo.name):
            print('Cloning ' + repo.name)
            git.Git(repo_path).clone('https://'+urllib.parse.quote(username)+':' +
                                     urllib.parse.quote(password)+'@github.com/'+urllib.parse.quote(username)+'/'+repo.name)
        else:
            print('Pulling ' + repo.name)
            repo = git.Repo(os.path.join(repo_path, repo.name))
            o = repo.remotes.origin
            o.pull()


if __name__ == "__main__":
    main()
