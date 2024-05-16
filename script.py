#!/usr/bin/env python3
import json
import sys

class TaskScheduler:
    def __init__(self, num_tasks, exec_times, start_times, deadlines):
        """
        Initialize the TaskScheduler with the number of tasks, execution times, start times, and deadlines.
        """
        self.num_tasks = num_tasks
        self.exec_times = exec_times
        self.start_times = start_times
        self.deadlines = deadlines
        self.optimal_order = []
        self.minimum_time = None

    def compute_schedule(self):
        """
        Return the final schedule - the optimal start time of each task.
        If scheduling is not possible, return [-1].
        """
        if not self.optimal_order:
            return [-1]
        current_time = 0
        schedule = [0] * self.num_tasks
        for task_idx in self.optimal_order:
            start_time = max(current_time, self.start_times[task_idx])
            schedule[task_idx] = start_time
            current_time = start_time + self.exec_times[task_idx]
        return schedule

    def compute_maximum_lateness(self, schedule):
        """
        Compute the maximum lateness of the schedule.
        """
        max_lateness = 0
        for idx in range(self.num_tasks):
            finish_time = schedule[idx] + self.exec_times[idx]
            lateness = finish_time - self.deadlines[idx]
            if lateness > max_lateness:
                max_lateness = lateness
        return max_lateness

def parse_tasks(filename):
    """
    Parse the task specifications from a JSON file.
    """
    with open(filename) as file:
        data = json.load(file)
        num_tasks = len(data)
        exec_times = [task["proc_times"] for task in data]
        start_times = [task["release_times"] for task in data]
        deadlines = [task["deadline"] for task in data]
    return num_tasks, exec_times, start_times, deadlines

def print_schedule_tree(scheduled, remaining, current_time, level):
    """
    Print the current state of the scheduling tree with proper indentation.
    """
    indent = "  " * level
    print(f"{indent}Scheduled: {scheduled}, Remaining: {remaining}, Current time: {current_time}")

def schedule_bratley(scheduled, remaining, current_time, scheduler, level=0):
    """
    Bratley algorithm for task scheduling.
    This algorithm explores all possible task permutations and prunes the tree when possible.
    
    :param scheduled: List of scheduled tasks
    :param remaining: List of tasks to be scheduled
    :param current_time: Current completion time
    :param scheduler: TaskScheduler object containing task parameters
    :param level: Current depth in the scheduling tree (for printing purposes)
    :return: True if an optimal solution is found, False otherwise
    """
    print_schedule_tree(scheduled, remaining, current_time, level)
    
    # Check for missed deadlines
    for task_idx in remaining:
        if max(current_time, scheduler.start_times[task_idx]) + scheduler.exec_times[task_idx] > scheduler.deadlines[task_idx]:
            return False

    # Check if all tasks are scheduled
    if not remaining:
        if scheduler.minimum_time is None or current_time < scheduler.minimum_time:
            scheduler.minimum_time = current_time
            scheduler.optimal_order = scheduled
        return False
    else:
        # Calculate lower bound
        lower_bound = max(current_time, min(scheduler.start_times[task_idx] for task_idx in remaining)) + sum(scheduler.exec_times[task_idx] for task_idx in remaining)
        if scheduler.minimum_time is None:
            upper_bound = max(scheduler.deadlines[task_idx] for task_idx in remaining)
            if lower_bound > upper_bound:
                return False
        else:
            if lower_bound >= scheduler.minimum_time:
                return False
    
    # Decomposition: update optimal_order if possible
    optimal_partial_solution = False
    if current_time <= min(scheduler.start_times[task_idx] for task_idx in remaining):
        scheduler.optimal_order = scheduled + remaining
        optimal_partial_solution = True
    
    # Branching: try scheduling each task in remaining
    for i in range(len(remaining)):
        if schedule_bratley(scheduled + [remaining[i]], remaining[:i] + remaining[i+1:], max(current_time, scheduler.start_times[remaining[i]]) + scheduler.exec_times[remaining[i]], scheduler, level + 1):
            return True
    
    return optimal_partial_solution

def main():
    """
    Main function to parse tasks, run the scheduling algorithm, and print the result.
    """
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        return
    
    input_file = sys.argv[1]
    task_count, exec_times, start_times, deadlines = parse_tasks(input_file)
    scheduler = TaskScheduler(task_count, exec_times, start_times, deadlines)
    
    scheduled_tasks = []
    remaining_tasks = [i for i in range(task_count)]
    schedule_bratley(scheduled_tasks, remaining_tasks, 0, scheduler)

    print("\n####--------------- Final Result ---------------####\n")

    if scheduler.optimal_order == []:
        print("Scheduling not possible")
    else:
        optimal_schedule = scheduler.compute_schedule()
        max_lateness = scheduler.compute_maximum_lateness(optimal_schedule)
        print("Optimal task order:", scheduler.optimal_order)
        print("Optimal schedule (start times):", optimal_schedule)
        print("Maximum lateness:", max_lateness)

if __name__ == "__main__":
    main()
