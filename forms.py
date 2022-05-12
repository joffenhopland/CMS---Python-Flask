from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, RadioField, IntegerField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Length, EqualTo, Email, DataRequired


class RegistrerForm(FlaskForm):
    fornavn = StringField(label="First name:", validators=[
                          Length(min=2, max=30), DataRequired()])
    etternavn = StringField(label="Last name:", validators=[
                            Length(min=2, max=30), DataRequired()])
    epost = StringField(label="Email:", validators=[Email(), DataRequired()])
    passord1 = PasswordField(label="Password:", validators=[
                             Length(min=6), DataRequired()])
    passord2 = PasswordField(label="Repeat password:", validators=[EqualTo(
        "passord1", message="Both passwords should be equal."), DataRequired()])
    submit = SubmitField(label="Register account")


class LoginForm(FlaskForm):
    epost = StringField(label="Email", validators=[Email(), DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Log in")


class DokumentForm(FlaskForm):
    tittel = StringField(label="Title", validators=[
                         Length(min=2, max=30), DataRequired()])
    beskrivelse = StringField(label="Description:", validators=[
                              Length(min=2, max=500), DataRequired()])
    tilgang = RadioField(label="Who can have access to this file?", choices=[
                         (0, "Everyone"), (1, "Registered users")], validators=[DataRequired()])
    fil = FileField("File", validators=[FileRequired()])
    tag = StringField(label="Tags")
    katalog = IntegerField(label="Folder")
    submit = SubmitField(label="Save")


class CommentForm(FlaskForm):
    tittel = StringField(label="Title", validators=[
                         Length(min=2, max=30), DataRequired()])
    kommentar = StringField(label="Comment", validators=[
                            Length(min=2, max=200), DataRequired()])
    submit = SubmitField(label="Submit")


class Katalog(FlaskForm):
    tilgang = RadioField(label="Open or restricted?", choices=[
                         (0, "Open"), (1, "Restricted")], validators=[DataRequired()])
    navn = StringField(label="Folder name", validators=[DataRequired()])
    submit = SubmitField(label="Create")


class SearchForm(FlaskForm):
    search = StringField(label="Search", validators=[
                         Length(min=3, max=40), DataRequired()])
    submit = SubmitField(label="Search")
