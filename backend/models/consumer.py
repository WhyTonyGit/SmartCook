from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    consumers = db.relationship('Consumer', back_populates='role')

class Consumer(db.Model):
    __tablename__ = 'consumer'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), default=2)  # 1=admin, 2=user
    avatar_url = db.Column(db.String(255), nullable=True)
    
    role = db.relationship('Role', back_populates='consumers')
    forbidden_ingredients = db.relationship(
        'Ingredient',
        secondary='consumer_ingredient',
        back_populates='forbidden_for_consumers'
    )
    favorite_recipes = db.relationship(
        'Recipe',
        secondary='consumer_recipe_fav',
        back_populates='favorited_by'
    )
    recipe_history = db.relationship(
        'Recipe',
        secondary='consumer_recipe_history',
        back_populates='viewed_by'
    )
    comments = db.relationship('Comment', back_populates='consumer', cascade='all, delete-orphan')
    marks = db.relationship('Mark', back_populates='consumer', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'role_id': self.role_id,
            'avatar_url': self.avatar_url
        }

