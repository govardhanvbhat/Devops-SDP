from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Function to get database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # your MySQL username
        password="admin",  # your MySQL password
        database="employee_managers"  # database name changed
    )

# Route to display all employees
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    conn.close()
    return render_template('index.html', employees=employees)

# Route to create a new employee
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        position = request.form['position']
        salary = request.form['salary']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO employees (name, email, position, salary) VALUES (%s, %s, %s, %s)', (name, email, position, salary))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('create.html')

# Route to edit an employee's details
@app.route('/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        position = request.form['position']
        salary = request.form['salary']

        cursor.execute('UPDATE employees SET name=%s, email=%s, position=%s, salary=%s WHERE id=%s',
                       (name, email, position, salary, employee_id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM employees WHERE id = %s', (employee_id,))
    employee = cursor.fetchone()
    conn.close()

    return render_template('edit.html', employee=employee)

# Route to delete an employee
@app.route('/delete/<int:employee_id>', methods=['GET'])
def delete(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE id = %s', (employee_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5001)
