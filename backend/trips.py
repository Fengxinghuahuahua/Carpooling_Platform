from flask import Blueprint, request, jsonify
from models import db, Travel, TravelParticipant, TravelStatus, User
from datetime import datetime, time, timedelta
from flask_login import login_required, current_user
from sqlalchemy import or_

travel_bp = Blueprint('travel', __name__)


@travel_bp.route('/', methods=['POST'])
@login_required
def create_travel():
    data = request.get_json()
    
    required_fields = ['origin', 'destination', 'departureTime', 'seatsTotal']
    if not all(field in data for field in required_fields):
        return jsonify({'code': 400, 'message': 'Missing required fields'}), 400

    try:
        departure_time_obj = datetime.fromisoformat(data['departureTime'])
    except ValueError:
        return jsonify({'code': 400, 'message': 'Invalid departureTime format.'}), 400

    earliest_time = departure_time_obj - timedelta(minutes=30)
    latest_time = departure_time_obj + timedelta(minutes=30)

    travel = Travel(
        departure=data['origin'],
        destination=data['destination'],
        earliest_departure=earliest_time,
        latest_departure=latest_time,
        max_people=data['seatsTotal'],
        notes=data.get('description', ''),
        creator_id=current_user.id
    )
    
    db.session.add(travel)
    db.session.commit()
    
    return jsonify({'code': 201, 'message': 'Travel created successfully', 'data': {'id': travel.id}}), 201


@travel_bp.route('/', methods=['GET'])
def list_travels():
    travels = Travel.query.filter_by(status=TravelStatus.ACTIVE).order_by(Travel.created_at.desc()).all()
    
    result = []
    for travel in travels:
        driver_info = {}
        if travel.creator:
            # --- 关键修改: 将 'creator' 和 'username' 改为前端需要的 'driver' 和 'name' ---
            driver_info = {
                'id': travel.creator.id,
                'name': travel.creator.username, # 改为 name
                'avatar': travel.creator.avatar
            }
        else:
            print(f"\033[93mWARNING: Travel with ID {travel.id} has no creator. Providing fallback.\033[0m")
            driver_info = {
                'id': None,
                'name': '未知用户', # 改为 name
                'avatar': '/static/uploads/Profile_Default.png' 
            }
        
        result.append({
            'id': travel.id,
            'departure': travel.departure,
            'destination': travel.destination,
            'earliest_departure': travel.earliest_departure.isoformat(),
            'latest_departure': travel.latest_departure.isoformat(),
            'current_people': travel.current_people,
            'max_people': travel.max_people,
            'driver': driver_info, # 将 creator 改为 driver
            'created_at': travel.created_at.isoformat()
        })
    
    return jsonify({'code': 200, 'data': result, 'message': 'Success'})


@travel_bp.route('/search', methods=['GET'])
def search_travels():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    earliest_time_str = request.args.get('earliestTime')
    latest_time_str = request.args.get('latestTime')

    query = Travel.query.filter_by(status=TravelStatus.ACTIVE)

    if origin:
        query = query.filter(Travel.departure.ilike(f'%{origin}%'))
    
    if destination:
        query = query.filter(Travel.destination.ilike(f'%{destination}%'))

    if earliest_time_str:
        try:
            earliest_time = datetime.strptime(earliest_time_str, '%Y/%m/%d')
            query = query.filter(Travel.latest_departure >= earliest_time)
        except ValueError:
            return jsonify({'code': 400, 'message': 'Invalid earliestTime format. Use YYYY/MM/DD.'}), 400

    if latest_time_str:
        try:
            latest_time = datetime.strptime(latest_time_str, '%Y/%m/%d')
            latest_time = datetime.combine(latest_time, time.max)
            query = query.filter(Travel.earliest_departure <= latest_time)
        except ValueError:
            return jsonify({'code': 400, 'message': 'Invalid latestTime format. Use YYYY/MM/DD.'}), 400
    
    travels = query.order_by(Travel.created_at.desc()).all()
    
    result = []
    for travel in travels:
        driver_info = {}
        if travel.creator:
            driver_info = {
                'id': travel.creator.id,
                'name': travel.creator.username,
                'avatar': travel.creator.avatar
            }
        else:
            print(f"\033[93mWARNING (Search): Travel with ID {travel.id} has no creator. Providing fallback.\033[0m")
            driver_info = {
                'id': None,
                'name': '未知用户',
                'avatar': '/static/uploads/Profile_Default.png'
            }

        result.append({
            'id': travel.id,
            'departure': travel.departure,
            'destination': travel.destination,
            'earliest_departure': travel.earliest_departure.isoformat(),
            'latest_departure': travel.latest_departure.isoformat(),
            'current_people': travel.current_people,
            'max_people': travel.max_people,
            'driver': driver_info,
            'created_at': travel.created_at.isoformat()
        })
    
    return jsonify({'code': 200, 'data': result})


@travel_bp.route('/<int:travel_id>', methods=['GET'])
def get_travel(travel_id):
    travel = db.session.get(Travel, travel_id)
    if not travel:
        return jsonify({'code': 404, 'message': 'Travel not found'}), 404
    
    travel.view_count += 1
    db.session.commit()
    
    driver_info = {}
    if travel.creator:
        driver_info = {'id': travel.creator.id, 'name': travel.creator.username, 'avatar': travel.creator.avatar}
    else:
        print(f"\033[93mWARNING (Detail): Travel with ID {travel.id} has no creator. Providing fallback.\033[0m")
        driver_info = {'id': None, 'name': '未知用户', 'avatar': '/static/uploads/Profile_Default.png'}

    return jsonify({
        'code': 200,
        'data': {
            'id': travel.id,
            'departure': travel.departure,
            'destination': travel.destination,
            'earliest_departure': travel.earliest_departure.isoformat(),
            'latest_departure': travel.latest_departure.isoformat(),
            'current_people': travel.current_people,
            'max_people': travel.max_people,
            'notes': travel.notes,
            'status': travel.status.value if hasattr(travel.status, 'value') else travel.status,
            'view_count': travel.view_count,
            'driver': driver_info,
            'created_at': travel.created_at.isoformat()
        }
    })

@travel_bp.route('/<int:travel_id>/join', methods=['POST'])
@login_required
def join_travel(travel_id):
    travel = db.session.get(Travel, travel_id)
    if not travel:
        return jsonify({'code': 404, 'message': 'Travel not found'}), 404
    
    if travel.creator_id == current_user.id:
        return jsonify({'code': 400, 'message': 'Cannot join your own travel'}), 400
    
    if travel.current_people >= travel.max_people:
        return jsonify({'code': 400, 'message': 'Travel is full'}), 400
    
    existing = TravelParticipant.query.filter_by(
        travel_id=travel_id,
        user_id=current_user.id
    ).first()
    
    if existing:
        return jsonify({'code': 400, 'message': 'You have already applied to join this travel'}), 400
    
    participant = TravelParticipant(
        travel_id=travel_id,
        user_id=current_user.id,
        status='pending'
    )
    
    db.session.add(participant)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': 'Join request sent successfully'})

@travel_bp.route('/<int:travel_id>/cancel', methods=['POST'])
@login_required
def cancel_travel(travel_id):
    travel = db.session.get(Travel, travel_id)
    if not travel:
        return jsonify({'code': 404, 'message': 'Travel not found'}), 404
    
    if travel.creator_id != current_user.id:
        return jsonify({'code': 403, 'message': 'Only the creator can cancel the travel'}), 403
    
    travel.status = TravelStatus.CANCELED
    db.session.commit()
    
    return jsonify({'code': 200, 'message': 'Travel canceled successfully'})