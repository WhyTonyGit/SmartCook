from extensions import db
from sqlalchemy import Enum
import enum

class Difficulty(enum.Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'

class Recipe(db.Model):
    __tablename__ = 'recipe'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cooking_time = db.Column(db.Integer, nullable=False)  # в минутах
    difficulty = db.Column(db.Enum(Difficulty), nullable=False, default=Difficulty.MEDIUM)
    image_url = db.Column(db.String(255), nullable=True)
    
    categories = db.relationship(
        'Category',
        secondary='recipe_category',
        back_populates='recipes'
    )
    ingredients = db.relationship(
        'Ingredient',
        secondary='recipe_ingredient',
        back_populates='recipes'
    )
    favorited_by = db.relationship(
        'Consumer',
        secondary='consumer_recipe_fav',
        back_populates='favorite_recipes'
    )
    viewed_by = db.relationship(
        'Consumer',
        secondary='consumer_recipe_history',
        back_populates='recipe_history'
    )
    comments = db.relationship('Comment', back_populates='recipe', cascade='all, delete-orphan')
    marks = db.relationship('Mark', back_populates='recipe', cascade='all, delete-orphan')
    learning = db.relationship('Learning', back_populates='recipe', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self, include_details=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'cooking_time': self.cooking_time,
            'difficulty': self.difficulty.value if isinstance(self.difficulty, Difficulty) else self.difficulty,
            'image_url': self.image_url
        }
        
        if include_details:
            data['categories'] = [c.to_dict() for c in self.categories]
            data['ingredients'] = [i.to_dict() for i in self.ingredients]
            data['comments_count'] = len(self.comments)
            if self.marks:
                data['avg_rating'] = sum(m.value for m in self.marks) / len(self.marks)
            else:
                data['avg_rating'] = 0.0
            if self.learning:
                data['steps'] = [s.to_dict() for s in sorted(self.learning.steps, key=lambda x: x.number)]
        
        return data

