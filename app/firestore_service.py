import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()

def get_users():
    return db.collection('users').get()

def get_user(user_id):
    return db.collection('users').document(user_id).get()

def create_user(user_data):
    user_ref = db.collection('users').document()
    user_ref.set({'password': user_data.password,'username': user_data.username})
    return user_ref.id

def get_proyects(user_id):
    return db.collection('users').document(user_id).collection("projects").get()

def get_tasks(user_id,project_id):
    return db.collection('users').document(user_id).collection("projects").document(project_id).collection('tasks').get()

def create_alumn_task(user_id,project_id, task):
    tasks_ref = db.collection('users').document(user_id).collection("projects").document(project_id).collection('tasks').document()
    tasks_ref.set({"description":task.description.data,
                    "label":task.label.data,
                    "link_to_reference": task.link_to_reference.data,
                    "score":90,
                    "done":False})
def delete_task(user_id,project_id,task_id):
    task_ref = db.collection('users').document(user_id).collection("projects").document(project_id).collection('tasks').document(task_id)
    #task_ref = db.collection(f"/users/{user_id}/projects/{project_id}/tasks/{task_id}")
    task_ref.delete()

def update_task(user_id,project_id,task_id,done):
    task_ref = db.collection('users').document(user_id).collection("projects").document(project_id).collection('tasks').document(task_id)
    #task_ref = db.collection(f"/users/{user_id}/projects/{project_id}/tasks/{task_id}")
    task_ref.update({"done":not done})