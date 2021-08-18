from nlp.nlp import NLP
import datetime

class CaseReport:
    def __init__(self, thread: dict, db_connection):
        self.thread = thread
        self.report = {}
        self.db = db_connection
        self.nlp = NLP()

    def process_thread(self):
        try:
            comment_inferences, aggregate_names = [], []

            #analyze the original post and subject line

            original_post_text = self.thread['original_post_text']

            if 'subject' in self.thread:
                original_post_text = self.thread['subject'] +' ' + original_post_text

            comment_inferences.append({
                'comment_id': self.thread['original_post_id'],
                'inferences': self.nlp.analyze(original_post_text, self.thread['location'])
            })

            for comment in self.thread['comments']:
                comment_inferences.append({
                    'comment_id': comment['id'],
                    'inferences': self.nlp.analyze(comment['text'], self.thread['location']),
                })

            for inference in comment_inferences:
                for name in inference['inferences']['names']:
                    aggregate_names.append(name)

            aggregate_names = list(set(aggregate_names))

            self.report = {
                'thread_id': self.thread['original_post_id'],
                'location': self.thread['location'],
                'aggregate_names': aggregate_names,
                'comment_inferences' : comment_inferences,
                'processing_date': datetime.datetime.now().isoformat(),
            }

            self.upload_to_db()

        except Exception:
            print("NLP meta-analysis failed")
            import pdb; pdb.set_trace()

    def upload_to_db(self):
        print(f"Uploading Case Report to database. CaseReport ID: {self.thread['original_post_id']}")
        try:
            self.db[self.thread['location']]['reports'].insert(self.report)
            print('Successfully inserted item')
        except Exception:
            print("Error inserting report into database.")