
# Training Tracker Application

This project is a Python application that reads training data from a JSON file and generates multiple outputs related to completed trainings. The application processes the data and outputs information such as the count of completed trainings, a list of people who completed specific trainings in a fiscal year, and a list of people with expired or soon-to-expire trainings.

## Features

1. **Count Completed Trainings**: The app counts how many people have completed each training.
2. **Fiscal Year Filter**: The app lists all people who completed specified trainings within a given fiscal year (July 1 to June 30).
3. **Expired or Soon-to-Expire Trainings**: The app finds all people with expired or soon-to-expire trainings as of a specified date.

## Input Data Format - trainings.txt

The input file must be a JSON file containing a list of people with the following structure:

```json
[
  {
    "name": "Person Name",
    "completions": [
      {
        "name": "Training Name",
        "timestamp": "mm/dd/yyyy",
        "expires": "mm/dd/yyyy"
      }
    ]
  }
]
