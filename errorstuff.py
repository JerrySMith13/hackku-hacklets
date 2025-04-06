class Err:
    def __init__(self, command, err, out):
        self.command = command
        self.err = err
        self.out = out
        
class LogCommandOutput:
    """
    _summary_
        Internal object used for logging command history with Merlin

    """
    def __init__(self, prompt_response_conclusion: (str, str, str), command_history: list[tuple[str, str]]):
        self.prompt = prompt_response_conclusion[0]
        self.intro = prompt_response_conclusion[1]
        self.conclusion = prompt_response_conclusion[2]
        self.command_history = command_history