import json

task = {
    "uuid": "huihuihui",
    "client-id": "283980f1-c138-4fc6-88f9-845f618d8516",
    "message": "Hallo",
    "state": False
}

with open("resources/tasks.json", "r") as file:
    data = json.load(file)

    data["tasks"].append(task)

    with open("resources/tasks.json", "w") as file:
        json.dump(data, file)
        file.close()

    file.close()
