from flask import Flask, request, jsonify, json
from case_project.databases.coffee_review_db import CoffeeReviewDB
from case_project.databases.coffee_info_json import CoffeInfoJSON
from api_token import Random64Token
from api_return_code_classes import APIClientError

app = Flask(__name__)
coffeeReviewDB = CoffeeReviewDB()
coffeeInfoJSON = CoffeInfoJSON(initiate=False)

###############################
####  COFFEE RELATED PATHS ####
###############################


@app.route('/coffee', methods=['GET', 'POST'])
def get_all_coffee():
    if request.method == 'GET':
        return app.response_class(
            response=json.dumps(coffeeInfoJSON.get_all_coffee()),
            status=200,
            mimetype='application/json'
        )

    if request.method == 'POST':
        # Get the JSON file sent with the post request.
        # Check that the file is in the right format.
        # Add coffee to the JSON-file database.
        return # Entry created with the correct ID.


@app.route('/coffee/search', methods=['GET'])
def search_for():
    try:
        search_word = request.args['search_word']
    except Exception:
        raise APIClientError('Missing required parameters.', 400)

    return app.response_class(
        response=json.dumps(coffeeInfoJSON.get_coffee_search(search_word=search_word)),
        status=200,
        mimetype='application/json'
    )


@app.route('/coffee/<coffee_id>', methods=['GET', 'POST'])
def get_coffee_info(coffee_id):
    """Returns all information about 'coffee_id' stored in database."""
    if not coffeeInfoJSON.coffee_exists(coffee_id=coffee_id):
        raise APIClientError('Coffee id does not exist.', 404)

    if request.method == 'POST':
        token = check_authorization()
        review = check_review_format()
        return app.response_class(
            response=json.dumps(coffeeReviewDB.add_review(coffee_id, token, review)),
            status=201,
            mimetype='application/json'
        )

    if request.method == 'GET':
        # Get information about coffee with id 'coffee_id'
        return app.response_class(
            response=json.dumps(coffeeInfoJSON.get_coffee(coffee_id=coffee_id)),
            status=200,
            mimetype='application/json'
        )

    raise APIClientError('Method not allowed', 405)


def check_review_format() -> dict:
    """
    Checks if the POST:ed review is in the right format,
    raises error otherwise.
    """
    try:
        review = request.get_json()
    except Exception:
        raise APIClientError('Wring format: No valid JSON-object in body.')

    if len(review) != 1:
        raise APIClientError('Wrong format: Too many keys in JSON-object.')

    try:
        review['review']
    except KeyError:
        raise APIClientError('Wrong format: Missing review key')
    return review


@app.route('/coffee/<coffee_id>/reviews', methods=['GET'])
def get_coffee_reviews(coffee_id):
    """Returns all coffee reviews connected to 'coffee_id'"""
    if not coffeeInfoJSON.coffee_exists(coffee_id=coffee_id):
        raise APIClientError('Coffee id does not exist.', 404)
    return app.response_class(
        response=json.dumps(coffeeReviewDB.get_reviews(coffee_id=coffee_id)),
        status=200,
        mimetype='application/json'
    )


@app.route('/coffee/reviews', methods=['GET'])
def get_all_reviews():
    return app.response_class(
        response=json.dumps(coffeeReviewDB.get_reviews()),
        status=200,
        mimetype='application/json'
    )


#############################
####  USER RELATED PATHS ####
#############################


def check_authorization() -> str:
    """ Checks the request authentication, raises error otherwise."""
    try:
        token = request.headers['authentication']
    except KeyError:
        raise APIClientError('Authentication token missing in header.', 401)

    if not coffeeReviewDB.is_authorized_user(token):
        raise APIClientError('Not a valid authentication token.', 401)
    return token


@app.route('/users', methods=['GET'])
def get_users():
    """ Returns information about all users registered to coffee review API if authorized """
    check_authorization()
    return app.response_class(
        response=json.dumps(coffeeReviewDB.get_all_users()),
        status=200,
        mimetype='application/json'
    )


@app.route('/users/register', methods=['POST'])
def register_user():
    try:
        username = request.args['username']
        email = request.args['email']
    except Exception:
        raise APIClientError('Missing required parameters.', 400)

    if not coffeeReviewDB.user_exists(username=username):
        token = Random64Token(token_lgth=50).token
        coffeeReviewDB.add_new_user(username=username, email=email, token=token)
        return jsonify({'auth_token': token}), 201
    raise APIClientError('Username already exists.', 409)


@app.route('/users/<user_id>', methods=['GET'])
def get_profile(user_id):
    """ Responds to URL-request with JSON format user information for id 'profile_id'"""
    if not coffeeReviewDB.user_exists(user_id=user_id):
        raise APIClientError('User does not exists.', 404)

    return app.response_class(
        response=json.dumps(coffeeReviewDB.get_user(user_id)),
        status=200,
        mimetype='application/json'
    )


@app.route('/users/<user_id>/reviews', methods=['GET'])
def get_profile_reviews(user_id):
    return coffeeReviewDB.get_reviews(user_id=user_id), 200


#############################
####  USER RELATED PATHS ####
#############################


@app.route('/coffee/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/coffee/<coffee_id>/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/users/<user_id>/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])
def review_modifier(user_id=None, coffee_id=None, review_id=None):
    if request.method == 'GET':
        pass

    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass

    return jsonify({'message': f'{review_id}: You made it to the right function'}), 200


################################
####  RETURN CODE HANDLERS  ####
################################


@app.errorhandler(APIClientError)
def client_error(e):
    return jsonify(e.to_dict()), e.status_code


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
