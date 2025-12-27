from extensions import db

class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    recipes = db.relationship(
        'Recipe',
        secondary='recipe_category',
        back_populates='categories'
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

