from flask import Blueprint, request, jsonify
from app import db
from app.models import ArtistProfile, User
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('profile', __name__)

@bp.route('/profiles/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    profile = ArtistProfile.query.filter_by(user_id=user_id).first_or_404()
    return jsonify({
        'user_id': profile.user_id,
        'bio': profile.bio,
        'portfolio': profile.portfolio
    })

@bp.route('/profiles/<int:user_id>', methods=['POST'])
@jwt_required()
def create_profile(user_id):
    data = request.get_json()
    current_user = get_jwt_identity()
    if current_user != user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    profile = ArtistProfile.query.filter_by(user_id=user_id).first()
    if profile:
        return jsonify({'message': 'Profile already exists'}), 400
    new_profile = ArtistProfile(
        user_id=user_id,
        bio=data.get('bio'),
        portfolio=data.get('portfolio')
    )
    db.session.add(new_profile)
    db.session.commit()
    return jsonify({'message': 'Profile created'}), 201

@bp.route('/profiles/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_profile(user_id):
    data = request.get_json()
    current_user = get_jwt_identity()
    if current_user != user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    profile = ArtistProfile.query.filter_by(user_id=user_id).first_or_404()
    profile.bio = data.get('bio', profile.bio)
    profile.portfolio = data.get('portfolio', profile.portfolio)
    db.session.commit()
    return jsonify({'message': 'Profile updated'})
