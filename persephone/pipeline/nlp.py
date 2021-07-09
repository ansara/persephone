import nltk
from nltk import PorterStemmer, word_tokenize
from nltk.corpus import stopwords

nltk.download("punkt", download_dir="../project/data/nltk", quiet=True)
nltk.download("stopwords", download_dir="../project/data/nltk", quiet=True)
nltk.download("averaged_perceptron_tagger", download_dir="../project/data/nltk", quiet=True)

from nltk.tag.stanford import StanfordNERTagger


SLANG_DICT = {
    "a": "4",
    "b": "8",
    "e": "3",
    "g": "6",
    "i": "1",
    "o": "0",
    "t": "7",
    "z": "2",
    "l": "!",
    "s": "$",
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


# TODO: lemenization, Area codes
class NLP:
    def __init__(self):
        self.ner = StanfordNERTagger(
            "../data/english.all.3class.caseless.distsim.crf.ser.gz",
            "../data/stanford-ner.jar",
        )

    # stem, tokenize, etc. then plug into process
    def analyze(self, text, subject=None):

        text = text.lower().split()
        text = self.sanitize_words(text)
        text = word_tokenize(text)

        flags = self.determine_flags(text)

        text = self.remove_stopwords(text)

        tagged_sent = self.ner.tag(text)
        named_entities = self.process(tagged_sent)
        
        named_entities_str_tag = [
            (" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities
        ]

        names = []
        locations = []
        other_identifiers = []
        locations_temp = []

        for item in named_entities_str_tag:
            if item[1] == "PERSON":
                names.append(item[0])
            elif item[1] == "LOCATION":
                locations.append(item[0])
            else:
                other_identifiers.append(item[0])

        # see if we can get city from subject line
        if subject:
            locations_temp = self.get_locations(subject, [], subject=True)

        if locations_temp:
            locations = locations_temp
        else:
            locations = self.get_locations(text, locations)

        # unique vals only
        locations = list(set(locations))
        names = list(set(names))

        # pair initials with names -->
        for name in names:
            temp = name.split()
            if len(temp) > 2:
                for part in range(len(temp)):
                    try:
                        if (
                            len(temp[part]) > 2
                            and len(text[text.index(temp[part]) + 1]) == 1
                        ):
                            names.append(
                                temp[part] + " " + text[text.index(temp[part]) + 1]
                            )

                    except Exception:
                        pass

        return {
            "names": names,
            "locations": locations,
            "other_identifiers": other_identifiers,
            "flags": flags,
        }

    def get_locations(self, text, locations, subject=False):

        if subject:
            try:
                text = text.split(",")
                text[0] = text[0].strip().lower()
                text[1] = text[1].strip().lower()
            except Exception:
                pass

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
                with open("../project/data/canadian_cities.txt") as f:
                    for line in f:
                        if line.split(",")[0].lower().strip().startswith(word):
                            locations.append(line.strip())
        locations = list(set(locations))
        return locations

    """
    Identify keywords that suggest if text is about a professional or social media
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

    def sanitize_words(self, text_list):

        # translate slang
        for word in text_list:
            temp_word = word
            if temp_word[-1] == "1":
                temp_word = temp_word[:-1] + "one"

            for letter in SLANG_DICT:
                temp_word = temp_word.replace(SLANG_DICT[letter], letter)

            text_list[text_list.index(word)] = temp_word

        text_list = " ".join(text_list)
        return text_list

    def remove_stopwords(self, text_list):
        stop_words = set(stopwords.words("english"))

        filtered_text = []
        for word in text_list:
            if word not in stop_words:
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
