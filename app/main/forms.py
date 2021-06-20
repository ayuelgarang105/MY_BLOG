from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import Required, DataRequired


class BlogForm(FlaskForm):
    category = SelectField(
        "Select Category",
        choices=[
            ("product", "Product"),
            ("interview", "Interview"),
            ("promotion", "Promotion"),
        ],
    )
    content = TextAreaField("Your Blog")
    submit = SubmitField("Create Blog")


class CommentForm(FlaskForm):
    comment = TextAreaField("Comment")
    submit = SubmitField("Submit")

class SubscriberForm(FlaskForm):
    email = StringField('Your Email Address')
    name = StringField('Enter your name',validators = [Required()])
    submit = SubmitField('Subscribe')