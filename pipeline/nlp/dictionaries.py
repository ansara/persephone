
name_file = open('./pipeline/nlp/female_names.txt', 'r')
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
    "AB": "Alberta",
    "BC": "British Columbia",
    "MB": "Manitoba",
    "NB": "New Brunswick",
    "NL": "Newfoundland and Labrador",
    "NS": "Nova Scotia",
    "NT": "Northwest Territories",
    "NUN": "Nunavut",
    "ONT": "Ontario",
    "PEI": "Prince Edward Island",
    "QC": "Quebec",
    "SK": "Saskatchewan",
    "YT": "Yukon",
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
