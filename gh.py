# from github import Github
import requests

def getRepos(url):

    r = requests.get(url)
    return r.json()


# def getRepos(org):
#     g = Github()
#     org = g.get_organization(org)
#     print(org)
#     repos =  org.get_repos()
#     return repos
