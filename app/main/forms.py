from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')
    
class CommentForm(FlaskForm):
    
    title = StringField('Comment title',validators=[Required()])

    comment = TextAreaField('blog comment')

    submit = SubmitField('Submit')
 
class BlogForm(FlaskForm):
    title = StringField('Blog Title')
    description = TextAreaField('Blog')
    submit = SubmitField('Submit')
    
    
 
