import exec
import voice
import merlin
import os
import whisper

def main():
    model = whisper.load_model("base")  # Load the Whisper model
    wizard = merlin.MerlinClient("AIzaSyCcTWxQPbN2tT22e_gogoDjhwlKVXabwnI")
    keepAlive = True
    
    while keepAlive:
        
        transcript = voice.wait_for_silence(model, 2, silence_duration=4)
        
        print(transcript)
        if transcript.strip() == "":
            return
        if wizard.should_keep_alive(transcript) is False:
            print("Ending conversation as per Merlin's suggestion.")
            keepAlive = False
            break
        res = wizard.cast_spell(transcript)
        res = merlin.MerlinClient.parse_spell_to_response(res)
        
        run = exec.run_response(res, wizard, transcript)
        while run[0] != exec.RunSignal.EXIT_SUCCESSFUL:
            if run[0] == exec.RunSignal.FIX_ERR_WITH_MERLIN:
                # Handle the error with Merlin
                err = run[1]
                res = wizard.handle_err(err)
                res = merlin.MerlinClient.parse_spell_to_response(res)
                run = exec.run_response(res, wizard, "This prompt is auto-generated, ignore it")
            elif run[0] == exec.RunSignal.EXIT_ABORTED:
                print("Execution aborted by user.")
                return
            else:
                print("An unknown error occurred.")
                return
        
def main_with_keyboard():
    wizard = merlin.MerlinClient("AIzaSyCcTWxQPbN2tT22e_gogoDjhwlKVXabwnI")
    keepAlive = True
    
    while keepAlive:
        transcript = input("Type your command: ")
        
        if transcript.strip() == "":
            return
        if wizard.should_keep_alive(transcript) is False:
            print("Ending conversation as per Merlin's suggestion.")
            keepAlive = False
            break
        res = wizard.cast_spell(transcript)
        res = merlin.MerlinClient.parse_spell_to_response(res)
        
        run = exec.run_response(res, wizard, transcript)
        while run[0] != exec.RunSignal.EXIT_SUCCESSFUL:
            if run[0] == exec.RunSignal.FIX_ERR_WITH_MERLIN:
                # Handle the error with Merlin
                err = run[1]
                res = wizard.handle_err(err)
                res = merlin.MerlinClient.parse_spell_to_response(res)
                run = exec.run_response(res, wizard, "This prompt is auto-generated, ignore it")
            elif run[0] == exec.RunSignal.EXIT_ABORTED:
                print("Execution aborted by user.")
                return
            else:
                print("An unknown error occurred.")
                return

if __name__ == "__main__":
    main_with_keyboard()