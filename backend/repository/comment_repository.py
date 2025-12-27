from extensions import db
from models import Comment
from exception import NotFoundError

class CommentRepository:
    @staticmethod
    def get_by_id(comment_id):
        return Comment.query.get(comment_id)
    
    @staticmethod
    def get_by_recipe(recipe_id):
        return Comment.query.filter_by(recipe_id=recipe_id).order_by(Comment.created_at.desc()).all()
    
    @staticmethod
    def create(text, consumer_id, recipe_id):
        comment = Comment(text=text, consumer_id=consumer_id, recipe_id=recipe_id)
        db.session.add(comment)
        db.session.commit()
        return comment
    
    @staticmethod
    def delete(comment_id):
        comment = CommentRepository.get_by_id(comment_id)
        if not comment:
            raise NotFoundError("Comment not found")
        db.session.delete(comment)
        db.session.commit()

