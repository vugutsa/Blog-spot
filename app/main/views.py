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

@main.route('/blog/comment/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentForm()
    blog= get_blog(id)
    if form.validate_on_submit():
        title = form.title.data
        comment = form.comment.data

        # Updated comment instance
        new_comment = Comment(blog_id=blog.id,blog_title=title,image_path=blog.poster,blog_comment=comment,user=current_user)

        # save comment method
        new_comment.save_comment()
        return redirect(url_for('.blog',id = blog.id ))

    title = f'{blog.title} comment'
    return render_template('new_comment.html',title = title, comment_form=form, blog=blog)

@main.route('/categories/<cate>')
def category(cate):
    '''
    function to return the blog by category
    '''
    category = blog.get_blog(cate)
    
    
    # print(category)
    title = f'{cate}'
    return render_template('categories.html',title = title, category = category)

@main.route('/blog/', methods = ['GET','POST'])
@login_required
def new_blog():

    form = blogForm()

    if form.validate_on_submit():
        category = form.category.data
        blog= form.blog.data
        title=form.title.data

        # Updated bloginstance
        new_blog = blog(title=title,category= category,blog= blog,user_id=current_user.id)

        title='Write a new blog'

        new_blog.save_blog()

        return redirect(url_for('main.index'))

    return render_template('blog.html',form= form)



@main.route('/comment/<int:id>')
def single_comment(id):
    comment=Comment.query.get(id)
    if comment is None:
        abort(404)
    format_comment = markdown2.markdown(comment.blog_comment,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('comment.html',comment = comment,format_comment=format_comment)
