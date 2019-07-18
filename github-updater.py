import os
import json
import git
from github import Github
import urllib.parse

def main():
    print('Checking Github credentials...')
    if os.path.isfile('credentials.txt'):
        credentials = json.loads(open('credentials.txt', 'r').read())
        username = credentials['username']
        password = credentials['password']
        print('Credentials loaded!')
    else:
        username = input('Insert username: ')
        password = input('Insert password: ')
        if input('Do you want to save your credentials? [y/n] ').lower() == 'y':
            credentials = {'username' : username, 'password' : password}
            credentials_file = open('credentials.txt', 'w')
            credentials_file.write(json.dumps(credentials))
            credentials_file.close()
            print('Credentials saved!')
        else:
            print('Credentials not saved!')
    g = Github(username, password)
    repo_path = os.path.dirname(os.path.realpath(__file__))
    print('Repositories folder: '+repo_path)
    for repo in g.get_user().get_repos():
        print('Checking ['+repo.name+'] repository status...')
        if not os.path.isdir(repo.name):
            print('New repository: cloning')
            git.Git(repo_path).clone('https://'+urllib.parse.quote(username)+':'+urllib.parse.quote(password)+'@github.com/'+urllib.parse.quote(username)+'/'+repo.name)
        else:
            print('Existing repository: pulling')
            repo = git.Repo(os.path.join(repo_path, repo.name))
            o = repo.remotes.origin
            o.pull()

if __name__ == "__main__":
    main()
