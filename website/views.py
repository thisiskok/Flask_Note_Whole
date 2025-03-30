from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user# #login_required: Ensures a route is only accessible to logged-in users; current_user: Provides access to the current logged-in user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)##new blueprint allow u to organize routes separately from the main app

def get_random_color():
    import random
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


@views.route('/', methods=['GET', 'POST'])#defines a route for the home page that accepts both GET and POST requests
@login_required
def home():
    #Retrieves below from the form data, submit the form
    if request.method == 'POST': 
        title = request.form.get('title')
        description = request.form.get('description')
        tag = request.form.get('tag')
        #note = request.form.get('note')#Gets the note from the HTML 

        if not title or not description:
            flash('Title and description are required!', category='error')
        #if len(note) < 1:
            #flash('Note is too short!', category='error') 
        else:
            new_note = Note(title=title,
                description=description,
                tag=tag,
                tag_color=get_random_color(),
                user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')


     # Retrieve all notes for the current user
    notes = Note.query.filter_by(user_id=current_user.id).all() #Note is a SQLAlchemy model represents the notes table in the database，all matches record

    # Retrieve distinct tags for the current user
    tags = db.session.query(Note.tag).filter_by(user_id=current_user.id).distinct().all() #filter_by =filter(Note.user_id == current_user.id).
    tags = [tag[0] for tag in tags] #tag[0] extracts the first (and only) element of each tuple

    return render_template("home.html", user=current_user, notes=notes, tags=tags)

@views.route('/edit-note', methods=['POST'])
@login_required
def edit_note():
    note_id = request.form.get('id')# request fotm is for update value, and then update to the retriverd records
    title = request.form.get('title')
    description = request.form.get('description')
    tag = request.form.get('tag')
    note = Note.query.get(note_id) #need note_id to find the newest record in the database
    if note and note.user_id == current_user.id:
        note.title = title
        note.description = description
        note.tag = tag
        db.session.commit()
        flash('Note updated!', category='success')
    else:
        flash('Note not found or unauthorized', category='error')
    return redirect(url_for('views.home'))


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note: # if note exists
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})#empty json response to tell the html this is completed
