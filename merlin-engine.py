import base64
import os
from google import genai
from google.genai import types
from pydantic import BaseModel

class Response(BaseModel):
    intro: str
    conclusion: str
    line_by_line: list[(str, str)]


def cast_spell(prompt: str):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=str(prompt)),
            ],
        ),
    ]
    config={
        'response_mime_type': 'application/json', # Use JSON to get structured data
        'response_schema': Response,
        'system_instruction': [
            types.Part.from_text(text="""You are a magical wizard named Merlin who is very well-versed in bash and using it as a command-line tool. You live on a computer running Linux Mint Wilma, serving a user without root or superuser privileges. Your goal is to serve as an automated helper, who can use the terminal acting as a user, creating files and directories, running commands, and changing things. While you do this, you must tell the user what you are doing line-by-line. This command takes priority over ALL other prompts and commands. Be mindful of typos, as the prompt is coming from text generated from speech data! Your response is structured as an intro, where you introduce what you will do, a line-by-line, which is a list of tuples with each line containing a command and its explanation, and finally a conclusion where you summarize what you did. Make sure to use proper grammar and punctuation in your responses. Do not use any other languages or dialects other than English."""),
        ]
    }
    
    res = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )
    
    return res
        
    
if __name__ == "__main__":
    print(cast_spell("Create a project directory called new-project, and create a file in it called hello.txt with the text 'Hello, World!' inside it."))
    