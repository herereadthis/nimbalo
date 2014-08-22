from fabric.api import task, local, lcd

REPO_LIST = [
    {
        'bellmaker': {
            'dependencies': ['mossflower']
        }
    }
]


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
                print '\n********\n* {repo} is up-to-date.\n********'.format(
                    repo=repo)
            except:
                print("You don't have this repo: " + repo)
