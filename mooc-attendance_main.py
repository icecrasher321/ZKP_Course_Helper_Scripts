import csv
from datetime import datetime, timedelta

def parse_csv(input_file, output_file, correct_code):
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    with open(output_file, 'w', newline='') as f:
        fieldnames = ['Berkeley Email', 'Sessions Attended']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()

        end_time = datetime.strptime("1/24/2023 18:40:00", '%m/%d/%Y %H:%M:%S')

        for row in data:
            email = row['Email (Berkeley email)']
            code = row['Attendance Code'].lower()
            timestamp = row['Timestamp']

            if code != correct_code:
                writer.writerow({'Berkeley Email': email, 'Sessions Attended': 0})
                continue

            submit_time = datetime.strptime(timestamp, '%m/%d/%Y %H:%M:%S')
            time_diff = submit_time - end_time

            if time_diff <= timedelta(minutes=20):
                writer.writerow({'Berkeley Email': email, 'Sessions Attended': 1})
            else:
                writer.writerow({'Berkeley Email': email, 'Sessions Attended': 0})

input_file = 'zkp_attendance.csv'
output_file = 'result.csv'
correct_code = 'sigma'

parse_csv(input_file, output_file, correct_code)
