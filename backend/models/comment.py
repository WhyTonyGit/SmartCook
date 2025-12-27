from extensions import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comment'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    consumer = db.relationship('Consumer', back_populates='comments')
    recipe = db.relationship('Recipe', back_populates='comments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'consumer_id': self.consumer_id,
            'consumer_username': self.consumer.username,
            'recipe_id': self.recipe_id,
            'created_at': self.created_at.isoformat()
        }

