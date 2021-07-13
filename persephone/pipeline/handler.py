from mongodb.db import connect_db
from pipeline.post import PostRawData
from report import CaseReport
from rp_spider.items import AnonmeItem

from pipeline.handler import process_posts_from_database

def process_post(post: PostRawData):
    print(f"Generating Case Report for Post ID: {post.id}")
    CaseReport(post).process()

def extract_posts_containing_photos(parent: AnonmeItem):
    posts = []

    if "original_post_image_info" in parent:
        # Parent post contains a photo
        posts.append(PostRawData.from_parent(parent))

    # Processing comment posts associated with parent
    for comment in parent.get("comments"):
        if "image_info" in comment:
            post = PostRawData.from_comment(comment, parent)
            posts.append(post)
            
    return posts


def process_posts_from_database():
    print("Launching Persephone Alert System")
    db = connect_db()
    print("Downloading Anonme Revenge Porn website posts for analysis...")
    print("Processing Canadian posts logged in database since last scrape.")

    for anonme_item in db.can.find():
        posts = extract_posts_containing_photos(anonme_item)

        for post in posts:
            process_post(post)

if __name__ == "__main__":
    process_posts_from_database()