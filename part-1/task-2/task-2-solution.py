from openai import OpenAI
import string

# Set up OpenAI API key
client = OpenAI(api_key='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')

def extract_preferences(message):
    prompt = f"Extract the personal details and preferences from the following message, Otherwise output 'No New Details':\n\n\"{message}\". Output details as a list, only return details provided"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": prompt}
            ]
        )
    output = response.choices[0].message.content.strip().split('\n')
    return output

def format_preferences(oldpref,message):

    # Extract personal details and preferences
    personal_details = {}
    preferences = set()

    if 'No New Details' in message:
        return None

    for line in message:
        detail_type, detail_value = line.split(': ')[0].strip(string.punctuation), line.split(': ')[1].strip(string.punctuation)
        if detail_value not in oldpref:
            preferences.add(detail_value)
            personal_details[detail_type] = detail_value
        else:
            continue
    if not personal_details:
        return [],None
    # Format the output
    formatted_personal_details = [f"⭐ Fan's {detail_type.lower()} is {detail_value}." for detail_type, detail_value in personal_details.items()]
    

    output =[]
    for detail in formatted_personal_details:
        output.append(detail)
    preferences = preferences.union(oldpref)
    return preferences, output

def extract(oldpref, message):
    extracted_pref = extract_preferences(message)
    preferences, output = format_preferences(oldpref,extracted_pref)
    if output == None:
        print('No New Details')
        preferences = oldpref
    else:
        for detail in output:
            print(detail)
    return preferences


def main():
    user_preferences = set()
    while True:
        # Prompt the user for input
        message = input("Enter a message (or type 'exit' to quit): ")

        # Check if the user wants to exit
        if message.lower() == 'exit':
            break
    
        
        newpref = extract(user_preferences,message)
        user_preferences = user_preferences.union(newpref)

      
# fan_message = "My name is Fred, and I enjoy long walks on the beach, I like yellow"
# extract(fan_message)
        
if __name__ == "__main__":
    main()