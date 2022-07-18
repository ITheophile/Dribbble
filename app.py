import os
from unicodedata import category
from millify import millify
from faker import Faker
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static\\assets'

# Navigation categories
categories = os.listdir('static/assets')


# For creating fake data
fake = Faker()


# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class DibbbleImage(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String(10), nullable = False)
    category = db.Column(db.String(20), nullable = False)
    likes = db.Column(db.Integer, nullable= False)
    views = db.Column(db.Integer, nullable = False)
    file_path = db.Column(db.String(100), nullable = False)




@app.route('/home')
@app.route('/')
def home():
    data = DibbbleImage.query.all()
    return render_template('index.html', categories = ['All'] + categories,
    data = data)


@app.route('/All')
def all():  
    return redirect(url_for('home'))


@app.route('/Animation')
def animation():
    data = DibbbleImage.query.filter_by(category = 'Animation')
    return render_template('index.html', categories = ['All'] + categories,
    data = data)

@app.route('/Branding')
def branding():
    data = DibbbleImage.query.filter_by(category = 'Branding')
    return render_template('index.html', categories = ['All'] + categories,
    data = data)

@app.route('/Illustration')
def illustration():
    data = DibbbleImage.query.filter_by(category = 'Illustration')
    return render_template('index.html', categories = ['All'] + categories,
    data = data)

@app.route('/Mobile')
def mobile():
    data = DibbbleImage.query.filter_by(category = 'Mobile')
    return render_template('index.html', categories = ['All'] + categories,
    data = data)

@app.route('/Print')
def print():
    data = DibbbleImage.query.filter_by(category = 'Print')
    return render_template('index.html', categories = ['All'] + categories,
    data = data)

@app.route('/Product design')
def product_design():
    data = DibbbleImage.query.filter_by(category = 'Product design')
    return render_template('index.html', categories = ['All'] + categories,
    data = data)

@app.route('/Typography')
def typography():
    data = DibbbleImage.query.filter_by(category = 'Typography')
    return render_template('index.html', categories = ['All'] + categories,
    data = data)

@app.route('/Web design')
def web_design():
    data = DibbbleImage.query.filter_by(category = 'Web design')
    return render_template('index.html', categories = ['All'] + categories,
    data = data)


@app.route('/admin', methods = ['GET', 'POST'])
def add_data():
    if request.method == 'POST':

        #store image's attributes in db
        # author = request.form.get('author')
        # likes = request.form.get('likes')
        # views = request.form.get('views')
        category = request.form.get('category')


        #store images in Folder
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, category, filename)
        file.save(file_path)

        new_file_path = file_path.split('\\')[1:]
        new_file_path = "/".join(new_file_path)

        # if attributes fields disabled
        author = fake.first_name()
        likes = millify(fake.random_int(), 1)
        views = millify(fake.random_int(), 1)

        new_image = DibbbleImage(author = author, category = category,
                                likes = likes, views = views, file_path = new_file_path)
        db.session.add(new_image)
        db.session.commit()

        return f'''<h3>Successfully added new image !!!</h3>
                   <p>{request.form}</p>
                   <p>{new_file_path}</p>
                   '''
    return render_template('admin.html', categories = categories)

@app.route('/admin/delete')
def delete_all():
    db.session.query(DibbbleImage).delete()
    db.session.commit()
    
    return '<h3> Deleted all entries !!!</h3>'


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)










