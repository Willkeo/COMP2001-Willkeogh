from flask import Flask, request, jsonify
from COMP_2001_Trail_Service import db
from COMP_2001_Trail_Service.models import User, Trail, Feature, TrailFeature, TrailCreationLog

app = Flask(__name__)


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [
        {
            "UserID": user.UserID,
            "Username": user.Username,
            "Email": user.Email,
            "UserRole": user.UserRole
        } for user in users
    ]
    return jsonify(users_list)

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(UserID=user_id).first()
    if user:
        user_data = {
            "UserID": user.UserID,
            "Username": user.Username,
            "Email": user.Email,
            "UserRole": user.UserRole
        }
        return jsonify(user_data)
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        UserID=data['UserID'],
        Username=data['Username'],
        Email=data['Email'],
        Password=data['Password'],
        UserRole=data['UserRole']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.filter_by(UserID=user_id).first()
    if user:
        data = request.get_json()
        user.Username = data['Username']
        user.Email = data['Email']
        user.Password = data['Password']
        user.UserRole = data['UserRole']
        db.session.commit()
        return jsonify({"message": "User updated successfully!"})
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(UserID=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"})
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/trails', methods=['GET'])
def get_trails():
    trails = Trail.query.all()
    trails_list = [
        {
            "TrailID": trail.TrailID,
            "TrailName": trail.TrailName,
            "TrailSummary": trail.TrailSummary,
            "Difficulty": trail.Difficulty
        } for trail in trails
    ]
    return jsonify(trails_list)

@app.route('/trails/<trail_id>', methods=['GET'])
def get_trail(trail_id):
    trail = Trail.query.filter_by(TrailID=trail_id).first()
    if trail:
        trail_data = {
            "TrailID": trail.TrailID,
            "TrailName": trail.TrailName,
            "TrailSummary": trail.TrailSummary,
            "TrailDescription": trail.TrailDescription,
            "Difficulty": trail.Difficulty
        }
        return jsonify(trail_data)
    else:
        return jsonify({"message": "Trail not found"}), 404

@app.route('/trails', methods=['POST'])
def create_trail():
    data = request.get_json()
    new_trail = Trail(
        TrailID=data['TrailID'],
        TrailName=data['TrailName'],
        TrailSummary=data['TrailSummary'],
        Difficulty=data['Difficulty'],
        Location=data['Location'],
        Distance=data['Distance'],
        ElevationGain=data.get('ElevationGain'),
        RouteType=data.get('RouteType'),
        OwnedBy=data.get('OwnedBy'),
        Rating=data.get('Rating'),
        EstimatedTime=data.get('EstimatedTime'),
        Pt1_Lat=data.get('Pt1_Lat'),
        Pt1_Long=data.get('Pt1_Long'),
        Pt1_Desc=data.get('Pt1_Desc'),
        Pt2_Lat=data.get('Pt2_Lat'),
        Pt2_Long=data.get('Pt2_Long'),
        Pt2_Desc=data.get('Pt2_Desc'),
        Pt3_Lat=data.get('Pt3_Lat'),
        Pt3_Long=data.get('Pt3_Long'),
        Pt3_Desc=data.get('Pt3_Desc'),
        Pt4_Lat=data.get('Pt4_Lat'),
        Pt4_Long=data.get('Pt4_Long'),
        Pt4_Desc=data.get('Pt4_Desc'),
        Pt5_Lat=data.get('Pt5_Lat'),
        Pt5_Long=data.get('Pt5_Long'),
        Pt5_Desc=data.get('Pt5_Desc')
    )
    db.session.add(new_trail)
    db.session.commit()
    return jsonify({"message": "Trail created successfully!"}), 201


@app.route('/trails/<trail_id>', methods=['PUT'])
def update_trail(trail_id):
    trail = Trail.query.filter_by(TrailID=trail_id).first()
    if trail:
        data = request.get_json()
        
        trail.TrailName = data['TrailName']
        trail.TrailSummary = data['TrailSummary']
        trail.TrailDescription = data['TrailDescription']
        trail.Difficulty = data['Difficulty']
        trail.Location = data['Location']
        trail.Distance = data['Distance']
        trail.ElevationGain = data.get('ElevationGain', trail.ElevationGain)
        trail.RouteType = data.get('RouteType', trail.RouteType)
        trail.OwnedBy = data.get('OwnedBy', trail.OwnedBy)
        trail.Rating = data.get('Rating', trail.Rating)
        trail.EstimatedTime = data.get('EstimatedTime', trail.EstimatedTime)
        trail.Pt1_Lat = data.get('Pt1_Lat', trail.Pt1_Lat)
        trail.Pt1_Long = data.get('Pt1_Long', trail.Pt1_Long)
        trail.Pt1_Desc = data.get('Pt1_Desc', trail.Pt1_Desc)
        trail.Pt2_Lat = data.get('Pt2_Lat', trail.Pt2_Lat)
        trail.Pt2_Long = data.get('Pt2_Long', trail.Pt2_Long)
        trail.Pt2_Desc = data.get('Pt2_Desc', trail.Pt2_Desc)
        trail.Pt3_Lat = data.get('Pt3_Lat', trail.Pt3_Lat)
        trail.Pt3_Long = data.get('Pt3_Long', trail.Pt3_Long)
        trail.Pt3_Desc = data.get('Pt3_Desc', trail.Pt3_Desc)
        trail.Pt4_Lat = data.get('Pt4_Lat', trail.Pt4_Lat)
        trail.Pt4_Long = data.get('Pt4_Long', trail.Pt4_Long)
        trail.Pt4_Desc = data.get('Pt4_Desc', trail.Pt4_Desc)
        trail.Pt5_Lat = data.get('Pt5_Lat', trail.Pt5_Lat)
        trail.Pt5_Long = data.get('Pt5_Long', trail.Pt5_Long)
        trail.Pt5_Desc = data.get('Pt5_Desc', trail.Pt5_Desc)

        db.session.commit()
        return jsonify({"message": "Trail updated successfully!"})
    else:
        return jsonify({"message": "Trail not found"}), 404

@app.route('/trails/<trail_id>', methods=['DELETE'])
def delete_trail(trail_id):
    trail = Trail.query.filter_by(TrailID=trail_id).first()
    if trail:
        db.session.delete(trail)
        db.session.commit()
        return jsonify({"message": "Trail deleted successfully!"})
    else:
        return jsonify({"message": "Trail not found"}), 404

@app.route('/features', methods=['GET'])
def get_features():
    features = Feature.query.all()
    features_list = [
        {
            "TrailFeatureID": feature.TrailFeatureID,
            "TrailFeature": feature.TrailFeature
        } for feature in features
    ]
    return jsonify(features_list)

@app.route('/features', methods=['POST'])
def create_feature():
    data = request.get_json()
    new_feature = Feature(
        TrailFeature=data['TrailFeature']
    )
    db.session.add(new_feature)
    db.session.commit()
    return jsonify({"message": "Feature created successfully!"}), 201

@app.route('/trailfeatures', methods=['GET'])
def get_trail_features():
    trail_features = TrailFeature.query.all()
    trail_features_list = [
        {
            "TrailID": trail_feature.TrailID,
            "TrailFeatureID": trail_feature.TrailFeatureID
        } for trail_feature in trail_features
    ]
    return jsonify(trail_features_list)

@app.route('/trailfeatures', methods=['POST'])
def add_trail_feature():
    data = request.get_json()
    trail_feature = TrailFeature(
        TrailID=data['TrailID'],
        TrailFeatureID=data['TrailFeatureID']
    )
    db.session.add(trail_feature)
    db.session.commit()
    return jsonify({"message": "Trail feature added successfully!"}), 201

@app.route('/trailfeatures/<trail_id>/<feature_id>', methods=['DELETE'])
def delete_trail_feature(trail_id, feature_id):
    trail_feature = TrailFeature.query.filter_by(TrailID=trail_id, TrailFeatureID=feature_id).first()
    if trail_feature:
        db.session.delete(trail_feature)
        db.session.commit()
        return jsonify({"message": "Trail feature removed successfully!"})
    else:
        return jsonify({"message": "Trail feature not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)