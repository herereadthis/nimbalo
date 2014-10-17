import os
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
