from flask import Flask, request, jsonify
from case_project.databases.coffe_review_db import CoffeReviewDB
from api_token import Random64Token

app = Flask(__name__)
coffeReviewDB = CoffeReviewDB()

###############################
####  COFFEE RELATED PATHS ####
###############################


@app.route('/coffee', methods=['GET'])
def get_all_coffe():
    # get all the coffe reviews from the database
    # Serialize into JSON-format
    return # JSON file.


@app.route('/coffee/<coffee_id>/info', methods=['GET'])
def get_coffee_info(coffee_id):
    return


@app.route('/coffee/<coffee_id>/reviews', methods=['GET'])
def get_coffee_reviews(coffee_id):
    return


#############################
####  USER RELATED PATHS ####
#############################

@app.route('/users', methods=['GET'])
def get_users():
    """ Returns information about all users registered to coffee review API if authorized """
    try:
        token = request.headers['authentication']
    except KeyError:
        return jsonify({'error': 'Authentication token missing in header.'}), 401

    if coffeReviewDB.is_authorized_user(token):
        return coffeReviewDB.get_all_users_json(), 200
    return jsonify({'error': 'Not a valid authentication token.'}), 401


@app.route('/users/register', methods=['POST'])
def register_user():
    try:
        username = request.args['username']
        email = request.args['email']
    except Exception:
        return jsonify({'error': 'Missing required information.'}), 400

    if not coffeReviewDB.user_exists(username=username):
        token = Random64Token(token_lgth=50).token
        coffeReviewDB.add_new_user(username=username, email=email, token=token)
        return jsonify({'auth_token': token}), 201
    return jsonify({'error': 'Username already exists.'}), 409


@app.route('/users/<profile_id>', methods=['GET'])
def get_profile(profile_id):
    if coffeReviewDB.user_exists(user_id=profile_id):
        return coffeReviewDB.get_user_json(profile_id), 200
    return jsonify({'error': 'User does not exists.'}), 404


@app.route('/users/<profile_id>/reviews', methods=['GET'])
def get_profile_reviews(profile_id):
    return coffeReviewDB.get_user_reviews(profile_id), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)