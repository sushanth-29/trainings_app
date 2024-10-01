import json
from datetime import datetime, timedelta

# Load data from the JSON file
with open('trainings.txt', 'r') as f:
    data = json.load(f)


def get_most_recent_completion(completions):
    """Return the most recent completion date for each training for a particular person."""
    distinct_completions = {}
    for comp in completions:
        name = comp["name"]
        timestamp = datetime.strptime(comp["timestamp"], '%m/%d/%Y')
        if name not in distinct_completions or timestamp > distinct_completions[name]["timestamp"]:
            distinct_completions[name] = {
                "timestamp": timestamp, "expires": comp.get("expires")}
    return distinct_completions

# 1. List each completed training with a count of how many people have completed that training


def find_completed_trainings_count(data):
    count_trainings = {}
    for person in data:
        completions = get_most_recent_completion(person['completions'])
        for training in completions.keys():
            count_trainings[training] = count_trainings.get(training, 0) + 1
    return count_trainings

# 2. List all people that completed specified trainings within a fiscal year


def find_completed_trainings_by_fiscal_year(data, trainings, fiscal_year):
    start_date = datetime(fiscal_year - 1, 7, 1)
    end_date = datetime(fiscal_year, 6, 30)
    result = {training: [] for training in trainings}

    for person in data:
        completions = get_most_recent_completion(person['completions'])
        for training, info in completions.items():
            if training in trainings and start_date <= info["timestamp"] <= end_date:
                result[training].append(person["name"])

    return result

# 3. Find all people with expired or soon-to-expire trainings


def find_expired_trainings(data, check_date):
    check_date = datetime.strptime(check_date, '%m/%d/%Y')
    expires_soon_threshold = check_date + timedelta(days=30)
    result = {}

    for person in data:
        completions = get_most_recent_completion(person['completions'])
        for training, info in completions.items():
            if info["expires"]:
                expires_date = datetime.strptime(info["expires"], '%m/%d/%Y')
                status = None
                if expires_date < check_date:
                    status = "Expired"
                elif check_date <= expires_date <= expires_soon_threshold:
                    status = "Expires Soon"

                if status:
                    # Group all expired or expiring trainings under the same person
                    if person["name"] not in result:
                        result[person["name"]] = []
                    result[person["name"]].append(
                        {"training": training, "status": status})

    return result


# Output 1: Count of completed trainings

training_count = find_completed_trainings_count(data)
print("Training Count:", json.dumps(training_count, indent=2))
# with open('trainings_count.json', 'w') as f:
#     json.dump(training_count, f, indent=2)


# Output 2: Trainings completed in Fiscal Year 2024
trainings = ["Electrical Safety for Labs",
             "X-Ray Safety", "Laboratory Safety Training"]
fiscal_year_results = find_completed_trainings_by_fiscal_year(
    data, trainings, 2024)
print("Fiscal Year 2024 Results:", json.dumps(fiscal_year_results, indent=2))

# with open('completed_trainings_in_fiscal_year.json', 'w') as f:
#     json.dump(fiscal_year_results, f, indent=2)


# Output 3: Expired or soon-to-expire trainings as of Oct 1, 2023
expired_trainings = find_expired_trainings(data, "10/01/2023")
print("Expired/Expires Soon Trainings:",
      json.dumps(expired_trainings, indent=2))

# with open('expired_trainings.json', 'w') as f:
#     json.dump(expired_trainings, f, indent=2)
