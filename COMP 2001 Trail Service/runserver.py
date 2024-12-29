from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from functools import wraps
import requests
import jwt
import datetime
from COMP_2001_Trail_Service import app, views
from auth import token_required, role_required, SECRET_KEY

AUTH_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

api = Api(
    app,
    version='1.0',
    title='COMP2001 Microservice',
    description='API for managing the microservice, users, trails and features.',
    doc='/swagger',
    security='BearerAuth'
)

api.authorizations = {
    'BearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
    }
}

users_ns = api.namespace('users', description='User operations')
trails_ns = api.namespace('trails', description='Trail operations')
features_ns = api.namespace('features', description='Feature operations')
views_ns = api.namespace('views', description='View operations')
auth_ns = api.namespace('auth', description='Authentication operations')

user_model = api.model('User', {
    'UserID': fields.String(required=True, description='The user ID'),
    'Username': fields.String(required=True, description='The users name'),
    'Email': fields.String(required=True, description='The users email address'),
    'Password': fields.String(required=True, description='The users password'),
    'UserRole': fields.String(required=True, description='The role of the user'),
})

trail_model = api.model('Trail', {
    'TrailID': fields.String(required=True, description='The trails ID'),
    'TrailName': fields.String(required=True, description='The name of the trail'),
    'TrailSummary': fields.String(required=True, description='A summary of the trail'),
    'TrailDescription': fields.String(required=True, description='A description of the trail'),
    'Difficulty': fields.String(required=True, description='The trails difficulty'),
    'Location': fields.String(required=True, description='The location of the trail'),
    'Distance': fields.Float(required=True, description='The distance of the trail in kilometers'),
    'ElevationGain': fields.Float(required=True, description='The elevation gain of the trail in meters'),
    'RouteType': fields.String(required=True, description='The type of route'),
    'OwnedBy': fields.String(required=True, description='The user ID of the trail owner'),
    'Rating': fields.Float(required=True, description='The rating of the trail'),
    'EstimatedTime': fields.String(required=True, description='The estimated time to complete the trail'),
    'Pt1_Desc': fields.String(required=True, description='Description of Point 1'),
    'Pt1_Lat': fields.Float(required=True, description='Latitude of Point 1'),
    'Pt1_Long': fields.Float(required=True, description='Longitude of Point 1'),
    'Pt2_Desc': fields.String(required=True, description='Description of Point 2'),
    'Pt2_Lat': fields.Float(required=True, description='Latitude of Point 2'),
    'Pt2_Long': fields.Float(required=True, description='Longitude of Point 2'),
    'Pt3_Desc': fields.String(required=True, description='Description of Point 3'),
    'Pt3_Lat': fields.Float(required=True, description='Latitude of Point 3'),
    'Pt3_Long': fields.Float(required=True, description='Longitude of Point 3'),
    'Pt4_Desc': fields.String(required=True, description='Description of Point 4'),
    'Pt4_Lat': fields.Float(required=True, description='Latitude of Point 4'),
    'Pt4_Long': fields.Float(required=True, description='Longitude of Point 4'),
    'Pt5_Desc': fields.String(required=True, description='Description of Point 5'),
    'Pt5_Lat': fields.Float(required=True, description='Latitude of Point 5'),
    'Pt5_Long': fields.Float(required=True, description='Longitude of Point 5'),
})

feature_model = api.model('Feature', {
    'TrailFeatureID': fields.String(required=True, description='The feature ID'),
    'TrailFeature': fields.String(required=True, description='The name of the feature'),
})

login_model = api.model('Login', {
    'username': fields.String(required=True, description='The username (email) of the user'),
    'password': fields.String(required=True, description='The password of the user'),
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc('user_login')
    @auth_ns.expect(login_model)
    def post(self):
        """Authenticate user with the Auth API and issue a token"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"message": "Username and password required"}), 400

        response = requests.post(AUTH_API_URL, json={
            "email": username,
            "password": password
        })

        if response.status_code == 200:
            user_data = response.json()
            token = jwt.encode(
                {
                    "user_id": user_data["UserID"],
                    "role": user_data["UserRole"],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                },
                SECRET_KEY,
                algorithm="HS256",
            )
            return jsonify({
                "message": "Login successful",
                "token": token
            }), 200
        else:
            return jsonify({"message": "Invalid credentials"}), response.status_code


@users_ns.route('')
class Users(Resource):
    @users_ns.doc('get_all_users')
    def get(self):
        return views.get_all_users()

    @users_ns.expect(user_model)
    @users_ns.doc('create_user')
    def post(self):
        return views.create_user()


@users_ns.route('/<string:user_id>')
@users_ns.param('user_id', 'The users ID')
class User(Resource):
    @users_ns.doc('get_user_by_id', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def get(self, user_id):
        return views.get_user_by_id(user_id)

    @users_ns.expect(user_model)
    @users_ns.doc('update_user', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def put(self, user_id):
        return views.update_user(user_id)

    @users_ns.doc('delete_user', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def delete(self, user_id):
        return views.delete_user(user_id)


@trails_ns.route('')
class Trails(Resource):
    @trails_ns.doc('get_all_trails')
    def get(self):
        return views.get_all_trails()

    @trails_ns.expect(trail_model)
    @trails_ns.doc('create_trail', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def post(self):
        return views.create_trail()


@trails_ns.route('/<string:trail_id>')
@trails_ns.param('trail_id', 'The trail ID')
class Trail(Resource):
    @trails_ns.doc('get_trail_by_id')
    def get(self, trail_id):
        return views.get_trail_by_id(trail_id)

    @trails_ns.expect(trail_model)
    @trails_ns.doc('update_trail', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def put(self, trail_id):
        return views.update_trail(trail_id)

    @trails_ns.doc('delete_trail', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def delete(self, trail_id):
        return views.delete_trail(trail_id)


@features_ns.route('')
class Features(Resource):
    @features_ns.doc('get_all_features')
    def get(self):
        return views.get_all_features()

    @features_ns.expect(feature_model)
    @features_ns.doc('create_feature', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def post(self):
        return views.create_feature()

@features_ns.route('/<string:feature_id>')
@features_ns.param('feature_id', 'The feature ID')
class Feature(Resource):
    @features_ns.doc('get_feature_by_id')
    def get(self, feature_id):
        return views.get_feature_by_id(feature_id)

    @features_ns.expect(feature_model)
    @features_ns.doc('update_feature', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def put(self, feature_id):
        return views.update_feature(feature_id)

    @features_ns.doc('delete_feature', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def delete(self, feature_id):
        return views.delete_feature(feature_id)

@views_ns.route('')
class Views(Resource):
    @views_ns.doc('get_all_views')
    def get(self):
        return views.get_all_views()

if __name__ == '__main__':
    from os import environ 
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '8000'))
    except ValueError:
        PORT = 8000
    app.run(HOST, PORT)


