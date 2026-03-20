from flask import Flask, render_template, request, redirect
import yaml
import time
import os

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
	with open("static/list.yaml", "r") as f:
		menu_data = yaml.load(f, Loader=yaml.FullLoader)
	return render_template("home.html", menu_data=menu_data)

@app.route("/submit", methods=["POST"])
def submit():
    # request.form.to_dict().keys() gives you the 'name' attributes of the checked boxes
    data = request.form
    selected_items = list(data.to_dict().keys())
    
    # Ensure the directory exists
    os.makedirs("order", exist_ok=True)
    
    file_path = f"order/{int(time.time())}.yaml"
    
    # Open with utf-8 encoding to support Vietnamese characters
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(
            selected_items, 
            f, 
            allow_unicode=True,  # This prevents the \uXXXX escaping
            default_flow_style=False, # This puts items on new lines (cleaner)
            sort_keys=False
        )
        
    return redirect("/thankyou")

@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

if __name__ == '__main__':
	app.run(debug=True)
