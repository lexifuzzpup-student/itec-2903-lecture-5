from flask import Flask, render_template, request, send_from_directory
import os
import uuid
import db

# create the app, labeled using the current filename
app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "user_feedback_images"

# define webpage route and callback
@app.route("/")
def homepage():
    return render_template("feedback_form.html")

# define /submit_feedback POST route
@app.route("/submit_feedback", methods = [ "POST" ])
def submit_feedback():
    feedback = request.form.to_dict()
    print(feedback)

    image_file = request.files["image"]
    if image_file.filename:
        # generate a uuid so the file always has a unique name
        save_filename = f"{uuid.uuid4()}_{image_file.filename}"
        save_location = os.path.join(app.config["UPLOAD_FOLDER"], save_filename)

        # read the file from the request and save it to disk
        print("Saving file to " + save_location)
        image_file.save(save_location)
        feedback["image_path"] = save_filename

    # save raw feedback to database
    db.save_feedback(feedback)

    return render_template("thank_you.html")

@app.route("/admin")
def admin_page():
    # get all feedback (or empty list if none exists)
    feedbacks = db.get_all_feedback() or []

    return render_template(
        "admin.html",
        feedback_count = len(feedbacks),
        feedbacks = feedbacks,
        user_image_location = app.config["UPLOAD_FOLDER"]
    )

@app.route("/" + app.config["UPLOAD_FOLDER"] + "/<image_name>")
def get_image(image_name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], image_name)

# run the server if the file is directly executed
if __name__ == "__main__":
    app.run(debug = True)