from datetime import datetime, timezone
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # type: ignore
from hashlib import md5
from app import app, db, login
from time import time
import sqlalchemy as sa # type: ignore
import sqlalchemy.orm as so # type: ignore
import jwt # type: ignore


def add_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}

class User(UserMixin, db.Model):
    # objects in the 'user' model
    followers = sa.Table(
    'followers',
    db.metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
    )
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(256))
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author') # initialized as a relationship.
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    following: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers',
    )

    followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following',
    )
    def set_password(self, password):
        self.password_hash = generate_password_hash(password) 
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    # Follower functions
    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)
    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
    def is_following(self, user):
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None
    def followers_count(self):
        query = sa.select(sa.func.count()).select_from(self.followers.select().subquery())
        return db.session.scalar(query)
    def following_count(self):
        query = sa.select(sa.func.count()).select_from(self.following.select().subquery())
        return db.session.scalar(query)
    def following_posts(self):
        Author = so.aliased(User)
        Follower = so.aliased(User)
        return (
            sa.select(Post)
            .join(Post.author.of_type(Author)) # Joins the table of the post and the author
            .join(Author.followers.of_type(Follower), isouter=True) # Joins the table again with the current table and author followers. oouter_join ensures that own user posts also appear.
            .where(sa.or_(
                Follower.id == self.id,
                Author.id == self.id,
            )) # filter out only who we are interested in
            .group_by(Post) # Remove duplicate posts
            .order_by(Post.timestamp.desc()) # sort by date
        )
    # Verify password reset signature
    def get_reset_password_token(self, expires_in=300):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256'
        )
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, id)
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