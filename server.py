from flask import Flask
import threading
import bot

app = Flask(_name_)

@app.route("/")
def index():
    return "Botul funcționează!"

if _name_ == "_main_":
    threading.Thread(target=bot.main).start()
    app.run(host="0.0.0.0", port=8080)