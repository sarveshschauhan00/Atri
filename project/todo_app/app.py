from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# File path for the CSV file
CSV_FILE = os.path.join(os.path.dirname(__file__), 'tasks.csv')

# Function to read tasks from the CSV file
def read_tasks():
    tasks = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tasks.append(row)
    return tasks

# Function to write tasks to the CSV file
def write_tasks(tasks):
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ['id', 'title', 'description', 'status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)

# Function to get a task by ID
def get_task_by_id(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

@app.route('/')
def index():
    tasks = read_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        tasks = read_tasks()
        new_id = str(len(tasks) + 1)
        new_task = {
            'id': new_id,
            'title': request.form['title'],
            'description': request.form['description'],
            'status': 'Pending'
        }
        tasks.append(new_task)
        write_tasks(tasks)
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/edit/<task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = get_task_by_id(task_id)
    if not task:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        tasks = read_tasks()
        for t in tasks:
            if t['id'] == task_id:
                t['title'] = request.form['title']
                t['description'] = request.form['description']
                t['status'] = request.form['status']
                break
        write_tasks(tasks)
        return redirect(url_for('index'))
    
    return render_template('edit_task.html', task=task)

@app.route('/delete/<task_id>')
def delete_task(task_id):
    tasks = read_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    write_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
