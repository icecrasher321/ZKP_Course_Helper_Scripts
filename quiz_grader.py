import pandas as pd

# Step 1: Load Quiz CSV files into dictionary
quiz_csvs = {
    'Quiz 3': 'quiz3.csv',
    'Quiz 4': 'quiz4.csv'
}
quiz_emails = {}
for quiz_name, filename in quiz_csvs.items():
    quiz_df = pd.read_csv(filename)
    quiz_emails[quiz_name] = list(quiz_df['Email Address'])

# Step 2: Load Enrollment CSV files into dictionary
enrollment_csvs = ['enrollment_ugrad.csv', 'enrollment_grad.csv']
enrollment = {}
for filename in enrollment_csvs:
    enrollment_df = pd.read_csv(filename)
    for index, row in enrollment_df.iterrows():
        enrollment[row['Student ID']] = row['Email Address']

# Step 3: Load BCourses CSV file into dataframe
bcourses_csv = 'bcourses_1.csv'
bcourses_df = pd.read_csv(bcourses_csv)

# Step 4: Update BCourses dataframe with quiz scores
for quiz_name, emails in quiz_emails.items():
    quiz_column = quiz_name + ' (856860' + quiz_name[-1] + ')'
    for index, row in bcourses_df.iterrows():
        if row['SIS User ID'] in enrollment.keys():
            email = enrollment[row['SIS User ID']]
            if email in emails:
                bcourses_df.at[index, quiz_column] = 1.00
            else:
                bcourses_df.at[index, quiz_column] = 0.00

# Step 5: Write updated BCourses dataframe to CSV file
bcourses_df.to_csv('updated_bcourses_2.csv', index=False)
