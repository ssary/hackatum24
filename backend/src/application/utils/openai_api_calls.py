import json

def create_chat_completion(client, user_1_input, user_2_input):
    messages = [
        {
            "role": "system",
            "content": "You are the best matching application, You Match activities and return answer in JSON format."
        },
        {
            "role": "user",
            "content": (
                f"Input is users details that may have matching interests to meet. "
                f"Your output is \"true\" if and only if the users is matching and can do the activity together based on their input, else you output \"false\".\n"
                f"The activities doesn’t need to be the same, but to be similar activities.\n"
                f"USER_1: {user_1_input}\nUSER_2: {user_2_input}"
            )
        }
    ]

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "response_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "match_output": {
                        "description": "The Binary output of the matching",
                        "type": "boolean"
                    },
                    "explanation": {
                        "description": "The reason for the output of the matching",
                        "type": "string"
                    }
                },
                "additionalProperties": False
            }
        }
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format=response_format
    )

    response_content = response.choices[0].message.content
    response_content = json.loads(response_content)
    # contains match_output and explanation
    return response_content