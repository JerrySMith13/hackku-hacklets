import tkinter as tk
from PIL import Image, ImageTk  # Ensure you have the Pillow library installed
import subprocess  # Import subprocess to run external scripts

# Flag to prevent resizing during button animation
is_animating = False

def run_main_process():
    """Run the main-process.py script in a non-blocking manner."""
    subprocess.Popen(["python3", "hackku-hacklets/main-process.py"])
    #############################################################################################
    #oldText = NONE
    #newText = NONE
    #text_label = tk.Label(root, text=newText, font=("Arial", 12), fg="black", bg="lightgray")
    #clear = tk.Label(root, text=NONE, font=("Arial", 12), fg="black", bg="lightgray")
    #while True:
    #    try:
    #        newText = read_file()
    #        if newText != oldText:
    #            clear.place(x=100, y=50)  # Adjust position as needed
    #            text_label.place(x=100, y=50)  # Adjust position as needed
    #            oldText = newText
    #    except EOFError:
    #        break
    #############################################################################################
        
def bounce_button(canvas_item):
    """Create a bounce effect for the button."""
    global is_animating
    is_animating = True  # Set the flag to prevent resizing

    # Move the canvas item down slightly
    canvas.move(canvas_item, 0, 5)
    canvas.after(100, lambda: canvas.move(canvas_item, 0, -5))  # Move it back after 100ms
    canvas.after(150, lambda: set_animation_flag(False))  # Reset the flag after the animation

def set_animation_flag(value):
    """Set the animation flag to the given value."""
    global is_animating
    is_animating = value

def run_main_process_with_bounce():
    """Make the circular button bounce and then run the main process."""
    bounce_button(button_image_item)  # Pass the button image item
    root.after(150, run_main_process)  # Delay running the process slightly to allow the bounce animation

def resize_background(event):
    """Resize the background image to fit the window only if the size has changed."""
    global last_width, last_height, is_animating

    # Skip resizing if the animation is in progress
    if is_animating:
        return

    # Check if the window size has actually changed
    if event.width == last_width and event.height == last_height:
        return  # Do nothing if the size hasn't changed

    last_width, last_height = event.width, event.height
    new_width = event.width
    new_height = event.height  # Leave space for the button
    resized_image = original_image.resize((new_width, new_height))
    new_background_image = ImageTk.PhotoImage(resized_image)
    canvas.itemconfig(background_item, image=new_background_image)
    canvas.background_image = new_background_image  # Keep a reference to avoid garbage collection

def open_preconditions():
    """Open the preconditions.txt file."""
    try:
        subprocess.Popen(["open", "hackku-hacklets/precondition.txt"])  # macOS-specific command
    except Exception as e:
        print(f"Error opening precondition.txt: {e}")

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Spell Book")
root.geometry("400x600")
root.resizable(False, False)  # Lock the window size

# Set the app icon to spellbookBG.png
icon_image = ImageTk.PhotoImage(Image.open("hackku-hacklets/merlin-ui/spellbookIcon.png"))
root.iconphoto(False, icon_image)

# Load the background image once
original_image = Image.open("hackku-hacklets/merlin-ui/spellbookBG.png")
background_image = ImageTk.PhotoImage(original_image)

# Resize the button image to make the label smaller
resized_button_image = Image.open("hackku-hacklets/merlin-ui/merlinButton.png").resize((200, 120))  # Adjust size as needed
buttonImage = ImageTk.PhotoImage(resized_button_image)

# Precondition Button
resized_prec_image = Image.open("hackku-hacklets/merlin-ui/preconditionImage.png").resize((100, 60))  # Adjust size as needed
precImage = ImageTk.PhotoImage(resized_prec_image)

# Add a frame to separate the canvas and the button
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

# Create a Canvas widget inside the frame
canvas = tk.Canvas(frame)
canvas.pack(fill="both", expand=True)

# Add the background image to the Canvas
background_item = canvas.create_image(0, 0, anchor="nw", image=background_image)
canvas.background_image = background_image  # Keep a reference to avoid garbage collection

# Replace the label with a circular button on the canvas

# Add a circular button to the canvas
circle_button = canvas.create_oval(
    100, 440, 300, 560,  # Coordinates for the oval (x1, y1, x2, y2)
    fill="",  # Background color (transparent if empty)
    outline="",  # Border color (transparent if empty)
)

# Add the button image inside the circle
button_image_item = canvas.create_image(
    200, 500,  # Center of the circle
    image=buttonImage,
)

# Bind the circular button to the same command as the label
canvas.tag_bind(circle_button, "<Button-1>", lambda event: run_main_process_with_bounce())
canvas.tag_bind(button_image_item, "<Button-1>", lambda event: run_main_process_with_bounce())

# Replace the button at the top-left corner with a label using preconditionImage.png
preconditions_label = tk.Label(
    root,
    image=precImage,  # Use the precondition image
    bg="lightgray"  # Background color
)
preconditions_label.place(x=20, y=20)  # Position the label at the top-left corner

# Bind the label to open the preconditions.txt file on click
preconditions_label.bind("<Button-1>", lambda event: open_preconditions())

# Track the last known window size
last_width, last_height = 400, 600

# Bind the resize event to dynamically resize the background
root.bind("<Configure>", resize_background)

# Start the Tkinter main loop
root.mainloop()