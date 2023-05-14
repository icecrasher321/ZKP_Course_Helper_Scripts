import pandas as pd

# Step 1: Load Enrollment CSV files into dictionary
enrollment_csvs = ['enrollment_ugrad.csv', 'enrollment_grad.csv']
enrollment = {}
for filename in enrollment_csvs:
    enrollment_df = pd.read_csv(filename)
    for index, row in enrollment_df.iterrows():
        enrollment[str(row['Student ID'])] = {'Email': row['Email Address'], 'Units': row['Units'], 'Name': row['Name']}


# Step 2: Load BCourses CSV file into dataframe
bcourses_csv = 'bc_view_final.csv'
bcourses_df = pd.read_csv(bcourses_csv)

# Step 3: Select only the columns you want
selected_columns = ['Student', 'SIS User ID', 'Lab (8578848)', 'Milestone Report (8582031)', 'HW (8586753)', 'Quizzes Final Score']
bcourses_df = bcourses_df[selected_columns]

# Step 4: Rename columns to match your desired output
bcourses_df = bcourses_df.rename(columns={'SIS User ID': 'Student ID', 'Quizzes Final Score': 'Quizzes Final Score (8583536)'})

# Step 5: Merge with enrollment data to get email addresses
enrollment_df = pd.DataFrame.from_dict(enrollment, orient='index')
enrollment_df.index.name = 'Student ID'
bcourses_df = bcourses_df.merge(enrollment_df, on='Student ID', how='right')

# Step 6: Merge with makeup data to get makeup counts
makeup_csv = 'makeup_final.csv'
makeup_df = pd.read_csv(makeup_csv)
makeup_df = makeup_df.rename(columns={' Makeup Count': 'Makeup Count'})  # remove extra space in column name
makeup_df = makeup_df[['Email', 'Makeup Count']]
bcourses_df = bcourses_df.merge(makeup_df, on='Email', how='left')

# Step 7: Merge with attendance data to get attendance counts
attendance_csv = 'attendance_final.csv'
attendance_df = pd.read_csv(attendance_csv)
attendance_df = attendance_df.rename(columns={'Student': 'Email', 'Sessions': 'Attendance Count'})  # rename columns to match
bcourses_df = bcourses_df.merge(attendance_df[['Email', 'Attendance Count']], on='Email', how='left')

# Step 8: Merge with article scores, Project Proposal, Presentation, Final Report sheet
articles_csv = 'other_scores.csv'
articles_df = pd.read_csv(articles_csv)
bcourses_df = bcourses_df.merge(articles_df[['Email', 'Article', 'Project Proposal', 'Project Presentation', 'Final report', 'Implementation Score']], on='Email', how='left')

# Step 9: Select the desired columns for output
selected_columns = ['Student ID', 'Email', 'Name', 'Units', 'Lab (8578848)', 'Milestone Report (8582031)', 'HW (8586753)', 'Quizzes Final Score (8583536)', 'Makeup Count', 'Attendance Count', 'Article', 'Project Proposal', 'Project Presentation', 'Final report', 'Implementation Score']
bcourses_df = bcourses_df[selected_columns]

# Step 10: Write updated BCourses dataframe to CSV file
bcourses_df.to_csv('Berkeley_Scores_Sheet_Updated.csv', index=False)




