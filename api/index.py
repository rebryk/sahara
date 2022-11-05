import flask
import search
import http

from flask import request


app = flask.Flask(__name__)


@app.route('/search/', methods=["GET"])
def query():
    query = request.args.get("query", None)

    if query is None:
        return flask.jsonify({"error": "please, provide query field"}), http.HTTPStatus.BAD_REQUEST

    try:
        return flask.jsonify(search.search(query))
    except Exception as e:
        return flask.jsonify({"error": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR
