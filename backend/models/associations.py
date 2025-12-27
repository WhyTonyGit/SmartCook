from extensions import db
from datetime import datetime

recipe_category = db.Table(
    'recipe_category',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

recipe_ingredient = db.Table(
    'recipe_ingredient',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
)

consumer_ingredient = db.Table(
    'consumer_ingredient',
    db.Column('consumer_id', db.Integer, db.ForeignKey('consumer.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
)

consumer_recipe_fav = db.Table(
    'consumer_recipe_fav',
    db.Column('consumer_id', db.Integer, db.ForeignKey('consumer.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)

consumer_recipe_history = db.Table(
    'consumer_recipe_history',
    db.Column('consumer_id', db.Integer, db.ForeignKey('consumer.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('viewed_at', db.DateTime, default=datetime.utcnow, nullable=False)
)

