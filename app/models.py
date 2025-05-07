from datetime import datetime, timezone
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa # type: ignore
import sqlalchemy.orm as so # type: ignore
from flask_login import UserMixin # type: ignore
from hashlib import md5
from app import db, login


def add_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}

class User(UserMixin, db.Model):
    # objects in the 'user' model
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(256))
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author') # initialized as a relationship.
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password) 
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Post(db.Model):
    # objects in the 'post' model
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc) # passed a lambda function that returns the current time in the UTC timezone. 
    )

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts') # initialized as a relationship.

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    
# Now, these two attributes, 'author' and 'posts; allow the application to access the connected user and post entries.

@login.user_loader # decorator
def load_user(id):
    return db.session.get(User, int(id)) # Gets the user information from the database