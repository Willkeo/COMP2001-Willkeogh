from flask import Flask, request, jsonify
from COMP_2001_Trail_Service import db
from sqlalchemy import text

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    try:
        query = text("EXEC CW2_ReadUser")
        result = db.session.execute(query)
        users = [dict(row) for row in result]
        return jsonify(users)
    except Exception as e:
        return jsonify({"message": "Cant fetch users", "error": str(e)}), 500


@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        query = text("EXEC CW2_CreateUser :UserID, :Username, :Email, :Password, :UserRole")
        db.session.execute(query, {
            'UserID': data['UserID'],
            'Username': data['Username'],
            'Email': data['Email'],
            'Password': data['Password'],
            'UserRole': data['UserRole']
        })
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except Exception as e:
        return jsonify({"message": "Cant create user", "error": str(e)}), 500


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        query = text("""
            EXEC CW2_UpdateUser :UserID, :Username, :Email, :Password, :UserRole
        """)
        db.session.execute(query, {
            'UserID': user_id,
            'Username': data['Username'],
            'Email': data['Email'],
            'Password': data['Password'],
            'UserRole': data['UserRole']
        })
        db.session.commit()
        return jsonify({"message": "User updated successfully!"})
    except Exception as e:
        return jsonify({"message": "Cant update user", "error": str(e)}), 500


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        query = text("EXEC CW2_DeleteUser :UserID")
        db.session.execute(query, {'UserID': user_id})
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"})
    except Exception as e:
        return jsonify({"message": "Create delete user", "error": str(e)}), 500


@app.route('/trails', methods=['GET'])
def get_trails():
    try:
        query = text("EXEC CW2_ReadTrail")
        result = db.session.execute(query)
        trails = [dict(row) for row in result]
        return jsonify(trails)
    except Exception as e:
        return jsonify({"message": "Cant fetch trails", "error": str(e)}), 500


@app.route('/trails', methods=['POST'])
def create_trail():
    try:
        data = request.get_json()
        query = text("""
            EXEC CW2_CreateTrail 
            :TrailID, :TrailName, :TrailSummary, :Difficulty, :Location, :Distance
        """)
        db.session.execute(query, {
            'TrailID': data['TrailID'],
            'TrailName': data['TrailName'],
            'TrailSummary': data['TrailSummary'],
            'Difficulty': data['Difficulty'],
            'Location': data['Location'],
            'Distance': data['Distance']
        })
        db.session.commit()
        return jsonify({"message": "Trail created successfully!"}), 201
    except Exception as e:
        return jsonify({"message": "Cant create trail", "error": str(e)}), 500


@app.route('/trails/<trail_id>', methods=['PUT'])
def update_trail(trail_id):
    try:
        data = request.get_json()
        query = text("""
            EXEC CW2_UpdateTrail 
            :TrailID, :TrailName, :TrailSummary, :Difficulty, :Location, :Distance
        """)
        db.session.execute(query, {
            'TrailID': trail_id,
            'TrailName': data['TrailName'],
            'TrailSummary': data['TrailSummary'],
            'Difficulty': data['Difficulty'],
            'Location': data['Location'],
            'Distance': data['Distance']
        })
        db.session.commit()
        return jsonify({"message": "Trail updated successfully!"})
    except Exception as e:
        return jsonify({"message": "Cant update trail", "error": str(e)}), 500


@app.route('/trails/<trail_id>', methods=['DELETE'])
def delete_trail(trail_id):
    try:
        query = text("EXEC CW2_DeleteTrail :TrailID")
        db.session.execute(query, {'TrailID': trail_id})
        db.session.commit()
        return jsonify({"message": "Trail deleted successfully!"})
    except Exception as e:
        return jsonify({"message": "Cant delete trail", "error": str(e)}), 500


@app.route('/features', methods=['GET'])
def get_features():
    try:
        query = text("EXEC CW2_ReadFeature")
        result = db.session.execute(query)
        features = [dict(row) for row in result]
        return jsonify(features)
    except Exception as e:
        return jsonify({"message": "Cant fetch features", "error": str(e)}), 500


@app.route('/features', methods=['POST'])
def create_feature():
    try:
        data = request.get_json()
        query = text("EXEC CW2_CreateFeature :TrailFeatureID, :TrailFeature")
        db.session.execute(query, {
            'TrailFeatureID': data['TrailFeatureID'],
            'TrailFeature': data['TrailFeature']
        })
        db.session.commit()
        return jsonify({"message": "Feature created successfully!"}), 201
    except Exception as e:
        return jsonify({"message": "Cant create feature", "error": str(e)}), 500


@app.route('/trailfeatures', methods=['GET'])
def get_trail_features():
    try:
        query = text("EXEC CW2_ReadTrailFeature")
        result = db.session.execute(query)
        trail_features = [dict(row) for row in result]
        return jsonify(trail_features)
    except Exception as e:
        return jsonify({"message": "Cant fetch trail features", "error": str(e)}), 500


@app.route('/trailfeatures', methods=['POST'])
def add_trail_feature():
    try:
        data = request.get_json()
        query = text("EXEC CW2_CreateTrailFeature :TrailID, :TrailFeatureID")
        db.session.execute(query, {
            'TrailID': data['TrailID'],
            'TrailFeatureID': data['TrailFeatureID']
        })
        db.session.commit()
        return jsonify({"message": "Trail feature added successfully!"}), 201
    except Exception as e:
        return jsonify({"message": "Create add trail feature", "error": str(e)}), 500


@app.route('/trailfeatures/<trail_id>/<feature_id>', methods=['DELETE'])
def delete_trail_feature(trail_id, feature_id):
    try:
        query = text("EXEC CW2_DeleteTrailFeature :TrailID, :TrailFeatureID")
        db.session.execute(query, {
            'TrailID': trail_id,
            'TrailFeatureID': feature_id
        })
        db.session.commit()
        return jsonify({"message": "Trail feature deleted successfully!"})
    except Exception as e:
        return jsonify({"message": "Create delete trail feature", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)