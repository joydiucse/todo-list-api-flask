from flask import Flask, jsonify, request

# Create a Flask web application instance
app = Flask(__name__)

# In-memory list to store tasks
# Each task will be a dictionary with keys: id, title, done
tasks = []

# Route to get all tasks
# HTTP Method: GET
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Return the list of tasks as JSON response
    return jsonify(tasks)

# Route to create a new task
# HTTP Method: POST
@app.route('/tasks', methods=['POST'])
def create_task():
    # Get JSON data sent in the request body
    data = request.get_json()

    # Create a new task dictionary with a unique id,
    # the 'title' from the request, and 'done' status as False by default
    new_task = {
        "id": len(tasks) + 1,      # Assign next id based on current length
        "title": data.get('title'), # Extract title from JSON data
        "done": False              # Task starts as not done
    }

    # Add the new task to the tasks list
    tasks.append(new_task)

    # Return the updated tasks list with HTTP status code 201 (Created)
    return jsonify(tasks), 201

# Route to update an existing task by its id
# HTTP Method: PUT
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # Get JSON data sent in the request body
    data = request.get_json()

    # Loop through the tasks list to find the task with matching id
    for task in tasks:
        if task['id'] == task_id:
            # Update the task title if a new title is provided
            if data.get('title'):
                task['title'] = data['title']

            # Update the 'done' status if provided, otherwise keep current status
            task['done'] = data.get('done', task['done'])

            # Return the updated task as JSON response
            return jsonify(task)

    # If no task with given id is found, return error with 404 status
    return jsonify({'error': 'Task not found'}), 404

# Route to delete a task by its id
# HTTP Method: DELETE
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Enumerate through tasks to get index and task simultaneously
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            # Remove the task from the list using pop()
            tasks.pop(i)

            # Return success response
            return jsonify({'success': True})

    # If task not found, return error with 404 status
    return jsonify({"error": "Task not found"}), 404

# Run the Flask app only if this script is executed directly (not imported)
if __name__ == '__main__':
    # Enable debug mode to auto-reload on code changes and show detailed errors
    app.run(debug=True)
