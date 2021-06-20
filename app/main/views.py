from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from . import main
from ..models import Blog, User, Comment,Subscriber
from .forms import BlogForm, CommentForm,SubscriberForm
from .. import db
from ..requests import get_quotes

# Views
@main.route("/")
def index():
    """
    View root page function that returns the index page and its data
    """
    title = "Home - Blog"

    quote = get_quotes()
    return render_template("index.html", quote=quote)

@main.route("/blogs")
@main.route("/blogs/<category>")
def blogs(category=None):


    """
    View root page function that returns the index page and its data
    """
    if not category:
        blogs = Blog.query.all()
    else:
        blogs = Blog.query.filter_by(category=category)

    return render_template("blogs.html", category=category, blogs=blogs)



@main.route("/blog/new/", methods=["GET", "POST"])
@login_required
def new_blog():
    """
    Function that creates new blogs
    """
    form = BlogForm()
    if form.validate_on_submit():
        category = form.category.data
        blog = form.content.data

        new_blog  = Blog(content=blog, user=current_user)

        new_blog.save_blog()
        return redirect(url_for("main.blogs"))

    return render_template("new_blog.html", new_blog_form=form)


@main.route("/user/<uname>")
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("Profile/profile.html", user=user)


@main.route("/user/<uname>/update", methods=["GET", "POST"])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for(".profile", uname=user.username))

    return render_template("profile/update.html", form=form)


@main.route("/blog/comments/<int:blog_id>", methods=["GET", "POST"])
@login_required
def view_comments(blog_id):
    """
    Function that return  the comments belonging to a particular blog
    """
    form = CommentForm()
    blog = Blog.query.filter_by(id=blog_id).first()
    comments = Comment.query.filter_by(blog_id=blog.id)
    if form.validate_on_submit():
        new_comment = Comment(comment=form.comment.data, blog=blog, user=current_user)
        new_comment.save_comment()
        return redirect(url_for("main.view_comments", blog_id=blog.id))

    return render_template(
        "comments.html", blog=blog, comments=comments, comment_form=form)

    @main.route('/subscribe', methods=['GET','POST'])
        
    def subscriber():
        quote = get_quotes()
        subscriber_form=SubscriberForm()
        blog = Blog.query.order_by(Blog.date.desc()).all()
        if subscriber_form.validate_on_submit():
            subscriber= Subscriber(email=subscriber_form.email.data,name = subscriber_form.name.data)
            
            db.session.add(subscriber)
            db.session.commit()

            mail_message("Welcome to K-Blogs","email/subscriber",subscriber.email,subscriber=subscriber)
            title= "K-BLOGS"
            return render_template('index.html',title=title, blog=blog, quote=quote)
        subscriber = Blog.query.all()
        blog = Blog.query.all()
        return render_template('subscribe.html',subscriber=subscriber,subscriber_form=subscriber_form,blog=blog)
