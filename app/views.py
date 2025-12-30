from app import app, db
from app.models import Staff, Task, Manager


from flask import render_template
from flask import request, url_for, redirect, flash
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

@app.route('/home_page_admin/delete_staffs')
def delete_staffs():
    staffs = Staff.query.all()
    return render_template('staffs_list_for_delete.html', staffs = staffs)

@app.route('/home_page_admin/delete_staffs/<int:staff_id>')
def delete_staffs_by_id(staff_id):
    staff = Staff.query.get_or_404(staff_id)
    db.session.delete(staff)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash('The staff you trying to remove has some unfinished tasks, go check!!!')
        return redirect('/home_page_admin')
    return redirect(url_for('delete_staffs'))

@app.route('/home_page_admin/update_staffs')
def update_staffs():
    staffs = Staff.query.all()
    return render_template('staffs_list_for_update.html', staffs = staffs)

@app.route('/home_page_admin/update_staffs/<int:staff_id>')
def update_staffs_by_id(staff_id):
    staff = Staff.query.get_or_404(staff_id)
    return render_template('staffs_update.html', staff_id=staff_id, staff=staff)

@app.route('/home_page_admin/update_staffs/<int:staff_id>/handle_update_staffs', methods = ["POST"])
def handle_update_staffs(staff_id):
    name = request.form['staffname']
    email = request.form['email']
    staff = Staff.query.get_or_404(staff_id)
    if name:
        staff.staffname = name
        db.session.commit()
        return 'Updated successfully'
    elif email:
        staff.email = email
        db.session.commit()
        return 'Updated successfully'
    elif name and email:
        staff.staffname = name
        staff.email = email
        db.session.commit()
        return 'Updated successfully'
    else:
        return 'Nothing is changed!'


@app.route('/home_page_admin/staffs')
def staffs():
    return render_template('staffs_input.html')

@app.route('/home_page_admin/tasks')
def tasks():
    staffs = Staff.query.all()
    return render_template('staffs_list_for_update_task.html', staffs = staffs)

@app.route('/home_page_admin/tasks/<int:staff_id>')
def update_tasks(staff_id):
    staff = Staff.query.get_or_404(staff_id)
    return f'All tasks of {staff.staffname}'

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
    if name == "" or email == "":
        flash('You missing some required information!!!')
        return redirect('/home_page_admin')
    elif Staff.query.filter_by(staffname = name).first():
        flash('This staff is already in the list')
        return redirect('/home_page_admin')
    elif Staff.query.filter_by(email = email).first():
        flash('This email is already used for the another staff')
        return redirect('/home_page_admin')

    staff = Staff(staffname = name, email = email)
    db.session.add(staff)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash('Unsuccessfully added this staff!!!')
        return redirect('/home_page_admin')
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
        return 'Unsuccessfully added new task'
    return redirect(url_for('check'))

@app.route('/delete_all_tasks')
def delete_all_tasks():
    Task.query.delete()
    db.session.commit()
    return 'Done'




@app.errorhandler(404)
def page_not_found(error):
    return "This page is not found.", 404
