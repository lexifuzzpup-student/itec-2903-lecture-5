import shelve

database_file = "feedbacks.db"
feedback_key = "feedback"

# feedback: { name: string, email: string, description: string, image_info: buffer }
def save_feedback(feedback):
    with shelve.open(database_file) as db:

        # get existing feedback or create new list
        if feedback_key in db:
            feedbacks = db[feedback_key]
        else:
            feedbacks = []

        # append feedback to list
        feedbacks.append(feedback)
        db[feedback_key] = feedbacks

def get_all_feedback():
    with shelve.open(database_file) as db:
        feedbacks = db.get(feedback_key)
    return feedbacks


if __name__ == "__main__":
    print(get_all_feedback())