from unittest import TestCase

from src.application.solve_task_scheduling import solve_task_scheduling_2_stations_4_tasks, solve_task_scheduling_8_task_2_stations, \
    solve_task_scheduling_for_input_file


class TestEquations(TestCase):

    def test_should_find_solution_1(self) -> None:
        solution_found = solve_task_scheduling_2_stations_4_tasks()

        # assert solution_found == True

    def test_should_find_solution_2(self) -> None:
        solution_found = solve_task_scheduling_8_task_2_stations()

        # assert solution_found == True

    def test_should_find_solution_8(self) -> None:
        solution_found = solve_task_scheduling_for_input_file("8-tasks-2-stations-production-schedule.json")

        # assert solution_found == True

    def test_should_find_solution_945(self) -> None:
        solution_found = solve_task_scheduling_for_input_file("945-production-schedule.json")

        # assert solution_found == True

    def test_should_find_solution_5824(self) -> None:
        solution_found = solve_task_scheduling_for_input_file("5824-production-schedule.json")

        # assert solution_found == True

    def test_should_find_solution_7208(self) -> None:
        solution_found = solve_task_scheduling_for_input_file("7208-production-schedule.json")

        # assert solution_found == True

    def test_should_find_solution_8006(self) -> None:
        solution_found = solve_task_scheduling_for_input_file("8006-production-schedule.json")

        # assert solution_found == True

    def test_should_find_solution_20043(self) -> None:
        solution_found = solve_task_scheduling_for_input_file("20043-production-schedule.json")

        # assert solution_found == True

    def test_should_find_solution_20119(self) -> None:
        solution_found = solve_task_scheduling_for_input_file("20119-production-schedule.json")

        # assert solution_found == True

    def test_should_find_solution_9000456(self) -> None:
        solution_found = solve_task_scheduling_for_input_file("9000456-production-schedule.json")

        # assert solution_found == True
