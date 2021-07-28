from datetime import datetime

from nltk import inference
from mongodb.db import connect_db
from nlp.nlp import NLP
from post import PostRawData


class CaseReport:
    post: PostRawData
    inferences: dict  # Case details extracted using NLP
    
    def __init__(self, thread: PostRawData):
        self.thread = thread
        self.report = {}

    def process_thread(self):
        try:
            import pdb; pdb.set_trace()
            text_evidence = self.post.get_text_evidence() #returns text, and region of thread as context
            inferences = NLP().analyze(text_evidence[0], text_evidence[1])
            
            comments = []

            for comment in self.thread['comments']:
                comments.append({
                    'comment_id': comment['id'],
                    'inferences': NLP().analyze(text_evidence[0], text_evidence[1]),
                })
            

            self.report = {
                'thread_id': self.thread.parent_post_id,
                'location': self.thread.location,
                'aggregate_inferences': inferences, #fix this
                'comments' : comments,
            }

            self.upload_to_db()

        except Exception:
            print("NLP meta-analysis failed")


    def upload_to_db(self):
        print(f"Uploading Case Report to database. CaseReport ID: {self.thread.id}")
        db = connect_db()
        try:
            print("Database connected.")
            db.case_reports.insert(self)
        except Exception:
            pass
