from ortools.sat.python import cp_model
import matplotlib.pyplot as plt

from src.helpers.exporter import export_cp_model


class SolveTaskScheduling:
    def __init__(self, durations, x_matrix, y_matrix, global_start=0):
        self.durations = durations
        self.x_matrix = x_matrix
        self.y_matrix = y_matrix
        self.global_start = global_start

        self.N = len(durations)
        self.K = len(y_matrix[0])
        self.horizon = sum(durations)

        self.task_data = []  # To store solved task (id, start, end, station)

    def find_solution(self):
        model = cp_model.CpModel()

        # Variables
        start_vars = [model.NewIntVar(self.global_start, self.horizon, f'start_{i}') for i in range(self.N)]
        end_vars = [model.NewIntVar(self.global_start, self.horizon, f'end_{i}') for i in range(self.N)]
        interval_vars = [
            model.NewIntervalVar(start_vars[i], self.durations[i], end_vars[i], f'interval_{i}')
            for i in range(self.N)
        ]

        # Precedence constraints
        for i in range(self.N):
            for j in range(self.N):
                if self.x_matrix[i][j] == 1:
                    model.Add(start_vars[j] >= end_vars[i])

        # Disjunctive resource constraints (No overlap on the same station)
        for k in range(self.K):
            tasks_on_k = [i for i in range(self.N) if self.y_matrix[i][k] == 1]
            if len(tasks_on_k) > 1:
                model.AddNoOverlap([interval_vars[i] for i in tasks_on_k])

        # Optional: Minimize makespan
        makespan = model.NewIntVar(self.global_start, self.horizon, 'makespan')
        model.AddMaxEquality(makespan, end_vars)
        model.Minimize(makespan)

        # Export CP-SAP in
        export_cp_model(model, "my_cp_model", text_format_output=True)

        # Solve
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(f"\n✅ Solution found. Makespan: {solver.Value(makespan)} seconds\n")
            for i in range(self.N):
                start = solver.Value(start_vars[i])
                end = solver.Value(end_vars[i])
                station = self.y_matrix[i].index(1)
                self.task_data.append((i, start, end, station))
                print(f"Task {i}: Start at {start}, End at {end}, Duration: {self.durations[i]}, Station: {station}")

            self._plot_gantt_chart()
        else:
            print("❌ No feasible solution found.")

    def _plot_gantt_chart(self):
        fig, ax = plt.subplots(figsize=(10, 1 + self.K))
        cmap = plt.cm.get_cmap("tab10", self.K)

        for task_id, start, end, station in self.task_data:
            ax.barh(
                y=station,
                width=end - start,
                left=start,
                height=0.6,
                color=cmap(station),
                edgecolor='black'
            )
            ax.text(start + 0.1, station, f'T{task_id}', va='center', ha='left', fontsize=9, color='white')

        ax.set_yticks(range(self.K))
        ax.set_yticklabels([f'Station {k}' for k in range(self.K)])
        ax.set_xlabel("Time (seconds)")
        ax.set_title("Gantt Chart of Task Schedule")
        ax.grid(True, axis='x')
        plt.tight_layout()
        plt.show()


# Example usage
if __name__ == "__main__":
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

    scheduler = SolveTaskScheduling(durations, x_matrix, y_matrix, global_start=0)
    scheduler.find_solution()
