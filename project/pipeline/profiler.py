import subprocess

details = ["name", "email", "phone_number", "location", "photo"]


def identify_leads(photos, inferences):
    for index, photo in enumerate(photos):
        photo.save(f"../data/case_photos/image_{index}.jpg")

    cmd = "python3 social_mapper.py -f imagefolder -i '../data/case_photos/' -m fast -li -ig -fb"
    subprocess.call(cmd)
    return []
