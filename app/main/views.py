from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import *
from .. import db,photos
from flask_login import login_required,current_user
import markdown2 
from ..request import get_quote
from ..models import *


@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Blog post',
    quote = get_quote()
    return render_template('index.html', title = title,quote = quote)

@main.route('/user/<uname>')
def profile(uname):
    
    quote = get_quote()
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, quote=quote)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    
    quote = get_quote()
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form, quote=quote)



@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    
    quote = get_quote()
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/writer/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic_writer(uname):
    
    quote = get_quote()
    writer = Writer.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        writer.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/comments/<id>')
@login_required
def comment(id):
    '''
    function to return the comments
    '''
    quote = get_quote()
    comm =Comments.get_comment(id)
    title = 'comments'
    return render_template('comments.html',comments = comm,title = title,quote=quote)


@main.route('/idea/new_idea', methods = ['GET','POST'])
@login_required
def new_idea():
    quote = get_quote()

    form = BlogForm()

    if form.validate_on_submit():
        idea= form.description.data
        title=form.title.data

        # Updated idea instance
        new_idea = Idea(title=title,description= idea,user_id=current_user.id)

        title='New idea'

        new_idea.save_idea()

        return redirect(url_for('main.new_idea'))

    return render_template('idea.html',form= form, quote=quote)

@main.route('/idea/all', methods=['GET', 'POST'])
@login_required
def all():
    ideas = Idea.query.all()
    quote = get_quote()
    
    return render_template('ideas.html', ideas=ideas, quote=quote)



@main.route('/new_comment/<int:idea_id>', methods = ['GET','POST'])
@login_required
def new_comment(idea_id):
    quote = get_quote()
    opinion = Idea.query.filter_by(id = idea_id).first()
    form = CommentForm()

    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comments(comment=comment,user_id=current_user.id, idea_id=idea_id)

        new_comment.save_comment()

        return redirect(url_for('main.index'))
    title='New comment'
    return render_template('new_comment.html',title=title,comment_form = form,idea_id=idea_id,quote=quote)
