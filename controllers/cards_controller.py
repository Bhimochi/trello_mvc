from flask import Blueprint, request
from db import db
from datetime import date
from models.card import Card, CardSchema

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

@cards_bp.route('/')
# @jwt_required()
def get_all_cards():
    # if not authorize():
    #     return {'error': 'You must be an admin'}, 401
    # Old Way Legacy
    # select * from cards;
    # cards = Card.query.all() <- Old way 
    # stmt = db.select(Card).where(Card.status == 'To Do')

    stmt = db.select(Card).order_by(Card.priority.desc(), Card.title)
    cards = db.session.scalars(stmt)  # New Way
    return CardSchema(many=True).dump(cards)

@cards_bp.route('/<int:id>/')
def get_one_card(id):
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        return CardSchema().dump(card)
    else:
        return {'error': f'Card not found with id {id}'}, 404

@cards_bp.route('/<int:id>/', methods=['DELETE'])
def delete_one_card(id):
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        db.session.delete(card)
        db.session.commit()
        return {'message': f'Card "{card.title}" deleted successfully'}
    else: 
        return {'error': f'Card not found with id {id}'}, 404
     


@cards_bp.route('/<int:id>/',methods=['PUT', 'PATCH'])
def update_one_card(id):
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        card.title = request.json['title'] or card.title
        card.description = request.json['description'] or card.description
        card.status = request.json['status'] or card.status
        card.priority = request.json['priority'] or card.priority
        db.session.commit()
        return CardSchema().dump(card)
    else:
        return {'error': f'Card not found with id {id}'}, 404


@cards_bp.route('/', methods=['POST'])
def create_card():
        # Create a new Card model instance
        card = Card(
            title = request.json['title'],
            description = request.json['description'],
            date = date.today(),
            status = request.json['status'],
            priority = request.json['priority']
        )
        # Add and commit user to DB
        db.session.add(user)
        db.session.commit()
        # Respond to client
        return CardSchema().dump(card), 201

