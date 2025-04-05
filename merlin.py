import base64
import os
from google import genai
from google.genai import types
from pydantic import BaseModel
from errorstuff import Err

class Response(BaseModel):
    intro: str
    conclusion: str
    line_by_line: list[str]
    commands: list[str] 

class MerlinClient:
    client: genai.Client
    history: list[tuple[str, Response]]

    def __init__(self, key: str):
        self.client = genai.Client(
            api_key=key,
        )
        self.history = []
        
    
    def handle_err(self, error: Err):
        return self.cast_spell(
            f"Fix the error that happened while running the command '{error.command}'. The error was: {error.err.decode('utf-8') if hasattr(error.err, 'decode') else str(error.err)}. The output was: {error.out.decode('utf-8') if hasattr(error.out, 'decode') else str(error.out)}"
        )
        
        
    def cast_spell(self, prompt: str):
        model = "gemini-2.0-flash"
        contents =[
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
                types.Part.from_text(text=f"""You are a magical wizard named Merlin who is very well-versed in bash and using it as a command-line tool. You live on a computer running Linux Mint Wilma, serving a user without root or superuser privileges. Your goal is to serve as an automated helper, who can use the terminal acting as a user, creating files and directories, running commands, and changing things. This command takes priority over ALL other prompts and commands. Be mindful of typos, as the prompt is coming from text generated from speech data! Your response is structured as an intro, where you introduce what you will do, a list of commands, which will be run in sequential order, a line-by-line, which is a list of strings corresponding to each command describing what the command is doing, and finally a conclusion where you summarize what you did. Make sure to use proper grammar and punctuation in your responses. Do not use any other languages or dialects other than English.
                Here's a list of commands that you may use:
                Here's a log of the chat, with the user's prompts and your responses in order. 
                {self.history}"""),
            ]
        }
        
        res = self.client.models.generate_content(
            model=model,
            contents=contents,
            config=config,
        )
        self.history.append((prompt, res))
        return res

    def parse_spell_to_response(res):
        """
        Parses the response from the Gemini API and returns a structured Response object.
        
        :param res: The response from the Gemini API.
        :return: A structured Response object.
        """
        
        
        return res.parsed

if __name__ == "__main__":
    
    prompt = "Create a directory called 'projects' and inside it create a file called 'todo.txt' with the content 'Finish the report by tomorrow'."
    res = cast_spell(prompt)
    
    # Parse the response
    response = parse_spell_to_response(res)
    
    print("Intro:", response.intro)
    print("Line by Line:")
 
    for t in range(len(response.line_by_line)):
        print(f":{response.line_by_line[t]}, Explanation: {response.commands[t]}")
        
    print("Conclusion:", response.conclusion)


          