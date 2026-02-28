import os 
import json

def load_tasks(file_path):
    with open(file_path, "r") as f:
        tasks = [json.loads(line) for line in f if line.strip()]
    return tasks
    


def save_tasks(file_path, tasks):
    with open(file_path, "w") as f:
        for task in tasks:
            f.write(json.dumps(task) + "\n")