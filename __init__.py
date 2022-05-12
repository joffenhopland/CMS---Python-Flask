
from flask_login import current_user, login_required, login_user, logout_user, LoginManager, login_manager
from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from forms import CommentForm, Katalog, RegistrerForm, LoginForm, DokumentForm, SearchForm
import uuid
from datetime import datetime
from database import db
from user import User
import secrets
from document import Document
from io import BytesIO
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg',
                      'jpeg', 'gif', 'mp4', 'webm', 'ogg', 'zip'}


app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)
bcrypt = Bcrypt(app)
app.config['MAIL_SERVER'] = 'smtpserver.uit.no'
app.config['MAIL_PORT'] = 587
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# app.config.from_pyfile('config.py')


# Login manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    database = db()
    return User(*database.getUser(user_id))


@app.route('/')
@app.route('/home', methods=["GET", "POST"])
def home_page():
    docId = request.args.get('docId')
    database = db()
    tags = database.tags()
    id = current_user.is_authenticated
    search_form = SearchForm(request.form)
    folder_form = Katalog(request.form)
    folders = database.parentFolder(id)
    documents = database.homepageDoc(id)
    folderId = request.args.get("folderId")
    tagId = request.args.get("tagid")
    createfolder = request.args.get("createfolder")

    if docId:
        return redirect(url_for("show_document", docId=docId))

    elif folderId and not createfolder and not request.method == "POST":
        folder = database.childFolder(folderId, id)
        documents = database.folderDocument(folderId, id)
        return render_template('home.html', tags=tags, form=search_form, folders=folder, documents=documents, parent=folderId)

    elif folderId and not createfolder and not request.method == "POST":
        folder = database.childFolder(folderId, id)
        documents = database.folderDocument(folderId, id)
        return render_template('home.html', tags=tags, form=search_form, folders=folder, documents=documents, parent=folderId)

    elif tagId and not request.method == "POST":
        documents = database.searchDocTag(tagId, id)
        return render_template('home.html', tags=tags, form=search_form, documents=documents)

    elif createfolder and not request.method == "POST":
        if folderId:
            folder = database.childFolder(folderId, id)
            documents = database.folderDocument(folderId, id)
            return render_template('home.html', tags=tags, folder_form=folder_form, folders=folder, documents=documents, parent=folderId)
        else:
            return render_template('home.html', tags=tags, folder_form=folder_form, folders=folders, documents=documents, parent=folderId)

    elif request.method == "POST" and search_form.validate_on_submit():
        search = search_form.search.data.lower()
        documents = database.searchAll(search, id)
        return render_template('home.html', tags=tags, form=search_form, folders=(), documents=documents)

    elif request.method == "POST" and folder_form.validate_on_submit():
        navn = folder_form.navn.data
        tilgang = folder_form.tilgang.data
        database.newFolder(navn, tilgang, folderId)
        folder = database.childFolder(folderId, id)
        documents = database.folderDocument(folderId, id)
        if not folderId:
            folders = database.parentFolder(id)
            documents = database.homepageDoc(id)
            return render_template('home.html', tags=tags, form=search_form, folders=folders, documents=documents)
        else:
            return render_template('home.html', tags=tags, form=search_form, folders=folder, documents=documents, parent=folderId)
    else:
        return render_template('home.html', tags=tags, form=search_form, folders=folders, documents=documents)


@ app.route('/document/<int:docId>', methods=["GET", "POST"])
def show_document(docId):
    if current_user.is_authenticated:
        comment_form = CommentForm(request.form)
        form = DokumentForm()
        database = db()
        views = database.getViews(docId)
        views += 1
        database.updateViews(views, docId)
        database.getViews(docId)
        document = database.getDocument(docId)
        all_comments = database.getComments(docId)
        if request.method == "POST" and comment_form.validate_on_submit():
            comment_title = comment_form.tittel.data
            comment_text = comment_form.kommentar.data
            publisert = datetime.date(datetime.now())
            bruker_id = current_user.id
            dokument_docId = docId
            comment_tuple = (comment_title, publisert,
                             comment_text, dokument_docId, bruker_id)
            database.newComment(comment_tuple)
            flash("Successfully made a comment!", "success")
            return redirect(url_for('show_document', docId=docId))
        else:
            return render_template("document.html", document=document, comment_form=comment_form, all_comments=all_comments, form=form)
    else:
        return redirect(url_for("home_page", docId=docId))


@ app.route('/register', methods=["GET", "POST"])
def register_page():
    form = RegistrerForm(request.form)
    database = db()
    if form.validate_on_submit and database.attemptedUser(form.epost.data):
        flash("Email is already registered. Please use another email address", "danger")
        return render_template('register.html', form=form)
    if form.validate_on_submit() and database.attemptedUser(form.epost.data) == False:
        fornavn = form.fornavn.data
        etternavn = form.etternavn.data
        epost = form.epost.data
        passord = bcrypt.generate_password_hash(form.passord1.data)
        verifisering = str(uuid.uuid4())

        new_user = (fornavn, etternavn, epost, passord, verifisering)
        database.newUser(new_user)
        mail = Mail(app)
        msg = Message("Verify account",
                      sender='kpe144@uit.no', recipients=[epost])
        msg.body = "Welcome as a user to our website. Please verify your account to get access to all services on our website."
        msg.html = f'<b> Confirm email </b> <a href="http://127.0.0.1:5000/verifisert/{verifisering}"> CONFIRM </a>'
        with app.app_context():
            mail.send(msg)
        return render_template('register_landing_page.html')
    return render_template('register.html', form=form)


@ app.route('/register-landing-page', methods=["GET", "POST"])
def register_landing_page():
    render_template('register_landing_page')


@ app.route('/verifisert/<kode>')
def verifiser(kode):
    database = db()
    if database.verifiser(kode) == True:
        get_user = database.getUser2(kode)
        user = User(*get_user)
        login_user(user)
        flash(f"Success! You are verified and logged in!!", "success")
        return redirect(url_for("home_page"))
    else:
        flash(f'Verification failed...', "danger")
        return render_template('home.html')


@ app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    database = db()
    if (
        form.validate_on_submit() and database.checkVerification(form.epost.data) == False
    ):
        flash("You are not verified. Please check your email", "danger")
    elif (
        form.validate_on_submit()
    ):  # Vi må sjekke at brukeren er verifisert også
        epost = form.epost.data
        attempted_user = database.attemptedUser(epost)
        if attempted_user:
            if bcrypt.check_password_hash(
                database.getPasswordHash(epost), form.password.data
            ):
                get_user = database.getUser(attempted_user)
                # lager user object for å få login_user til å funke
                user = User(*get_user)
                login_user(user)
                flash(
                    f"Success! You are logged in as {attempted_user}!", "success")
                return redirect(url_for("home_page"))
            else:
                flash("Email and password does not match! Please try again.", "danger")
                return render_template("login.html", form=form)
        else:
            flash("That user doesn't exist! Try again.")
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)


@ app.route('/logout')
@ login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", "info")
    return redirect(url_for("home_page"))


@ app.route('/new-document', methods=["GET", "POST"])
@ login_required
def new_document_page():
    if current_user.is_authenticated:
        form = DokumentForm()
        database = db()
        folderId = request.args.get("folderId")
        if request.method == "POST":
            if 'fil' not in request.files:
                return redirect(url_for('home_page', _external=True))
            file = form.fil.data
            filnavn = file.filename
            filtype = file.mimetype
            blob = form.fil.data.read()

            if file.filename == '':
                print('no filename')
                return redirect(request.url)
            elif file and allowed_file(file.filename):
                tittel = form.tittel.data
                beskrivelse = form.beskrivelse.data
                tilgang = form.tilgang.data
                publisert = datetime.date(datetime.now())
                bruker_id = current_user.id
                filnavn = secure_filename(filnavn)
                new_document = (tittel, beskrivelse, publisert,
                                tilgang, blob, bruker_id, filnavn, filtype)
                database.newDocument(new_document, folderId)

                getTags = database.allTags()
                tags = [item[0] for item in getTags]
                doc_tags = form.tag.data.lower()
                doc_tags = doc_tags.replace(" ", "").split(",")

                for i in range(len(doc_tags)):
                    if doc_tags[i] not in tags:
                        database.newTag(doc_tags[i])
                        database.setDocTag(doc_tags[i])
                    else:
                        database.setDocTag(doc_tags[i])
                print(folderId)
                flash("Successfully uploaded document!", "success")
                return redirect(url_for('home_page', folderId=folderId))

        return render_template('new_document.html', form=form)
    else:
        return redirect(url_for("home_page"))


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@ app.route('/delete/<int:docId>', methods=["GET", "POST"])
@ login_required
def delete_document_page(docId):
    if current_user.is_authenticated:
        database = db()
        database.deleteDocument(docId)
        folderId = request.args.get("folderId")
        if folderId:
            flash("Successfully deleted document!", "success")
            return redirect(url_for('home_page', folderId=folderId))
        else:
            flash("Successfully deleted document!", "success")
            return redirect(url_for('home_page'))
    else:
        return redirect(url_for("home_page"))


@ app.route('/edit-document/<int:docId>', methods=["GET", "POST"])
@ login_required
def edit_document_page(docId):
    if current_user.is_authenticated:
        database = db()
        get_document = database.getDocument(docId)
        doc_object = Document(*get_document)
        # turn document tuple into an object to pre populate the edit form
        form = DokumentForm(obj=doc_object)
        if request.method == "POST":
            tittel = form.tittel.data
            beskrivelse = form.beskrivelse.data
            tilgang = form.tilgang.data
            docId = doc_object.docId
            # må legge til tags
            database.updateDocument(tittel, beskrivelse, tilgang, docId)
            flash("Successfully edited document!", "success")
            return redirect(url_for('show_document', docId=docId))
        return render_template('edit.html', form=form)
    else:
        return redirect(url_for("home_page"))


@ app.route('/preview/<int:docId>')
def preview_page(docId):
    if current_user.is_authenticated:
        database = db()
        get_document = database.getDocument(docId)
        doc_object = Document(*get_document)
        image_bytes = doc_object.fil
        bytes_io = BytesIO(image_bytes)
        filename = doc_object.dokumentnavn
        return send_file(bytes_io, attachment_filename=filename)
    else:
        return redirect(url_for("home_page"))


@ app.route('/delete-comment/<int:comment_id>', methods=["GET", "POST"])
@ login_required
def delete_comment_page(comment_id):
    if current_user.is_authenticated:
        database = db()
        comment = database.getSpecificComment(comment_id)
        docId = comment[4]
        database.deleteComment(comment_id)
        flash("Successfully deleted comment!", "success")
        return redirect(url_for('show_document', docId=docId))


app.secret_key = secrets.token_urlsafe(16)

if __name__ == "__main__":
    app.run(debug=True)
