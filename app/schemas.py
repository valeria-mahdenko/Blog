from marshmallow import Schema, fields, post_load

from app.models import User, Post, Comment


class CreateUserInputSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        password = data.pop("password")
        user = User(**data)
        user.hash_password(password)
        return user


class UserSchema(Schema):
    class Meta:
        model = User
        load_instance = True
        fields = ('id', 'email', 'username', 'created_at')


class CreatePostInputSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    author_id = fields.Integer(required=True)

    @post_load
    def make_post(self, data, **kwargs):
        return Post(**data)


class PostSchema(Schema):
    class Meta:
        model = Post
        load_instance = True
        fields = ('id', 'title', 'content', 'created_at', 'author')

    author = fields.Nested(UserSchema)


class CreateCommentInputSchema(Schema):
    content = fields.Str(required=True)
    author_id = fields.Integer(required=True)

    @post_load
    def make_comment(self, data, **kwargs):
        return Comment(**data)


class CommentSchema(Schema):
    class Meta:
        model = Comment
        load_instance = True
        fields = ('id', 'content', 'created_at', 'author', 'post')

    author = fields.Nested(UserSchema)
    post = fields.Nested(PostSchema)
