import json
import exec

def DecodeJSON(response):
    
    if isinstance(response, str):  #if the response is a string
        try:                                    
            response_data = json.loads(response)    #Try to decode the string as JSON
        except json.JSONDecodeError as e:           #If the JSON decoder throws an error
            print(f"Error decoding JSON: {e}")      #Print the error message
            return
    else:
        response_data = response  #If the response is already a dictionary, use it directly

    # Grab the relevant values. It says default error message if nothing is there.
    intro = response_data.get("Intro", "No Intro provided.")
    results = response_data.get("results", "No results provided.")
    conclusion = response_data.get("conclusion", "No conclusion provided.")
    script = response_data.get("Script", "No Script provided.")

    print(intro)
    exec.execute_command(script)  # Execute the script command



# Example JSON response
example_response = """
{
    "Intro": "Intro",
    "results": "results",
    "conclusion": "conclusion",
    "Script": "echo \\"Script\\""
}
"""

if __name__ == "__main__":
    DecodeJSON(example_response)