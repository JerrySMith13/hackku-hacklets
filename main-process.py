import exec
import voice
import merlin
import os
import whisper

def main():
    model = whisper.load_model("base")  # Load the Whisper model
    print("Press CTRL+C to start recording: ")
    
    transcript = voice.wait_for_silence(model, 2)
    print(transcript)
    
    wizard = merlin.MerlinClient("AIzaSyCcTWxQPbN2tT22e_gogoDjhwlKVXabwnI")
    res = wizard.cast_spell(transcript)
    res = merlin.MerlinClient.parse_spell_to_response(res)
    
    print(res.commands)
    print(res.line_by_line)
    
    print(exec.run_response(res))
    
   
    
    
    
    
if __name__ == "__main__":
    main()