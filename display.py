import customtkinter
import script
import threading
import json

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("800x150")
app.title("Discord Screenshot Sender")

app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)
app.grid_rowconfigure(1, weight=1)

# Stop Listener Flag
stop_listener_flag = threading.Event()
listener_thread = None
try:
    with open("config.json","r") as f:
        data = json.load(f)
except Exception as e:
    with open("config.json","w") as f:
        default_data = {
            "user":"Enter Your Discord Username Here",
            "webhook":"Enter Your Discord Webhook Here",
            "key":"Key.home"
        }
        json.dump(default_data, f)
        data = default_data

user = data["user"]
webhook = data["webhook"]
desiredKey = data["key"]
        
def read_key(label):
    try:
        with open("config.json","r") as f:
            data = json.load(f)
    except Exception as e:
        with open("config.json","w") as f:
            default_data = {
                "user":"Enter Your Discord Username Here",
                "webhook":"Enter Your Discord Webhook Here",
                "key":"None"
            }
            json.dump(default_data, f)
            data = default_data

    label.configure(text=data["key"])
    label.after(1000,read_key, label)


# Function to start/stop the listener thread
def listen_callback():
    global listener_thread
    listener_thread = None
    if checkbox_var.get() == "on":
        print("Starting Listening...")
        stop_listener_flag.clear()
        if listener_thread is None or not listener_thread.is_alive():
            listener_thread = threading.Thread(target=script.listen, args=(stop_listener_flag,))
            listener_thread.start()
    else:
        print("Stop Listening...")
        stop_listener_flag.set()
        if listener_thread is not None:
            # Join the listener_thread
            listener_thread.join()

def read_callback():
    global read_thread
    read_thread = None
    if read_thread is None or not read_thread.is_alive():
        read_thread = threading.Thread(target=script.select_key, args=(stop_listener_flag,))
        read_thread.start()
    



# Username in Discord Entry
label_username = customtkinter.CTkLabel(app, text="Username in Discord:")
label_username.grid(row=2, column=1, pady=5, padx=5, sticky="nw")
text_username = customtkinter.CTkEntry(master=app, width=450)
text_username.grid(row=2, column=2, pady=5, padx=5, sticky="nw")
text_username.insert("0",user)
button_username = customtkinter.CTkButton(app, text="Submit", command=lambda: json.dump({**json.load(open("config.json")), "user": text_username.get()}, open("config.json", "w")))
button_username.grid(row=2, column=3, pady=5, padx=5, sticky="ne")


# Discord Webhook Entry
label_webhook = customtkinter.CTkLabel(app, text="Discord Webhook:")
label_webhook.grid(row=1, column=1, pady=5, padx=5, sticky="sw")
text_webhook = customtkinter.CTkEntry(master=app, width=450)
text_webhook.grid(row=1, column=2, pady=5, padx=5, sticky="sw")
text_webhook.insert("0",webhook)
button_webhook = customtkinter.CTkButton(app, text="Submit", command=lambda: json.dump({**json.load(open("config.json")), "webhook": text_webhook.get()}, open("config.json", "w")))
button_webhook.grid(row=1, column=3, pady=5, padx=5, sticky="se")



# Listen Checkbox
checkbox_var = customtkinter.StringVar(value="off")
checkbox_listen = customtkinter.CTkCheckBox(master=app, text="Listen", command=listen_callback, variable=checkbox_var, onvalue="on", offvalue="off")
checkbox_listen.grid(row=3, column=1, pady=5, padx=5, sticky="w")

# Listen Checkbox
checkbox_listen2 = customtkinter.CTkButton(master=app, text="select key", command=read_callback)
checkbox_listen2.grid(row=3, column=3, pady=5, padx=5, sticky="e")

label = customtkinter.CTkLabel(app, text=data["key"], fg_color="transparent")
label.grid(row=3, column=2, pady=5, padx=5)
read_key(label)


def on_closing():
    # Stop the listener thread before closing the application
    stop_listener_flag.set()
    if listener_thread is not None:
        listener_thread.join()
    print("Closed")
    app.destroy()

# Bind the function to the window close event
app.protocol("WM_DELETE_WINDOW", on_closing)

print("hello world")
app.mainloop()
