# Task Scheduling with Bratley Algorithm

This project implements a task scheduling algorithm using the Bratley Algorithm. The goal is to find the optimal schedule for a set of tasks based on their processing times, release times, and deadlines.

## Usage

1. Prepare a JSON file with the task specifications (see the [Input Format](#input-format) section).

2. Run the script with the JSON file as an argument:
    ```sh
    python script.py <input_file>
    ```

## Input Format

The input JSON file should contain an array of tasks, where each task is an object with `release_times`, `proc_times`, and `deadline` fields. Here is an example:

```json
[
    {
        "release_times": 0,
        "proc_times": 3,
        "deadline": 9
    },
    {
        "release_times": 1,
        "proc_times": 2,
        "deadline": 6
    },
    {
        "release_times": 2,
        "proc_times": 1,
        "deadline": 5
    },
    {
        "release_times": 3,
        "proc_times": 2,
        "deadline": 7
    },
    {
        "release_times": 0,
        "proc_times": 1,
        "deadline": 4
    }
]
```
## Output Example
```
Scheduled: [], Remaining: [0, 1, 2, 3, 4], Current time: 0
  Scheduled: [0], Remaining: [1, 2, 3, 4], Current time: 3
  Scheduled: [1], Remaining: [0, 2, 3, 4], Current time: 3
  Scheduled: [2], Remaining: [0, 1, 3, 4], Current time: 3
  Scheduled: [3], Remaining: [0, 1, 2, 4], Current time: 5
  Scheduled: [4], Remaining: [0, 1, 2, 3], Current time: 1
    Scheduled: [4, 0], Remaining: [1, 2, 3], Current time: 4
    Scheduled: [4, 1], Remaining: [0, 2, 3], Current time: 3
      Scheduled: [4, 1, 0], Remaining: [2, 3], Current time: 6
      Scheduled: [4, 1, 2], Remaining: [0, 3], Current time: 4
        Scheduled: [4, 1, 2, 0], Remaining: [3], Current time: 7
        Scheduled: [4, 1, 2, 3], Remaining: [0], Current time: 6
          Scheduled: [4, 1, 2, 3, 0], Remaining: [], Current time: 9
      Scheduled: [4, 1, 3], Remaining: [0, 2], Current time: 5
    Scheduled: [4, 2], Remaining: [0, 1, 3], Current time: 3
    Scheduled: [4, 3], Remaining: [0, 1, 2], Current time: 5

####--------------- Final Result ---------------####

Optimal task order: [4, 1, 2, 3, 0]
Optimal schedule (start times): [6, 1, 3, 4, 0]
Maximum lateness: 0
```
