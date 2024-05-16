#!/usr/bin/env python3
import json
import sys


class SchedulingTask:
    def __init__(self, num_tasks, processing_times, release_times, deadlines):
        """
        Initialize the scheduling task with the number of tasks, processing times, release times, and deadlines.
        """
        self.num_tasks = num_tasks
        self.processing_times = processing_times
        self.release_times = release_times
        self.deadlines = deadlines
        self.best_solution = []
        self.upper_bound = None

    def get_schedule(self):
        """
        Return the final schedule - the optimal start time of each task.
        If scheduling is not possible, return [-1].
        """
        if not self.best_solution:
            return [-1]
        current_time = 0
        schedule = [0] * self.num_tasks
        for task_index in self.best_solution:
            scheduled_time = max(current_time, self.release_times[task_index])
            schedule[task_index] = scheduled_time
            current_time = scheduled_time + self.processing_times[task_index]
        return schedule


def load_tasks(filename):
    """
    Load the task specifications from a JSON file.
    """
    with open(filename) as file:
        data = json.load(file)
        num_tasks = len(data)
        processing_times = [task["proc_times"] for task in data]
        release_times = [task["release_times"] for task in data]
        deadlines = [task["deadline"] for task in data]
    return num_tasks, processing_times, release_times, deadlines


def display_schedule_tree(scheduled, to_schedule, current_time, depth):
    """
    Print the current state of the scheduling tree with proper indentation.
    """
    indent = "  " * depth
    print(
        f"{indent}Scheduled: {scheduled}, To schedule: {to_schedule}, Current time: {current_time}"
    )


def branch_and_bound(scheduled, to_schedule, current_time, task, depth=0):
    """
    Branch and Bound algorithm for task scheduling.
    This algorithm explores all possible task permutations and prunes the tree when possible.

    :param scheduled: List of scheduled tasks
    :param to_schedule: List of tasks to be scheduled
    :param current_time: Current completion time
    :param task: SchedulingTask object containing task parameters
    :param depth: Current depth in the scheduling tree (for printing purposes)
    :return: True if an optimal solution is found, False otherwise
    """
    display_schedule_tree(scheduled, to_schedule, current_time, depth)

    # Check for missed deadlines
    for task_index in to_schedule:
        if (
            max(current_time, task.release_times[task_index])
            + task.processing_times[task_index]
            > task.deadlines[task_index]
        ):
            return False

    # Check if all tasks are scheduled
    if not to_schedule:
        if task.upper_bound is None or current_time < task.upper_bound:
            task.upper_bound = current_time
            task.best_solution = scheduled
        return False
    else:
        # Calculate lower bound
        lower_bound = max(
            current_time,
            min(task.release_times[task_index] for task_index in to_schedule),
        ) + sum(task.processing_times[task_index] for task_index in to_schedule)
        if task.upper_bound is None:
            upper_bound = max(task.deadlines[task_index] for task_index in to_schedule)
            if lower_bound > upper_bound:
                return False
        else:
            if lower_bound >= task.upper_bound:
                return False

    # Decomposition: update best_solution if possible
    optimal_partial_solution = False
    if current_time <= min(
        task.release_times[task_index] for task_index in to_schedule
    ):
        task.best_solution = scheduled + to_schedule
        optimal_partial_solution = True

    # Branching: try scheduling each task in to_schedule
    for i in range(len(to_schedule)):
        if branch_and_bound(
            scheduled + [to_schedule[i]],
            to_schedule[:i] + to_schedule[i + 1 :],
            max(current_time, task.release_times[to_schedule[i]])
            + task.processing_times[to_schedule[i]],
            task,
            depth + 1,
        ):
            return True

    return optimal_partial_solution


def main():
    """
    Main function to load tasks, run the scheduling algorithm, and print the result.
    """
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        return

    input_file = sys.argv[1]
    task_num, proc_times, release_times, deadlines = load_tasks(input_file)
    task = SchedulingTask(task_num, proc_times, release_times, deadlines)

    scheduled_tasks = []
    not_scheduled_tasks = [i for i in range(task_num)]
    branch_and_bound(scheduled_tasks, not_scheduled_tasks, 0, task)

    print("\n ####--------------- Final Result ---------------####\n")

    if task.best_solution == []:
        print("Scheduling not possible")
    else:
        print("Optimal task order:", task.best_solution)
        print("Optimal schedule (start times):", task.get_schedule())


if __name__ == "__main__":
    main()
