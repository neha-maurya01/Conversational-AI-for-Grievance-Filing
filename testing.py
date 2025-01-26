import pandas as pd
from engine import predict_category
from tqdm import tqdm

# Load the dataset
df = pd.read_csv("./dataset/grievances_dataset.csv")
count = 0

# Open the file in write mode
with open("./results/test_output.txt", "w") as file:
    for itr, row in tqdm(df.iterrows()):
        # Predict the category
        p_dept, p_cat, p_score = predict_category(row['Grievance'])
        if p_dept == row['Category/Label']:
            count += 1
        else:
            # Write the output to the file
            file.write(f"{row['Grievance']}\n")
            file.write(f"{p_dept}, {p_cat}, {p_score}\n")
            file.write(f"{row['Category/Label']}\n")
            file.write("--------------------------------------------------------------------\n")

# Calculate accuracy
accuracy = count / 200
print(accuracy * 100)
