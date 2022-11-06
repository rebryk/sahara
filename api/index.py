import http
import flask
import search
import generate
import requests

from flask import request
from flask_cors import CORS

app = flask.Flask(__name__)
cors = CORS(app)


HEADERS = {
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "x-hasura-api-key": "",
}


@app.route('/search/', methods=["GET"])
def search_request():
    query = request.args.get("query", None)

    if query is None:
        return flask.jsonify({"error": "please, provide query field"}), http.HTTPStatus.BAD_REQUEST

    try:
        response = flask.jsonify(search.search(query))
        response.headers["Cache-Control"] = "s-maxage=86400"
        return response
    except Exception as e:
        return flask.jsonify({"error": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/generate/', methods=["GET"])
def generate_request():
    query = request.args.get("query", None)

    if query is None:
        return flask.jsonify({"error": "please, provide query field"}), http.HTTPStatus.BAD_REQUEST

    try:
        response = flask.jsonify(generate.generate_sql(query))
        response.headers["Cache-Control"] = "s-maxage=86400"
        return response
    except Exception as e:
        return flask.jsonify({"error": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/proxy/', methods=["POST"])
def graphql_proxy():
    try:
        data = request.get_json()
        response = requests.post(
            "https://core-hsr.dune.com/v1/graphql", json=data, headers=HEADERS
        )
        print(response.__dict__)
        return response.json()
    except Exception as e:
        return flask.jsonify({"error": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == "__main__":
    app.run()
