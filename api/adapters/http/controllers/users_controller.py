from http import HTTPStatus
from flask import Blueprint
import inject

from domain.exceptions.MissingFieldException import MissingFieldException
from domain.exceptions.NotFoundException import NotFoundException

from domain.models.User import User

from domain.services.FollowService import FollowService
from domain.services.UserService import UserService

from ..auth import token_required

@inject.autoparams()
def create_users_blueprint(user_service: UserService, follow_service: FollowService) -> Blueprint:
    users_blueprint = Blueprint('users', __name__)

    @users_blueprint.route('/users', methods=['GET'])
    @token_required
    def get_users(current_user: User):
        users: list[User] = user_service.find_all()
        return [user.to_dict() for user in users], HTTPStatus.OK


    @users_blueprint.route('/users/<username>', methods=['GET'])
    @token_required
    def get_user(current_user: User, username: str):
        user: User = user_service.find_by_username(username)
        return user.to_dict(), HTTPStatus.OK

    return users_blueprint
