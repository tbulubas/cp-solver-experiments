import json


def transform_tasks_from_dict(data):
    tasks = data["Tasks"]
    start_time = data["startTime"]

    # Step 1: Assign numeric index to each task and station
    task_id_map = {}
    station_id_map = {}
    durations = []

    for idx, task in enumerate(tasks):
        task_key = (task['id']['prodId'], task['id']['taskId'])
        task_id_map[task_key] = idx
        durations.append(task['duration'])

        station_id = task['station']
        if station_id not in station_id_map:
            station_id_map[station_id] = len(station_id_map)

    N = len(tasks)
    K = len(station_id_map)
    x_matrix = [[0 for _ in range(N)] for _ in range(N)]
    y_matrix = [[0 for _ in range(K)] for _ in range(N)]

    for j, task in enumerate(tasks):
        task_j_key = (task['id']['prodId'], task['id']['taskId'])

        # Preceding tasks
        for pred in task.get('dependingOn', []):
            task_i_key = (pred['prodId'], pred['taskId'])
            if task_i_key in task_id_map:
                i = task_id_map[task_i_key]
                x_matrix[i][j] = 1

        # Immediately preceding task (station-ordered constraint)
        imm_pred = task.get('preceding')
        if imm_pred:
            task_i_key = (imm_pred['prodId'], imm_pred['taskId'])
            if task_i_key in task_id_map:
                i = task_id_map[task_i_key]
                x_matrix[i][j] = 1

        # Assign station
        station_idx = station_id_map[task['station']]
        y_matrix[j][station_idx] = 1

    return durations, x_matrix, y_matrix, int(start_time), task_id_map, station_id_map


def transform_tasks(json_tasks):
    tasks = json.loads(json_tasks)

    # Step 1: Assign numeric index to each task and station
    task_id_map = {}
    station_id_map = {}
    durations = []

    for idx, task in enumerate(tasks):
        task_key = (task['id']['prodId'], task['id']['taskId'])
        task_id_map[task_key] = idx
        durations.append(task['duration'])

        station_id = task['station']
        if station_id not in station_id_map:
            station_id_map[station_id] = len(station_id_map)

    N = len(tasks)
    K = len(station_id_map)
    x_matrix = [[0 for _ in range(N)] for _ in range(N)]
    y_matrix = [[0 for _ in range(K)] for _ in range(N)]

    # Step 2: Build dependency matrix and station assignments
    for j, task in enumerate(tasks):
        task_j_key = (task['id']['prodId'], task['id']['taskId'])

        # Preceding tasks
        for pred in task.get('dependingOn', []):
            task_i_key = (pred['prodId'], pred['taskId'])
            if task_i_key in task_id_map:
                i = task_id_map[task_i_key]
                x_matrix[i][j] = 1

        # Immediately preceding task (must be same station)
        imm_pred = task.get('preceding')
        if imm_pred:
            task_i_key = (imm_pred['prodId'], imm_pred['taskId'])
            if task_i_key in task_id_map:
                i = task_id_map[task_i_key]
                x_matrix[i][j] = 1

        # Assign station
        station_idx = station_id_map[task['station']]
        y_matrix[j][station_idx] = 1

    return durations, x_matrix, y_matrix
