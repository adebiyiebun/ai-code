import csv 
import json

def group_consecutive_rows(csv_file):
    # Open the CSV file for reading
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        # Initialize variables to store grouped rows
        grouped_rows = []

        # Iterate over each row in the CSV file
        for row in csvreader:
            # If grouped_rows is not empty and the current row has the same role as the last row in grouped_rows, merge the messages
            if grouped_rows and grouped_rows[-1]['sender_handle'] == row['sender_handle']:
                grouped_rows[-1]['message'] += " " + row['message']
            else:
                # Add the current row to grouped_rows
                grouped_rows.append({'role': row['sender_handle'], 'message': row['message']})

    return grouped_rows

def convert_messages(csv_file, json_file):

    grouped_rows = group_consecutive_rows(csv_file)
    # Iterate over each row in the CSV file
    for i in range(0, len(grouped_rows), 2):
        current_row = grouped_rows[i]
        next_row = grouped_rows[i+1]
        messages = [{"role": "system", "content": "Jada is a creator on Fanvue, chatting with one of her fans."}]

        role_1 = "user" if current_row['role'] == 'fan' else "assistant"
        role_2 = "user" if next_row['role'] == 'fan' else "assistant"
            
        message_1  = {"role": role_1, "content": current_row['message']}
        message_2 = {"role": role_2, "content": next_row['message']}
        messages.append(message_1,message_2)

        with open(json_file, 'w') as jsonfile:
                json.dump({"messages": [messages]}, jsonfile)
                jsonfile.write("\n")

convert_messages('../fan_creator_chat.csv',"myfile.json")