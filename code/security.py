from user import User
from werkzeug.security import safe_str_cmp

"""
username_mapping and user_id_mapping are sued to store different user info
function authenticate and identity use username_mapping and user_id_mapping to locate specific user
"""

"""
users = [
    User(1, 'bob', 'asdf')
]

username_mapping = {
    u.username: u for u in users
}

user_id_mapping = {
    u.id: u for u in users
}
"""

def authenticate(username, password):
    user = User.find_by_username(username)
    if safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
