import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Actors, db
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response


	# Home route
	@app.route('/')
	def index():
		return jsonify({
			'message': 'Welcome to the casting agency'
		})

	
	# Actor routes
	@app.route('/actors')
	@requires_auth('get:actors')
	def list_actors(jwt):
		try:
			actors = Actors.query.all()
			formatted_actors = [actor.format() for actor in actors]

			return jsonify({
				'success': True,
				'actors': formatted_actors
			}), 200
		except:
			abort(500)

	@app.route('/actors', methods=['POST'])
	@requires_auth("add:actors")
	def add_actor(jwt):
		try:
			get_input = request.get_json()

			name = get_input["name"]
			age = get_input["age"]
			gender = get_input["gender"]

			if name=='' or age=='' or gender=='':
				abort(400)
			else:
				new_actor = Actors(name=name, gender=gender, age=age)
				new_actor.insert()

				return jsonify({
					"success": True,
					"actor": actor.format()
					}), 201
		except:
			abort(422)

	@app.route("/actors/<id>", methods=["PATCH"])
	@requires_auth("edit:actors")
	def update_actor(jwt, id):
		actor = Actors.query.filter(actor.id == id).one_or_none()
		if actor is None:
			abort(404)
		try:
			name = request.get_json()["name"]
			if name == "":
				abort(400)
			else:
				actor.name = name
				actor.update()

				return jsonify({
					"success": True,
					"actor": [actor.format()]
					}), 200
		except:
			abort(422)


	@app.route("/actors/<id>", methods=["DELETE"])
	@requires_auth("delete:actor")
	def delete_actor(jwt, id):
		try:
			actor = Actors.query.filter(actor.id == id).one_or_none()
			if actor is None:
				abort(404)
			else:
				actor.delete()

				return jsonify({
					"success": True,
					"delete": id
					}), 200
		except:
			abort(422)


    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
