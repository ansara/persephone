import io
from dataclasses import dataclass

import PIL.Image as Image


@dataclass(frozen=True)
class PostRawData:
    post_type: str
    id: str
    url: str
    date_posted: str
    thread_subject: str
    text: str
    photos: list
    parent_post_text: str
    parent_post_id: str

    def get_text_evidence(self) -> str:
        photos = self.photos
        text = [self.thread_subject, self.text, self.parent_post_text]
        if isinstance(photos, dict):
            text.append(self.photos["image_title"])
        else:
            titles = [sub["image_title"] for sub in self.photos]
            text = text + titles

        evidence = " ".join(list(filter(None, text)))
        print(f"Raw Text Evidence: '{evidence}'")
        return str(evidence)

    @classmethod
    def from_parent(cls, post):
        return PostRawData(
            post_type="Parent",
            id=post.get("original_post_id"),
            url=post.get("url"),
            date_posted=post.get("original_post_date"),
            thread_subject=post.get("subject"),
            text=post.get("original_post_text"),
            photos=post.get("original_post_image_info"),
            parent_post_text=None,
            parent_post_id=None,
        )

    @classmethod
    def from_comment(cls, comment, parent):
        return PostRawData(
            post_type="Comment",
            id=comment.get("comment_id"),
            url=comment.get("comment_link"),
            date_posted=comment.get("date"),
            thread_subject=parent.get("subject"),
            text=comment.get("text"),
            photos=comment.get("image_info"),
            parent_post_text=parent.get("original_post_text"),
            parent_post_id=parent.get("original_post_id"),
        )

    def get_photo_jpgs(self):
        print("Getting photos as jpegs")
        jpgs = []

        if isinstance(self.photos, dict):
            raw = self.photos["image_data"]
            jpgs.append(Image.open(io.BytesIO(raw)))
        else:
            photos_raw = [sub["image_data"] for sub in self.photos]
            for raw in photos_raw:
                jpg = Image.open(io.BytesIO(raw))
                jpgs.append(jpg)

        return jpgs
