from flask import Flask, render_template, request, redirect, url_for

app = Flask( __name__ )

from sqlalchemy import create_engine
import sqlalchemy.orm
from database_setup import Base, Blog

engine = create_engine( "mysql://admin1:@GitPa$$w0rd#@54.74.234.11/team_404?charset=utf8mb4" )
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin1:@GitPa$$w0rd#@54.74.234.11/team_404'
Base.metadata.bind = engine

DBSession = sqlalchemy.orm.sessionmaker( bind=engine )
session = DBSession()

@app.route( '/' )

@app.route( '/blogs' )
def showBlogs():
    blogs = session.query( Blog ).all()
    return render_template( "blog_post.html", blogs=blogs )


# This will let us Create a new blog post and save it in our database
@app.route( '/blogs/new/', methods=['GET', 'POST'] )
def newBlog():
    if request.method == 'POST':
        newBlog = Blog( title=request.form['name'], author=request.form['author'], post_date=request.form['date'] )
        session.add( newBlog )
        session.commit()
        return redirect( url_for( 'showBlogs' ) )
    else:
        return render_template( 'create_post.html' )


# This will let us Update our blog posts and save it in our database
@app.route( "/blogs/<int:post_id>/edit/", methods=['GET', 'POST'] )
def editBlog(post_id):
    editedBlog = session.query( Blog ).filter_by( id=post_id ).one()
    if request.method == 'POST':
        if request.form['name']:
            editedBlog.title = request.form['name']
            return redirect( url_for( 'showBlogs' ) )
    else:
        return render_template( 'edit_blog.html', blog=editedBlog)


# This will let us Delete our blog post
@app.route( '/blogs/<int:post_id>/delete/', methods=['GET', 'POST'] )
def deleteBlog(post_id):
    BlogToDelete = session.query( Blog ).filter_by( id=post_id ).one()
    if request.method == 'POST':
        session.delete( BlogToDelete )
        session.commit()
        return redirect( url_for( 'showBlogs', post_id=post_id ) )
    else:
        return render_template( 'delete_blog.html', blog=BlogToDelete )


if __name__ == '__main__':
    app.debug = True
    app.run( host='localhost', port=5555)
