from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user# #login_required: Ensures a route is only accessible to logged-in users; current_user: Provides access to the current logged-in user
from .models import Note
from . import db
import json
from .models import SharedPermission
from .utils import send_email

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
        else:
            new_note = Note(title=title,
                description=description,
                tag=tag,
                tag_color=get_random_color(),
                user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')


    # 自己的笔记
    notes = Note.query.filter_by(user_id=current_user.id).all()
    for note in notes:
        note.is_owner = True
        note.can_edit = True
        note.can_delete = True

    # 别人分享给我的
    shared_note_ids = db.session.query(SharedPermission.note_id).filter_by(email=current_user.email).all()
    shared_note_ids = [note_id for (note_id,) in shared_note_ids]
    shared_permissions = SharedPermission.query.filter(SharedPermission.note_id.in_(shared_note_ids), SharedPermission.email == current_user.email).all()
    shared_notes = []
    for perm in shared_permissions:
        note = Note.query.get(perm.note_id)
        if note:
            note.is_owner = False
            note.can_edit = perm.can_edit
            note.can_delete = False  # 无论如何不能删除
            shared_notes.append(note)

    all_notes = notes + shared_notes

    tags = db.session.query(Note.tag).filter_by(user_id=current_user.id).distinct().all()
    tags = [tag[0] for tag in tags]

    return render_template("home.html", user=current_user, notes=all_notes, tags=tags)


@views.route('/edit-note', methods=['POST'])
@login_required
def edit_note():
    note_id = request.form.get('id')# request fotm is for update value, and then update to the retriverd records
    title = request.form.get('title')
    description = request.form.get('description')
    tag = request.form.get('tag')
    note = Note.query.get(note_id) #need note_id to find the newest record in the database
    
    # ✅ 如果没有这个笔记
    if not note:
        flash('Note not found', category='error')
        return redirect(url_for('views.home'))

    # ✅ 检查是否是作者 or 被授权编辑
    is_owner = note.user_id == current_user.id
    has_shared_edit = SharedPermission.query.filter_by(
        note_id=note.id,
        email=current_user.email,
        can_edit=True
    ).first() is not None

    if is_owner or has_shared_edit:
        note.title = title
        note.description = description
        note.tag = tag
        db.session.commit()
        flash('Note updated!', category='success')
    else:
        flash('Note not found or unauthorized', category='error')


    return redirect(url_for('views.home'))

@views.route('/share-note/<int:note_id>', methods=['POST'])
@login_required
def share_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        return "Unauthorized", 403

    email = request.form.get('shared_email')
    permission = request.form.get('permission_level')
    can_edit = (permission == 'edit')

    existing_perm = SharedPermission.query.filter_by(note_id=note.id, email=email).first()
    if existing_perm:
        existing_perm.can_edit = can_edit
    else:
        new_perm = SharedPermission(note_id=note.id, email=email, can_edit=can_edit)
        db.session.add(new_perm)

    db.session.commit()

    # send share email
    send_email(
        to=email,
        subject=f"You've been shared a note: {note.title}",
        body=f"Hi,\n\n{current_user.first_name} shared a note with you.\n\nTitle: {note.title}\n\nYou can now view it in your dashboard."
    )

    flash(f"Shared with {email}!", category='success')
    return redirect(url_for('views.home'))




@views.route('/delete-note', methods=['POST'])
def delete_note():  
    print("received request, headers:", request.headers)
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note: # if note exists
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})#empty json response to tell the html this is completed