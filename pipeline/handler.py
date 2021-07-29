from mongodb.db import connect_db
from report import CaseReport

def process_thread(thread):
    # print(f"Generating Case Report for Thread: {thread.id}")
    CaseReport(thread).process_thread()

def process_posts_from_database():
    print("Launching Persephone Alert System")
    db = connect_db()
    print("Downloading Anonme Revenge Porn website posts for analysis...")
    print("Processing posts logged in database since last scrape.")

    for location in db.list_collection_names():
        for thread in db[location].find():
            process_thread(thread)

if __name__ == "__main__":
    process_posts_from_database()