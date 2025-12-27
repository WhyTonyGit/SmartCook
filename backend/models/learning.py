from extensions import db

class Learning(db.Model):
    __tablename__ = 'learning'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), unique=True, nullable=False)
    
    recipe = db.relationship('Recipe', back_populates='learning')
    steps = db.relationship('StepLearning', back_populates='learning', cascade='all, delete-orphan', order_by='StepLearning.number')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe_id': self.recipe_id,
            'steps': [s.to_dict() for s in sorted(self.steps, key=lambda x: x.number)]
        }

class StepLearning(db.Model):
    __tablename__ = 'step_learning'
    
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    learning_id = db.Column(db.Integer, db.ForeignKey('learning.id'), nullable=False)
    
    learning = db.relationship('Learning', back_populates='steps')
    
    def to_dict(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'title': self.title,
            'description': self.description,
            'number': self.number,
            'learning_id': self.learning_id
        }

