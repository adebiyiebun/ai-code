from openai import OpenAI
import string

# Set up OpenAI API key
client = OpenAI(api_key='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')

def extract_preferences(message):
    prompt = f"Extract the personal details and preferences from the following message, Otherwise output 'No New Details':\n\n\"{message}\". Output details as a list"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": prompt}
            ]
        )
    output = response.choices[0].message.content.strip().split('\n')
    return output

def format_preferences(message):

    # Extract personal details and preferences
    personal_details = {}
    preferences = []

    if 'No New Details' in message:
        return None

    for line in message:
        detail_type, detail_value = line.split(': ')[0].strip(string.punctuation), line.split(': ')[1].strip(string.punctuation)
        personal_details[detail_type] = detail_value


    # Format the output
    formatted_personal_details = [f"⭐ Fan's {detail_type.lower()} is {detail_value}." for detail_type, detail_value in personal_details.items()]
    formatted_preferences = [f"⭐ {preference}." for preference in preferences]

    output =[]
    for detail in formatted_personal_details:
        output.append(detail)

    return output

def extract(message):
    preferences = extract_preferences(message)
    output = format_preferences(preferences)
    if output == None:
        print('No New Details')
    else:
        for detail in output:
            print(detail)

fan_message = "My name is Fred, and I enjoy long walks on the beach, I like yellow"
extract(fan_message)