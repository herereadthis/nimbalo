from fabric.api import task, local, lcd

REPO_LIST = [
    {
        'bellmaker': {
            'dependencies': ['mossflower']
        }
    }
]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


@task
def update_repos(REPO_LIST=REPO_LIST):
    """
    Helper function to checkout all the repos, and then fetch and reset.
    You will have a fresh copy of master for each repo.
    """
    for repository in REPO_LIST:
        repo = repository.keys()[0]

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
