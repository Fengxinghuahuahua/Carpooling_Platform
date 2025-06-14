from flask import Blueprint, request, jsonify
from models import db, Comment
from flask_login import login_required, current_user

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/travel/<int:travel_id>', methods=['POST'])
@login_required
def add_comment(travel_id):
    data = request.get_json()
    content = data.get('content')
    
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    
    comment = Comment(
        content=content,
        travel_id=travel_id,
        author_id=current_user.id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'message': 'Comment added successfully',
        'comment_id': comment.id
    }), 201

@comment_bp.route('/travel/<int:travel_id>', methods=['GET'])
def get_comments(travel_id):
    comments = Comment.query.filter_by(travel_id=travel_id).order_by(Comment.created_at.asc()).all()
    
    result = []
    for comment in comments:
        result.append({
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
            'author': {
                'id': comment.author.id,
                'username': comment.author.username,
                'avatar': comment.author.avatar
            }
        })
    
    return jsonify(result), 200