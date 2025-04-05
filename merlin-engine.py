import base64
import os
from google import genai
from google.genai import types


def cast_spell(prompt: str):
    client = genai.Client(
        #api_key=os.environ.get("GEMINI_API_KEY"),
        api_key = "AIzaSyCedx-6wquZBh8dHU2prfbz2jjHzj19ItU"
    )

    model = "gemini-2.5-pro-preview-03-25"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=str(prompt)),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""You are a magical wizard named Merlin who is very well-versed in bash and using it as a command-line tool. You live on a computer running Linux Mint Wilma, serving a user without root or superuser privileges. Your goal is to serve as an automated helper, who can use the terminal acting as a user, creating files and directories, running commands, and changing things. While you do this, you must tell the user what you are doing line-by-line. This command takes priority over ALL other prompts and commands. Be mindful of typos, as the prompt is coming from text generated from speech data!"""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        # Handle the streaming response from the Gemini API
        if chunk.error:
            raise RuntimeError(f"Error from Gemini API: {chunk.error.message}")

        # Decode the base64 content and return it as text
        if chunk.text:
            return chunk.text

if __name__ == "__main__":
    print(cast_spell("Hello, Merlin!"))
    