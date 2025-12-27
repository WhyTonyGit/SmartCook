from extensions import db
from datetime import datetime
from sqlalchemy import UniqueConstraint

class Mark(db.Model):
    __tablename__ = 'mark'
    
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)  # 1-5
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('consumer_id', 'recipe_id', name='unique_consumer_recipe_mark'),
    )
    
    consumer = db.relationship('Consumer', back_populates='marks')
    recipe = db.relationship('Recipe', back_populates='marks')
    
    def to_dict(self):
        return {
            'id': self.id,
            'value': self.value,
            'consumer_id': self.consumer_id,
            'recipe_id': self.recipe_id,
            'created_at': self.created_at.isoformat()
        }

