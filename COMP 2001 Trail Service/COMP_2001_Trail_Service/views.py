from flask import Flask, request, jsonify
from COMP_2001_Trail_Service import db
from COMP_2001_Trail_Service import app
from sqlalchemy import text



@app.route('/users', methods=['GET'])
def get_user_by_id():
    try:
        user_id = request.args.get('UserID')
        if not user_id:
            return jsonify({"message": "UserID is required"}), 400

        query = text("EXEC [CW2].[ReadUser] @UserID = :UserID")
        result = db.session.execute(query, {'UserID': user_id})
        users = [dict(row) for row in result]
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"message": "Cannot fetch user", "error": str(e)}), 500


@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if not all(key in data for key in ['UserID', 'Username', 'Email', 'Password', 'UserRole']):
            return jsonify({"message": "All user fields are required"}), 400

        query = text("""
            EXEC [CW2].[CreateUser] 
            @UserID = :UserID, @Username = :Username, @Email = :Email, @Password = :Password, @UserRole = :UserRole
        """)
        db.session.execute(query, data)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except Exception as e:
        return jsonify({"message": "Cannot create user", "error": str(e)}), 500


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        query = text("""
            EXEC [CW2].[UpdateUser] 
            @UserID = :UserID, @Username = :Username, @Email = :Email, @Password = :Password, @UserRole = :UserRole
        """)
        db.session.execute(query, {
            'UserID': user_id,
            **data
        })
        db.session.commit()
        return jsonify({"message": "User updated successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Cannot update user", "error": str(e)}), 500


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        query = text("EXEC [CW2].[DeleteUser] @UserID = :UserID")
        db.session.execute(query, {'UserID': user_id})
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Cannot delete user", "error": str(e)}), 500

@app.route('/trails', methods=['GET'])
def get_trail_by_id():
    try:
        trail_id = request.args.get('TrailID')
        if not trail_id:
            return jsonify({"message": "TrailID is required"}), 400

        query = text("EXEC [CW2].[ReadTrail] @TrailID = :TrailID")
        result = db.session.execute(query, {'TrailID': trail_id})
        trails = [dict(row) for row in result]
        return jsonify(trails), 200
    except Exception as e:
        return jsonify({"message": "Cannot fetch trail", "error": str(e)}), 500


@app.route('/trails', methods=['POST'])
def create_trail():
    try:
        data = request.get_json()
        if not all(key in data for key in ['TrailID', 'TrailName', 'TrailSummary', 'Difficulty', 'Location', 'Distance']):
            return jsonify({"message": "All trail fields are required"}), 400

        query = text("""
            EXEC [CW2].[CreateTrail] 
            @TrailID = :TrailID, @TrailName = :TrailName, @TrailSummary = :TrailSummary,
            @Difficulty = :Difficulty, @Location = :Location, @Distance = :Distance
        """)
        db.session.execute(query, data)
        db.session.commit()
        return jsonify({"message": "Trail created successfully!"}), 201
    except Exception as e:
        return jsonify({"message": "Cannot create trail", "error": str(e)}), 500


@app.route('/trails/<trail_id>', methods=['PUT'])
def update_trail(trail_id):
    try:
        data = request.get_json()
        query = text("""
            EXEC [CW2].[UpdateTrail] 
            @TrailID = :TrailID, @TrailName = :TrailName, @TrailSummary = :TrailSummary,
            @Difficulty = :Difficulty, @Location = :Location, @Distance = :Distance
        """)
        db.session.execute(query, {
            'TrailID': trail_id,
            **data
        })
        db.session.commit()
        return jsonify({"message": "Trail updated successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Cannot update trail", "error": str(e)}), 500


@app.route('/trails/<trail_id>', methods=['DELETE'])
def delete_trail(trail_id):
    try:
        query = text("EXEC [CW2].[DeleteTrail] @TrailID = :TrailID")
        db.session.execute(query, {'TrailID': trail_id})
        db.session.commit()
        return jsonify({"message": "Trail deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Cannot delete trail", "error": str(e)}), 500


@app.route('/features', methods=['GET'])
def get_feature_by_id():
    try:
        feature_id = request.args.get('TrailFeatureID')
        if not feature_id:
            return jsonify({"message": "TrailFeatureID is required"}), 400

        query = text("EXEC [CW2].[ReadFeature] @TrailFeatureID = :TrailFeatureID")
        result = db.session.execute(query, {'TrailFeatureID': feature_id})
        features = [dict(row) for row in result]
        return jsonify(features), 200
    except Exception as e:
        return jsonify({"message": "Cannot fetch feature", "error": str(e)}), 500


@app.route('/features', methods=['POST'])
def create_feature():
    try:
        data = request.get_json()
        query = text("EXEC [CW2].[CreateFeature] @TrailFeatureID = :TrailFeatureID, @TrailFeature = :TrailFeature")
        db.session.execute(query, data)
        db.session.commit()
        return jsonify({"message": "Feature created successfully!"}), 201
    except Exception as e:
        return jsonify({"message": "Cannot create feature", "error": str(e)}), 500


print("Routes registered in views.py:")
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == '__main__':
    app.run(debug=True)