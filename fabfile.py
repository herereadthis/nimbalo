import os
import time
from fabric.api import task, local, lcd

REPO_LIST = [
    {
        'bellmaker': {
            'dependencies': ['mossflower']
        }
    },
    {
        'sunflash': {
            'dependencies': []
        }
    },
    {
        'mossflower': {
            'dependencies': []
        }
    },
    {
        'noonvale': {
            'dependencies': []
        }
    },
    {
        'redwall': {
            'dependencies': []
        }
    }
]


# environment variables
GITHUB_OWNER = os.environ.get('GITHUB_OWNER', None)
GITHUB_ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN', None)
TRAVIS_TOKEN = os.environ.get('TRAVIS_TOKEN', None)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def env_github_owner():
    if not GITHUB_OWNER:
        except_statement = "No GITHUB_OWNER in environment variables!"
        raise Exception(except_statement)


def env_github_access_token():
    if not GITHUB_ACCESS_TOKEN:
        except_statement = "No GITHUB_ACCESS_TOKEN in environment variables!"
        raise Exception(except_statement)


def env_travis_token():
    if not TRAVIS_TOKEN:
        except_statement = "No TRAVIS_TOKEN in environment variables!"
        raise Exception(except_statement)


@task
def verify(var=5):
    """
    Verify Task - Prints your integer arg or 5 if undefined.
    """
    print bcolors.OKBLUE + "\nvar = {var}".format(var=var) + bcolors.ENDC


def grab_repo(repo):
    with lcd("../"):
        clone_this = "https://github.com/herereadthis/{repo}.git".format(
            repo=repo)
        git_clone_this = "git clone {clone_this}".format(
            clone_this=clone_this)

        print bcolors.OKGREEN + "\n\n\n********\n********"
        print "Cloning {repo} repo...\n********\n********".format(repo=repo)
        print "\n\n" + bcolors.ENDC
        time.sleep(1)
        local(git_clone_this)
        with lcd(repo):
            local("npm install")
            local("./node_modules/bower/bin/bower install")
            local("git submodule init")
            local("git submodule update")
            print bcolors.OKGREEN + "\n\n\n********\n********"
            print "Installed {repo}!\n********\n********".format(repo=repo)
            print "\n\n\n\n" + bcolors.ENDC
            time.sleep(1)


def grunt_build(repo):
    with lcd("../"):
        print bcolors.OKGREEN + "\n\n\n********\n********"
        print "Running Grunt for {repo}. This may fail on grunt test.".format(
            repo=repo)
        print "********\n********\n\n\n\n" + bcolors.ENDC
        with lcd(repo):
            local("./node_modules/grunt-cli/bin/grunt")
    time.sleep(1)


@task
def clone_repo(repo_list=REPO_LIST):
    """
    No args: gets all frontend repos. Specify a particular repo with arg.
    """
    if repo_list == REPO_LIST:
        for repository in repo_list:
            repo = repository.keys()[0]
            grab_repo(repo)
        for repository in repo_list:
            repo = repository.keys()[0]
            grunt_build(repo)
    else:
        repo = repo_list
        grab_repo(repo)
        grunt_build(repo)


@task
def update_repos(REPO_LIST=REPO_LIST):
    """
    Helper function to checkout all the repos, and then fetch and reset.
    You will have a fresh copy of master for each repo.
    """
    for i, repository in enumerate(REPO_LIST):
        repo = repository.keys()[0]
        print repo

        with lcd("../%s" % repo):
            try:
                local("git fetch origin")
                local("git checkout master")
                local("git reset --hard origin/master")
                local("git submodule update")
                print '\n********'
                print '* ' + bcolors.OKGREEN + '{repo} is up-to-date.'.format(
                    repo=repo)
                print bcolors.ENDC + '********'
            except:
                print(bcolors.FAIL + "You don't have this repo: " + repo)
