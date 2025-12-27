from app import app, db
from app.models import Staff, Task, Manager


from flask import render_template
from flask import request, url_for, redirect
from sqlalchemy.exc import IntegrityError

@app.route('/')
def home_page():
    return render_template('home_page.html', title='Task Manager')

@app.route('/do_the_login', methods = ["POST"])
def do_the_login():
    name = request.form['name']
    password = request.form['password']
    if Manager.query.filter_by(staffname=name).first() and Manager.query.filter_by(password=password).first():
        return redirect(url_for('home_page_admin'))
    else:
        return redirect(url_for('home_page_again'))
    
@app.route('/home_page_again')
def home_page_again():
    return render_template('home_page_again.html', title='Task Manager')


@app.route('/home_page_admin')
 
def home_page_admin():
    return render_template(
        'index.html',
        title='Task Manager',
    )

@app.route('/home_page_admin/staffs')
def staffs():
    return render_template('staffs_input.html')

@app.route('/home_page_admin/tasks')
def tasks():
    return render_template('tasks_input.html')

@app.route('/check')
def check():
    staffs = Staff.query.all()
    return render_template('staffs_list.html', staffs=staffs)

@app.route('/table')
def table():
    tasks = Task.query.all()
    contents = []
    for task in tasks:
        contents.append(task.content)
    return render_template('table.html', tasks=tasks, contents=contents)


@app.route('/handle_staffs_form', methods = ["POST"])
def handle_staffs_form():
    name = request.form['name']
    email = request.form['email']
    if Staff.query.filter_by(staffname = name).first():
        return 'This staff is already in the list', 400
    if Staff.query.filter_by(email = email).first():
        return 'This email is used for the another staff', 400
    
    staff = Staff(staffname = name, email = email)

    db.session.add(staff)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return 'This name or this email is already used', 404
    return redirect(url_for('check'))

@app.route('/handle_tasks_form', methods = ["POST"])
def handle_tasks_form():
    id = int(request.form['id'])
    title = request.form['title']
    content = request.form['content']

    task = Task(title=title, content=content, staff_id=id)
    db.session.add(task)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return 'You mising some required data'
    return redirect(url_for('check'))

@app.route('/delete_all_tasks')
def delete_all_tasks():
    Task.query.delete()
    db.session.commit()
    return 'Done'




@app.errorhandler(404)
def page_not_found(error):
    return "This page is not found.", 404
