from datetime import datetime

import pdf
import profiler
from nlp import NLP
from pipeline.db import connect_db
from pipeline.post import PostRawData


class CaseReport:
    post: PostRawData
    date_processed: datetime
    inferences: dict  # Case details extracted using NLP
    leads: list  # Potential victims

    def __init__(self, post: PostRawData):
        self.post = post
        self.date_processed = datetime.now()
        self.inferences = {}
        self.leads = []

    def process(self):
        text_evidence = self.post.get_text_evidence()
        try:
            self.inferences = NLP().analyze(text_evidence, self.post.thread_subject)
            print(f"NLP Analysis: {self.inferences}")
        except Exception:
            print("NLP meta-analysis failed. Continuing without inferences.")

        photos = self.post.get_photo_jpgs()
        try:
            self.leads = profiler.identify_leads(photos, self.inferences)
        except Exception:
            print("Identity mapping failed. Continuing without leads.")
        self.log()

    def save_as_pdf(self):
        try:
            pdf.generate_pdf(self)
        except Exception:
            pass

    def log(self):
        print("Case Report complete. Submitting case for review.")
        self.upload_to_db()

        self.save_as_pdf()

    def upload_to_db(self):
        print(f"Uploading Case Report to database. CaseReport ID: {self.post.id}")
        db = connect_db()
        try:
            print("Database connected.")
            db.case_reports.insert(self)
        except Exception:
            pass
