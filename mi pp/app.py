import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import get_db_connection
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'tu_clave_secreta_aquí'  # Añade una clave secreta para las sesiones

UPLOAD_FOLDER = 'static/profile_pics'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
BLOG_UPLOAD_FOLDER = 'static/blog_images'  # Carpeta para imágenes de blog
os.makedirs(BLOG_UPLOAD_FOLDER, exist_ok=True)
app.config['BLOG_UPLOAD_FOLDER'] = BLOG_UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data)

        image_file = 'default.png'
        if form.profile_image.data and form.profile_image.data.filename:
            file = form.profile_image.data
            # Genera un nombre único para evitar sobrescrituras
            image_file = secure_filename(f"{username}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_file))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password_hash, profile_image, role) VALUES (%s, %s, %s, %s, %s)",
                           (username, email, password, image_file, 'user'))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Registro exitoso. Inicia sesión.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error al registrar: {str(e)}", "danger")
            conn.rollback()
            conn.close()

    return render_template('register.html', form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash("Inicia sesión primero.", "warning")
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT username, email, profile_image FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        profile_image = user['profile_image']  # Mantén la imagen actual por defecto

        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename:
                # Genera un nombre único para la nueva imagen
                profile_image = secure_filename(f"{username}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_image))
                session['profile_image'] = profile_image

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET username=%s, email=%s, profile_image=%s WHERE id=%s",
                           (username, email, profile_image, session['user_id']))
            conn.commit()
            cursor.close()
            conn.close()
            session['username'] = username
            flash("Perfil actualizado correctamente.", "success")
            return redirect(url_for('edit_profile'))
        except Exception as e:
            flash(f"Error al actualizar el perfil: {str(e)}", "danger")
            conn.rollback()
            conn.close()

    return render_template('edit_profile.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['profile_image'] = user['profile_image']
                session['role'] = user['role']
                flash("Inicio de sesión exitoso.", "success")
                return redirect(url_for('courses'))
            else:
                flash("Credenciales incorrectas.", "danger")
        except Exception as e:
            flash(f"Error al iniciar sesión: {str(e)}", "danger")
            conn.close()

    return render_template('login.html', form=form)

@app.route('/courses')
def courses():
    if 'user_id' not in session:
        flash("Inicia sesión primero.", "warning")
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('courses.html', courses=courses)
    except Exception as e:
        flash(f"Error al cargar cursos: {str(e)}", "danger")
        conn.close()
        return redirect(url_for('home'))

@app.route('/admin')
def admin():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash("Acceso denegado.", "danger")
        return redirect(url_for('home'))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin.html', users=users)
    except Exception as e:
        flash(f"Error al cargar usuarios: {str(e)}", "danger")
        conn.close()
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for('home'))

@app.route('/blog')
def blog():
    # Esta ruta puede mostrar las publicaciones del blog
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM blog")
        posts = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('blog.html', posts=posts)
    except Exception as e:
        flash(f"Error al cargar las publicaciones del blog: {str(e)}", "danger")
        return redirect(url_for('home'))

@app.route('/blog/new', methods=['GET', 'POST'])
def new_blog():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash("Acceso denegado.", "danger")
        return redirect(url_for('blog'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_file = None
        
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                image_file = secure_filename(file.filename)
                file.save(os.path.join(app.config['BLOG_UPLOAD_FOLDER'], image_file))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO blog (title, content, image_url) VALUES (%s, %s, %s)",
                       (title, content, image_file))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Publicación agregada con éxito.", "success")
        return redirect(url_for('blog'))
    
    return render_template('new_blog.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash("Acceso denegado.", "danger")
        return redirect(url_for('home'))
    
    username = request.form['username']
    email = request.form['email']
    password = generate_password_hash(request.form['password'])
    role = request.form['role']
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                       (username, email, password, role))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Usuario agregado exitosamente.", "success")
        return redirect(url_for('admin'))
    except Exception as e:
        flash(f"Error al agregar el usuario: {str(e)}", "danger")
        conn.rollback()
        conn.close()
        return redirect(url_for('admin'))


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash("Acceso denegado.", "danger")
        return redirect(url_for('admin'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Usuario eliminado con éxito.", "success")
        return redirect(url_for('admin'))
    except Exception as e:
        flash(f"Error al eliminar el usuario: {str(e)}", "danger")
        conn.rollback()
        conn.close()
        return redirect(url_for('admin'))
    

    
if __name__ == '__main__':
    app.run(debug=True)
