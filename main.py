from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    text = db.Column(db.String(4000))

    def __init__(self, name, text):
        self.name = name
        self.text = text
        
def get_blogs():
    return Blog.query.all()

@app.route('/', methods=['GET'])
def index():
    return render_template('bloglistings.html', blogs=get_blogs(), title="Buil-a-Blog")



def get_blog_by_id():
    return Blog.query.get()

@app.route('/blog', methods=['GET'])
def get_blog_page():


    blog_id = request.args.get("id")
    blog = Blog.query.get(blog_id)
    # for blog in blogs:
    #     print ('blog.name = ' + blog.name)
    return render_template('blog.html', blog=blog, title="Buil-a-Blog")




@app.route('/addblog', methods=['GET'])
def get_add_blog():
    return render_template('addblog.html',title="Add a Blog Entry")


@app.route('/add_blog_entry', methods=['POST'])
def add_blog_entry():
    blog_name = request.form['blog_name']
    blog_text = request.form['blog_text']
    error1 = "Please name your blog."
    error2 = "Please input text into field."

    if ((not blog_name) or (blog_name.strip() == "")) and ((not blog_text) or (blog_text.strip() == "")):

        return render_template("addblog.html", error1=error1, error2=error2)

    elif (not blog_name) or (blog_name.strip() == ""):
        
        return render_template("addblog.html", error1=error1)

    
    elif (not blog_text) or (blog_text.strip() == ""):
        
        return render_template("addblog.html", error2=error2)


    blog = Blog(blog_name, blog_text)
    # text = Blog(blog_text)
    # db.session.add(name, text)
    db.session.add(blog)
    db.session.commit()
    return redirect('/blog?id=' + str(blog.id))


@app.route('/showblog')
def show_blog():
    pass


if __name__ == '__main__':
    app.run()