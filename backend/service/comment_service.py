from repository import CommentRepository
from exception import NotFoundError, ForbiddenError
from models import Comment

class CommentService:
    @staticmethod
    def get_comments(recipe_id):
        return CommentRepository.get_by_recipe(recipe_id)
    
    @staticmethod
    def create_comment(recipe_id, consumer_id, text):
        if not text or not text.strip():
            raise ValueError("Comment text is required")
        return CommentRepository.create(text, consumer_id, recipe_id)
    
    @staticmethod
    def delete_comment(comment_id, consumer_id, is_admin=False):
        comment = CommentRepository.get_by_id(comment_id)
        if not comment:
            raise NotFoundError("Comment not found")
        
        if comment.consumer_id != consumer_id and not is_admin:
            raise ForbiddenError("You can only delete your own comments")
        
        CommentRepository.delete(comment_id)

