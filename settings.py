
GITHUB_BASE_URL = 'https://api.github.com'
BITBUCKET_BASE_URL = 'https://api.bitbucket.org/2.0'

GITHUB_SUFFIX = {
    'user_url': 'users/{user_name}',
    'repo_url': 'users/{user_name}/repos',
    'team_url': 'orgs/{org_name}'
}

BITBUCKET_SUFFIX = {
    'user_url': 'users/{user_name}',
    'team_url': 'teams/{team_name}',
    'repo_url': 'repositories/{team_name}'
}

GITHUB_KEYS = ['fork', 'forks_count', 'watchers_count', 'language', 'description']

BITBUCKET_KEYS = ['is_private', 'language', 'description']