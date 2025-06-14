from flask import Blueprint, request, jsonify
from models import db, Travel, TravelParticipant
from datetime import datetime
from flask_login import login_required, current_user

travel_bp = Blueprint('travel', __name__)

@travel_bp.route('/create', methods=['POST'])
@login_required
def create_travel():
    data = request.get_json()
    
    travel = Travel(
        departure=data['departure'],
        destination=data['destination'],
        earliest_departure=datetime.fromisoformat(data['earliest_departure']),
        latest_departure=datetime.fromisoformat(data['latest_departure']),
        max_people=data['max_people'],
        notes=data.get('notes', ''),
        creator_id=current_user.id
    )
    
    db.session.add(travel)
    db.session.commit()
    
    return jsonify({'message': 'Travel created successfully', 'travel_id': travel.id}), 201

@travel_bp.route('/list', methods=['GET'])
def list_travels():
    # 可以添加分页和筛选条件
    travels = Travel.query.filter_by(status='active').order_by(Travel.created_at.desc()).all()
    
    result = []
    for travel in travels:
        result.append({
            'id': travel.id,
            'departure': travel.departure,
            'destination': travel.destination,
            'earliest_departure': travel.earliest_departure.isoformat(),
            'latest_departure': travel.latest_departure.isoformat(),
            'current_people': travel.current_people,
            'max_people': travel.max_people,
            'creator': travel.creator.username,
            'created_at': travel.created_at.isoformat()
        })
    
    return jsonify(result), 200

@travel_bp.route('/<int:travel_id>', methods=['GET'])
def get_travel(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    
    # 增加浏览量
    travel.view_count += 1
    db.session.commit()
    
    return jsonify({
        'id': travel.id,
        'departure': travel.departure,
        'destination': travel.destination,
        'earliest_departure': travel.earliest_departure.isoformat(),
        'latest_departure': travel.latest_departure.isoformat(),
        'current_people': travel.current_people,
        'max_people': travel.max_people,
        'notes': travel.notes,
        'status': travel.status,
        'view_count': travel.view_count,
        'creator': {
            'id': travel.creator.id,
            'username': travel.creator.username,
            'avatar': travel.creator.avatar
        },
        'created_at': travel.created_at.isoformat()
    }), 200

@travel_bp.route('/<int:travel_id>/join', methods=['POST'])
@login_required
def join_travel(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    
    if travel.creator_id == current_user.id:
        return jsonify({'error': 'Cannot join your own travel'}), 400
    
    if travel.current_people >= travel.max_people:
        return jsonify({'error': 'Travel is full'}), 400
    
    # 检查是否已经申请过
    existing = TravelParticipant.query.filter_by(
        travel_id=travel_id,
        user_id=current_user.id
    ).first()
    
    if existing:
        return jsonify({'error': 'You have already applied to join this travel'}), 400
    
    participant = TravelParticipant(
        travel_id=travel_id,
        user_id=current_user.id,
        status='pending'
    )
    
    db.session.add(participant)
    db.session.commit()
    
    return jsonify({'message': 'Join request sent successfully'}), 200

@travel_bp.route('/<int:travel_id>/cancel', methods=['POST'])
@login_required
def cancel_travel(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    
    if travel.creator_id != current_user.id:
        return jsonify({'error': 'Only the creator can cancel the travel'}), 403
    
    travel.status = 'canceled'
    db.session.commit()
    
    return jsonify({'message': 'Travel canceled successfully'}), 200