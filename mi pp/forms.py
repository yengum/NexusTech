from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import EqualTo


class RegisterForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    profile_image = FileField('Imagen de Perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

# Agregado EditUserForm
class EditUserForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=120)])
    role = SelectField('Rol', choices=[('user', 'Usuario'), ('admin', 'Administrador')], validators=[DataRequired()])
    profile_image = FileField('Imagen de Perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Actualizar Usuario')
