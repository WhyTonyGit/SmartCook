from extensions import db

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    
    recipes = db.relationship(
        'Recipe',
        secondary='recipe_ingredient',
        back_populates='ingredients'
    )
    forbidden_for_consumers = db.relationship(
        'Consumer',
        secondary='consumer_ingredient',
        back_populates='forbidden_ingredients'
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_url': self.image_url
        }

