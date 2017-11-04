from flask import *
#from data import Articles
from flask_mysqldb import MySQL
from WForms import *
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)
app.secret_key = "flask_development"

#cofig mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dengima'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL_DB
mysql = MySQL(app)


#Articles = Articles()


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def About():
    return render_template('about.html')



@app.route('/articles')
def articles():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()

    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles found'
        return render_template('articles.html', msg=msg)

    cur.close()


@app.route('/article/<string:id>/')
def article(id):

    cur = mysql.connection.cursor()

    result = cur.execute('SELECT * FROM articles WHERE id = %s',[id])

    article = cur.fetchone()

    return render_template('article.html', article=article)


@app.route("/login", methods=['GET','POST'])
def login():
    #if 'email' in session:
    #        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password_candidate = form.password.data
        
        #create cursor
        cur = mysql.connection.cursor()

        #get user by email
        result = cur.execute('SELECT * FROM users WHERE email = %s', [email] )
        if result > 0:
            data = cur.fetchone()
            password = data['password']

            #comapare passwords
            if sha256_crypt.verify(password_candidate, password):
                #passed
                session['logged_in'] = True
                session['email'] = email
                app.logger.info("pwd matched")
                flash('You are now logged in', 'success')
                return redirect(url_for('home'))
            else:
                flash("Wrong Password, Try again", 'danger')
                app.logger.info("pwd not matched")
                #return render_template("login.html", error=error)
                return redirect(url_for('login'))


            cur = close()
        else:
            app.logger.info("no user")
            flash("Email not found, enter correcct email",'danger')
            #return render_template("login.html", error=error)
            return redirect(url_for('login'))      
    return render_template("login.html", form=form)

#User Register
@app.route('/register',methods=['POST','GET'])
def Register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #create cursor
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users(username,email,password) VALUES(%s,%s,%s)',(username,email,password))
        
        #commit to db
        mysql.connection.commit()
        
        #close db
        cur.close()

        flash('You are now registered and can log in','success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route("/logout")
def logout():
    session.clear()
    flash("You are now logged out",'success')
    return redirect(url_for('login'))


#Dashboard
@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles found'
        return render_template('dashboard.html', msg=msg)

    cur.close()

    return render_template('dashboard.html')


def is_loggged_in(f):
    @warps(f)
    def wrap(*args,**kwargs):
        if 'logged-in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized','Please login','danger')
            return redirect(url_for('login'))
    return wrap

#Add article
@app.route('/add_article', methods=['POST','GET'])
def add_article():
    if 'email' not in session:
        return redirect(url_for('login'))
    form = ArticleForm()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO articles(title,body,author) VALUES(%s,%s,%s)',(title,body,session['email']))

        mysql.connection.commit()

        cur.close()
        flash("Article created successfully", 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)    



@app.route('/edit_article/<string:id>', methods=['POST','GET'])
def edit_article(id):
    if 'email' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    
    result = cur.execute("SELECT * FROM articles WHERE id = %s",[id])    

    article = cur.fetchone()

    form = ArticleForm(request.form)
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        cur = mysql.connection.cursor()

        cur.execute("UPDATE articles SET title=%s, body=%s WHERE id=%s", [title,body,id])
        
        mysql.connection.commit()

        cur.close()
        flash("Article Upadted Successfully", 'success')
        return redirect(url_for("dashboard"))
    return render_template('edit_article.html', form=form)  


#Delete Article
@app.route("/delete_article/<string:id>" ,methods=['POST'])
def delete_article(id):
    if 'email' not in session:
        return redirect(url_for('login'))
    else:

        cur = mysql.connection.cursor()
        
        cur.execute("DELETE FROM articles WHERE id=%s",[id])

        mysql.connection.commit()

        cur.close()

        flash("Article Deleted", 'success')

        return redirect(url_for('dashboard'))
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
