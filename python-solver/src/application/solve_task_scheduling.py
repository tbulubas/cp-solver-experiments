from common.utils import load_json_from_subdir
from src.algorithm.cp_task_scheduling import SolveTaskScheduling
import json

from src.helpers.transform_tasks import transform_tasks, transform_tasks_from_dict
from src.helpers.visualization import plot_task_dependency_dag


def solve_task_scheduling_2_stations_4_tasks():
    durations = [4, 3, 2, 5]
    x_matrix = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ]
    y_matrix = [
        [1, 0],
        [1, 0],
        [0, 1],
        [0, 1],
    ]

    solver = SolveTaskScheduling(durations, x_matrix, y_matrix, global_start=0)

    solver.find_solution()


def solve_task_scheduling_8_task_2_stations():
    durations = [30, 20, 30, 30, 30, 20, 30, 30]

    x_matrix = [[0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0]]
    y_matrix = [[1, 0], [1, 0], [1, 0], [1, 0], [0, 1], [0, 1], [0, 1], [0, 1]]

    solver = SolveTaskScheduling(durations, x_matrix, y_matrix, global_start=0)

    solver.find_solution()


def solve_task_scheduling_for_input_file(input_file_name):

    data = load_json_from_subdir("solver-benchmarks", input_file_name)

    tasks = data["Tasks"]

    durations, x_matrix, y_matrix, global_start, task_id_map, station_id_map = transform_tasks_from_dict(data)

    # Visualize dependencies
    plot_task_dependency_dag(tasks, task_id_map)
    global_start = 0

    solver = SolveTaskScheduling(durations, x_matrix, y_matrix, global_start=global_start)
    solver.find_solution()


