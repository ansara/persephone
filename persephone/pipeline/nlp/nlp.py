import nltk
from nltk import PorterStemmer, word_tokenize
from nltk.corpus import stopwords

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)

from nltk.tag.stanford import StanfordNERTagger

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

# keywords found in forums that indicate that given comments are about a professional sex worker
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


# TODO: lemenization, fix get_location --> subject, documentation, states and international capability, mongodb aws
class NLP:
    def __init__(self):
        self.ner = StanfordNERTagger(
            "/home/adam/persephone/persephone/pipeline/nlp/english.all.3class.caseless.distsim.crf.ser.gz",
            "/home/adam/persephone/persephone/pipeline/nlp/stanford-ner.jar",
        )

    # stem, tokenize, etc. then plug into process
    def analyze(self, text, context=None):
        report = {}
        names, other_identifiers, locations_temp, locations = [], [], [], []

        text = text.lower().split()
        text = self.sanitize_words(text) #replace slang characters --> SLANG_DICT
        text_list = word_tokenize(text) #break into list of words --> this was originally after sanitize_words

        text_processed = self.remove_stopwords(text_list)


        tagged_entities = self.ner.tag(text_processed)
        named_entities = self.process(tagged_entities)
        
        named_entities_str_tag = [
            (" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities
        ]

        for item in named_entities_str_tag:
            if item[1] == "PERSON":
                names.append(item[0])
            elif item[1] == "LOCATION":
                locations.append(item[0])
            else:
                other_identifiers.append(item)


        # pair initials with names -->
        for name in names:
            temp = name.split()
            #only a single name --> no initals or fullname
            if len(temp)==1:
                #see if previous or next word is a single character
                try:
                    adjacent_word = text_list[text_list.index(temp[0]) + 1]

                    if len(adjacent_word) == 1:
                        names.append(name + " " + adjacent_word.upper() + ".")
                except Exception:
                    print("ERROR")
                    pass

                try:
                    previous_word = text_list[text_list.index(temp[0]) - 1]
                    
                    if len(previous_word) == 1:
                        names.append(previous_word.upper() + ". " + name)

                except Exception:
                    print("ERROR 1")
                    pass

        #Advanced location analysis is currently only available for Canada 
        #get_locations will try to identify specific Canadian cities and provinces mentioned in threads
        #locations from  non-Canadian threads are exclusively analyzed with nlp model
        if 'general_region' in context:
            
            if context['general_region']=='Canada':
                if 'subject_line' in context:
                    locations.append(self.get_locations(context['subject_line'], subject=True))

                # no match using subject lines, so analyze
                if not locations:
                    locations.append(self.get_locations(text_processed))


        # unique values only
        names = list(set(names))
        locations = list(set(locations))

        flags = self.determine_flags(text_list)

        return {
            "names": names,
            "locations": locations,
            "other_identifiers": other_identifiers,
            "flags": flags,
        }

    #translate slang characters
    def sanitize_words(self, text_list):

        # translate slang
        for word in text_list:
            temp_word = word
            if temp_word[-1] == "1":
                temp_word = temp_word[:-1] + "one"

            for slang_character in SLANG_DICT:
                temp_word = temp_word.replace(slang_character, SLANG_DICT[slang_character])

            text_list[text_list.index(word)] = temp_word

        text_list = " ".join(text_list)
        return text_list

    def remove_stopwords(self, text_list):
        stop_words = set(stopwords.words("english"))

        filtered_text = []
        for word in text_list:
            if word not in stop_words or len(word)==1: #want to keep single characters because they are often used as initials
                filtered_text.append(word)

        return filtered_text

    def process(self, tagged_sent):
        continuous_chunk = []
        current_chunk = []

        for token, tag in tagged_sent:
            if tag != "O":
                current_chunk.append((token, tag))
            else:
                if current_chunk:  # if the current chunk is not empty
                    continuous_chunk.append(current_chunk)
                    current_chunk = []

        # Flush the final current_chunk into the continuous_chunk, if any.
        if current_chunk:
            continuous_chunk.append(current_chunk)
        return continuous_chunk

    """
    Identify keywords that suggest if text is about a professional sex worker or social media --> these comments are not what we are targeting
    """
    def determine_flags(self, text):

        stemmer = PorterStemmer()

        flags = {"professional": False, "social_media": False, "keywords_found": []}

        for word in text:
            word = stemmer.stem(word)
            if word in PROFSSIONAL_KEYWORDS:
                flags["professional"] = True
                flags["keywords_found"].append(word)

            if word in SOCIAL_MEDIA_KEYWORDS:
                flags["social_media"] = True
                flags["keywords_found"].append(word)

        flags["keywords_found"] = list(set(flags["keywords_found"]))

        return flags

    def get_locations(self, text, thread_region, subject=False):

        locations = []

        if subject:
            try:
                text = text.split(",")
                text[0] = text[0].strip().lower()
                text[1] = text[1].strip().lower()
            except Exception:
                print("Formatting error with subject line, skipping")

        # check if word matches any province_dict
        for word in text:
            if len(word) >= 2:
                for prov_short in PROV_DICT.keys():
                    if prov_short.lower().startswith(word):
                        locations.append(PROV_DICT[prov_short])

                for prov_name in PROV_DICT.values():
                    if prov_name.lower().startswith(word):
                        locations.append(prov_name)

            # check for match with Canadian cities
            if len(word) >= 4:
                with open("./canadian_cities.txt") as f:
                    for line in f:
                        if line.split(",")[0].lower().strip().startswith(word):
                            locations.append(line.strip())
        locations = list(set(locations))
        return locations

test = NLP()
test.analyze("HELLO this is a test, I am from Regina Saskatchewan")