from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('follow', __name__)

@bp.route('/follow/<int:artist_id>', methods=['POST'])
@jwt_required()
def follow_artist(artist_id):
    current_user_id = get_jwt_identity()
    artist = User.query.get_or_404(artist_id)
    if artist.is_artist and artist_id != current_user_id:
        # Logic to handle following an artist
        return jsonify({'message': 'Followed artist'}), 200
    return jsonify({'message': 'Invalid artist or self-following'}), 400

@bp.route('/following', methods=['GET'])
@jwt_required()
def get_following():
    current_user_id = get_jwt_identity()
    # Fetch the list of artists followed by the current user
    return jsonify({'following': []})  # Implement fetching logic
