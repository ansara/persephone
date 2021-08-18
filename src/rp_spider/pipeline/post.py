from dataclasses import dataclass

#TODO: region_context
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
    location: str


    def get_text_evidence(self) -> str:
        photos = self.photos
        text = [self.thread_subject, self.text, self.parent_post_text]
        if isinstance(photos, dict):
            text.append(self.photos["image_title"])
        else:
            titles = [sub["image_title"] for sub in self.photos]
            text = text + titles

        evidence = (" ".join(list(filter(None, text))), self.location)
        print(f"Raw Text Evidence: '{evidence}'")
        return evidence

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
            location = post.get("location"),
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
            location = parent.get("location"),
            text=comment.get("text"),
            photos=comment.get("image_info"),
            parent_post_text=parent.get("original_post_text"),
            parent_post_id=parent.get("original_post_id"),
        )