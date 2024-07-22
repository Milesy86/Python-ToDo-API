import json
from models.task import Task
from sqlalchemy import select

class TestTasks:

    def test_get_tasks(self, get_token, client, session):
        token = get_token("testuser", "testpass")

        task1 = Task(title="Task 1", description="Description 1", completed=False, user_id=1)
        task2 = Task(title="Task 2", description="Description 2", completed=True, user_id=1)
        session.add(task1)
        session.add(task2)
        session.commit()

        response = client.get("/tasks", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        tasks = response.json["tasks"]
        assert len(tasks) == 2
        assert tasks[0]["title"] == "Task 1"
        assert tasks[1]["title"] == "Task 2"
    
    def test_add_task(self, get_token, client, session):
        token = get_token("testuser", "testpass")

        task_data = {
            "title": "Test Task 1",
            "description": "Test Description 1",
            "completed": False,
            "user_id": 1
        }
        response = client.post("/tasks", headers={"Authorization": f"Bearer {token}"}, data=json.dumps(task_data), content_type="application/json")
        assert response.status_code == 201
        assert response.json == {"msg": "Task added"}

        task = session.execute(select(Task).filter_by(title=task_data["title"])).scalar_one()
        assert task is not None
        assert task.title == task_data["title"]
        assert task.description == task_data["description"]
        assert not task.completed
        assert task.user_id == task_data["user_id"]

        # Test adding a task with no "completed" property. It should default to False.
        task_data = {
            "title": "Test Task 2",
            "description": "Test Description 2",
            "user_id": 1
        }
        response = client.post("/tasks", headers={"Authorization": f"Bearer {token}"}, data=json.dumps(task_data), content_type="application/json")
        assert response.status_code == 201
        assert response.json == {"msg": "Task added"}

        task = session.execute(select(Task).filter_by(title=task_data["title"])).scalar_one()
        assert task is not None
        assert task.title == task_data["title"]
        assert task.description == task_data["description"]
        assert not task.completed
        assert task.user_id == task_data["user_id"]
        
    def test_add_task_missing_title(self, get_token, client, session):
        token = get_token("testuser", "testpass")

        task_data = {
            "description": "Test Description",
            "completed": False,
            "user_id": 1
        }
        response = client.post("/tasks", headers={"Authorization": f"Bearer {token}"}, data=json.dumps(task_data), content_type="application/json")
        assert response.status_code == 400
        assert response.json["error"] == "Title, description and user_id are required."

    def test_add_task_missing_description(self, get_token, client, session):
        token = get_token("testuser", "testpass")

        task_data = {
            "title": "Test Task",
            "completed": False,
            "user_id": 1
        }
        response = client.post("/tasks", headers={"Authorization": f"Bearer {token}"}, data=json.dumps(task_data), content_type="application/json")
        assert response.status_code == 400
        assert response.json["error"] == "Title, description and user_id are required."

    def test_add_task_missing_user_id(self, get_token, client, session):
        token = get_token("testuser", "testpass")

        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "completed": False, 
        }
        response = client.post("/tasks", headers={"Authorization": f"Bearer {token}"}, data=json.dumps(task_data), content_type="application/json")
        assert response.status_code == 400
        assert response.json["error"] == "Title, description and user_id are required."

    def test_update_task(self, get_token, client, session):
        token = get_token("testuser", "testpass")

        task = Task(title="Task to Update", description="Update Description", completed=False, user_id=1)
        session.add(task)
        session.commit()

        update_data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "completed": True
        }
        response = client.put(f"/tasks/{task.id}", headers={"Authorization": f"Bearer {token}"}, data=json.dumps(update_data), content_type="application/json")
        assert response.status_code == 200
        assert response.json == {"msg": "Task updated"}

        updated_task = session.execute(select(Task).filter_by(id=task.id)).scalar_one()
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Updated Description"
        assert updated_task.completed
        assert updated_task.user_id == 1

    def test_delete_task(self, get_token, client, session):
        token = get_token("testuser", "testpass")

        task = Task(title="Task to Delete", description="Delete Description", completed=False, user_id=1)
        session.add(task)
        session.commit()

        response = client.delete(f"/tasks/{task.id}", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 201
        assert response.json == {"msg": "Task deleted"}

        deleted_task = session.execute(select(Task).filter_by(id=task.id)).scalar_one_or_none()
        assert deleted_task is None

    def test_get_task_by_id(self, get_token, client, session):
        token = get_token("testuser", "testpass")

        task1 = Task(title="Task 1", description="Description 1", completed=False, user_id=1)
        task2 = Task(title="Task 2", description="Description 2", completed=True, user_id=1)
        session.add(task1)
        session.add(task2)
        session.commit()

        response = client.get("/tasks/1", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        response_task = response.json
        assert response_task["title"] == "Task 1"
        response = client.get("/tasks/2", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        response_task = response.json
        assert response_task["title"] == "Task 2"

    def test_get_tasks_no_token(self, client):
        response = client.get("/tasks")
        assert response.status_code == 401
        assert response.json["msg"] == "Missing Authorization Header"
    
    def test_add_task_no_token(self, client):
        response = client.post("/tasks")
        assert response.status_code == 401
        assert response.json["msg"] == "Missing Authorization Header"

    def test_get_task_by_id_no_token(self, client):
        response = client.get(f"/tasks")
        assert response.status_code == 401
        assert response.json["msg"] == "Missing Authorization Header"