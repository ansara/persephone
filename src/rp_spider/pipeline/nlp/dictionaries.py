
name_file = open('./pipeline/nlp/english_names_female.txt', 'r')
FEMALE_NAME_LIST = [line.strip().lower() for line in name_file.readlines()]

SLANG_DICT = {
    "4": "a",
    "8": "b",
    "3": "e",
    "6": "g",
    "1": "i",
    "0": "o",
    "7": "t",
    "2": "z",
    "!": "l",
    "$": "s",
    "@": "a",
    "*": "",
    "(": "",
    ")": "",
    "#": "",
}

PROV_DICT = {
    "ab": "alberta",
    "bc": "british columbia",
    "mb": "manitoba",
    "nb": "new Brunswick",
    "nl": "newfoundland and labrador",
    "ns": "nova scotia",
    "nt": "northwest territories",
    "nun": "nunavut",
    "ont": "ontario",
    "pei": "prince edward island",
    "qc": "quebec",
    "sk": "saskatchewan",
    "yt": "yukon",
}

# keywords found in forums that indicate that given comments are about a professional sex worker or social media image
PROFSSIONAL_KEYWORDS = [
    "onlyfan",
    "of",
    "porn",
    "pornhub",
    "ph",
    "hub",
    "onlyslut",
    "professional",
    "pro",
    "pornstar",
    "star",
]

# keywords that suggest the given photo is from social media
SOCIAL_MEDIA_KEYWORDS = [
    "instagram",
    "facebook",
    "snapchat",
    "sc",
    "fb",
    "insta",
    "vsco",
    "model",
]