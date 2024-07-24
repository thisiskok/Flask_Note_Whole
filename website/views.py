from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

def get_random_color():
    import random
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
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

    search_query = request.args.get('search')

    if search_query:
        notes = Note.query.filter(Note.user_id == current_user.id).filter(
            (Note.tag.like(f"%{search_query}%")) | (Note.title.like(f"%{search_query}%"))
        ).all()
    else:
        notes = Note.query.filter_by(user_id=current_user.id).all()

    tags = db.session.query(Note.tag).filter_by(user_id=current_user.id).distinct().all()
    tags = [tag[0] for tag in tags]

    return render_template("home.html", user=current_user, notes=notes, tags=tags, search_query=search_query)

@views.route('/edit-note', methods=['POST'])
@login_required
def edit_note():
    note_id = request.form.get('id')
    title = request.form.get('title')
    description = request.form.get('description')
    tag = request.form.get('tag')
    note = Note.query.get(note_id)
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
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
