from mongodb.db import connect_db
from nlp.nlp import NLP

class CaseReport:
    def __init__(self, thread: dict):
        self.thread = thread
        self.report = {}

        #test item
        self.thread = {'comments': [{'id': '22', 'text': 'My name is Carrol and this is Mark'}],
        'date_of_last_scrape': '2021-07-29T01:19:45.933490+00:00',
        'location': 'Kentucky',
        'original_post_date': '2021-07-22T11:21:08Z',
        'original_post_id': '183',
        'original_post_image': {'image_title': 'E1380FDE-4062-4CF7-BFA1-1….jpeg',
                                'image_url': 'https://anonposted.com/ken/src/1626952868362.jpeg'},
        'original_post_text': 'We’re is all the Jackson hos at',
        'subject': 'Were all the Jackson hos at ',
        'url': 'https://anonposted.com/ken/res/183.html'}

    def process_thread(self):
        try:
            comment_inferences, aggregate_names = [], []

            #analyze the original post and subject line

            original_post_text = self.thread['original_post_text']

            if 'subject' in self.thread:
                original_post_text = self.thread['subject'] +' ' + original_post_text

            comment_inferences.append({
                'comment_id': self.thread['original_post_id'],
                'inferences': NLP().analyze(original_post_text, self.thread['location'])
            })

            for comment in self.thread['comments']:
                comment_inferences.append({
                    'comment_id': comment['id'],
                    'inferences': NLP().analyze(comment['text'], self.thread['location']),
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
            }

            import pdb; pdb.set_trace()
            self.upload_to_db()

        except Exception:
            print("NLP meta-analysis failed")
            import pdb; pdb.set_trace()

    def upload_to_db(self):
        print(f"Uploading Case Report to database. CaseReport ID: {self.thread['original_post_id']}")
        db = connect_db()
        try:
            print("Database connected.")
            db['reports'].insert(self.report)
        except Exception:
            print("Error inserting report into database.")
