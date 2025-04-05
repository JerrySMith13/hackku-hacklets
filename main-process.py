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
    
    run = exec.run_response(res)
    while run[0] != exec.RunSignal.EXIT_SUCCESSFUL:
        if run[0] == exec.RunSignal.FIX_ERR_WITH_MERLIN:
            # Handle the error with Merlin
            err = run[1]
            res = wizard.handle_err(err)
            res = merlin.MerlinClient.parse_spell_to_response(res)
            run = exec.run_response(res)
        elif run[0] == exec.RunSignal.EXIT_ABORTED:
            print("Execution aborted by user.")
            return
        else:
            print("An unknown error occurred.")
            return
    
    
    
    
    
   
    
    
    
    
if __name__ == "__main__":
    main()