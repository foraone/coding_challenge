
import requests
import logging
import settings
import json

logger = logging.getLogger('app.api')

class ApiResult(object):
    """
    It's used to format output data
    """
    NOT_FOUND = 'Not Found'
    ERROR = 'error'
    SUCCESS = 'success'
    WARNING = 'warning'

    def __init__(self, result=None, data=None, error_title=None, error_message=None):
        self.result = result
        self.data = data
        self.error_title = error_title
        self.error_message = error_message

    def to_format(self):
        if self.result == ApiResult.ERROR:
            return {
                'data': {
                    'error': {
                        'title': self.error_title,
                        'message': self.error_message
                    }
                },
                'status': 404
            }
        return {
            'data': self.data,
            'status': 200
        }


class BaseAPI(object):
    def __init__(self, **kwargs):
        self.org_name = kwargs.get('org_name')
        self.team_name = kwargs.get('team_name')

    @staticmethod
    def _request(url):
        try:
            response = requests.get(url)
            logger.info(f"Request: {url}")
            if response.status_code == 200:
                return json.loads(response.content)
            logger.error(f'Error: {url}. Code: {response.status_code}')
        except Exception:
            pass

        return {}

class RepoAPI(BaseAPI):
    def _merge_data(self, github_team, github_repos, bitbucket_repos):
        #def _extract_and_merge_data(self, git_user_data, git_repos_data, bitbucket_repos_data):
        output_repo = {}
        list_languages = {}

        # Extract count of public repos and followers from Github
        public_repos_count = github_team.get('public_repos', 0)
        followers_count = github_team.get('followers', 0)
        fork_repos_count = 0

        logger.info(f'Github account {self.team_name} returns:'
                    f'public_repos = {public_repos_count}, followers_count = {followers_count}')

        
        for repo in github_repos:
            repo_data = {}
            for attr in settings.GITHUB_KEYS:

                # Detect if the repo is original or forked
                if attr == 'fork':
                    if repo[attr]:
                        fork_repos_count += 1
                else:
                    repo_data[attr] = repo.get(attr, None)

                    # Count languages
                    if attr == 'language' and repo[attr]:
                        lang = repo[attr].lower()
                        if lang in list_languages:
                            list_languages[lang] += 1
                        else:
                            list_languages[lang] = 1

            output_repo[repo['name']] = repo_data

        # Extract these attributes from each repo of Bitbucket
        if len(bitbucket_repos) > 0:
            for repo in bitbucket_repos:
                repo_data = dict()
                repo_data['watchers_count'] = 0
                if repo['name'] not in output_repo:
                    for attr in settings.BITBUCKET_KEYS:

                        # Detect if the repo is public or private
                        if attr == 'is_private':
                            if not repo[attr]:
                                public_repos_count += 1
                        else:
                            repo_data[attr] = repo.get(attr, None)

                            if attr == 'language' and repo[attr]:
                                lang = repo[attr].lower()
                                if lang in list_languages:
                                    list_languages[lang] += 1
                                else:
                                    list_languages[lang] = 1
                    # get count of watchers
                    try:
                        repo_url = repo['links']['watchers']['href']
                        repo_data['watchers_count'] += self._request(repo_url)['size']
                    except KeyError:
                        pass
                    output_repo[repo['name']] = repo_data

        output_data = {
            'public_repos_count': public_repos_count,
            'followers_count': followers_count,
            'forked_repos_count': fork_repos_count,
            'non_forked_repos_count': public_repos_count - fork_repos_count,
            'list_languages': list_languages,
            'repos': output_repo
        }
        logger.info(f'Merged data of Github and Bitbucket: {output_data}')
        return ApiResult(result=ApiResult.SUCCESS, data=output_data).to_format()
    def getBitbucketInfo(self, org):
        pass
    def get_merged_team(self):
        """
        Lets merge
        """
    
        github_url = f"{settings.GITHUB_BASE_URL}/{settings.GITHUB_SUFFIX['team_url'].format(org_name=self.org_name)}"

        github_team_data = self._request(github_url)

        if not github_team_data:
            # return ApiResult(result=ApiResult.ERROR, error_title=ApiResult.NOT_FOUND,
            #                  error_message='Unable to get the org info from Github').to_format()
            #" ERROR"
            pass
        repos_url = github_team_data.get('repos_url', None)

        git_repos_data = self._request(repos_url)

        # There is a pagination in API. lets do some fix
        bitbucket_repos_url = f"{settings.BITBUCKET_BASE_URL}/{settings.BITBUCKET_SUFFIX['repo_url'].format(team_name=self.team_name)}"
        bitbucket_repos_data = self._request(bitbucket_repos_url).get('values', [])
        
        print(github_team_data, git_repos_data, bitbucket_repos_data)
        return self._merge_data(github_team_data, git_repos_data, bitbucket_repos_data)

    def _paging_request(self):
        