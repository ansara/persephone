import subprocess

details = ["name", "email", "phone_number", "location", "photo"]


#TODO: identify leads using facebook api --> https://developers.facebook.com/docs/graph-api/overview
#only search using names and location --> should be able to get public profiles

def identify_leads(inferences):
    cmd = "python3 social_mapper.py -f imagefolder -i '../data/case_photos/' -m fast -li -ig -fb"
    subprocess.call(cmd)
    return []