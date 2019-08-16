import logging

import flask
from flask import Response, json

from app import api

from bitbucket import readUrl
from gh import getRepos



url = 'https://bitbucket.org/api/2.0/repositories/mailchimp'
url2 = 'https://api.github.com/orgs/mailchimp/repos'

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)

@app.route("/api/v1/org/<org_name>/team/<team_name>", methods=["GET"])
def get_team(team_name, org_name):
    """
    Endpoint for getting merged team profile API
    :param team_name
    """
    team = api.RepoAPI(team_name=team_name, org_name=org_name)
    team_data = team.get_merged_team()
    print("team_data['status']",team_data['status'])
    return Response(json.dumps(team_data['data']), status=team_data['status'], mimetype='application/json')

@app.route("/org", methods=["GET"])
def dirty():
    """
    This is quick and dirty version
    """

    return Response(json.dumps(readUrl(url, [])), status=200, mimetype='application/json')


@app.route("/gh", methods=["GET"])
def dirty2():
    """
    This is quick and dirty version
    """

    data = getRepos(url2)
    filter = ["name", "full_name", "url", "language", "fork"]
    filteredData = []
    for line in data:
        filteredData.append({k: line[k] for k in filter})
    return Response(json.dumps(filteredData), status=200, mimetype='application/json')