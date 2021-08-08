from report import CaseReport
from mongodb.db import DB

def process_posts_from_database():
    print("Launching Persephone Alert System")
    db = DB().connect_db()
    print("Downloading Anonme Revenge Porn website posts for analysis...")
    print("Processing posts logged in database since last scrape.")

    for location in db.list_collection_names():
        for thread in db[location].find():
            CaseReport(thread, db).process_thread()

if __name__ == "__main__":
    process_posts_from_database()