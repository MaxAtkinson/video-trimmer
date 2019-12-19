import settings
from flask import Flask, jsonify
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
api = Api(app)
engine = create_engine(settings.SQLITE_CONNECTION_STRING)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


@app.teardown_request
def remove_session(ex=None):
    Session.remove()


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'message': 'The requested resource could not be found'
    }), 404


import models  # noqa
import resources  # noqa

resources.configure(api)

if __name__ == '__main__':
    app.run(debug=True)
