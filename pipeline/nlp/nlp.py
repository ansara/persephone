from nltk.tag.stanford import StanfordNERTagger
import nltk
from nltk import PorterStemmer, word_tokenize
from nltk import tag
from nltk.corpus import stopwords
import logging

logging.basicConfig(filename="nlp_log.txt", level=logging.ERROR)

from .dictionaries import *

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)

ENGLISH_STOPWORDS = set(stopwords.words("english"))

LOCATION_STOPWORDS = ['city', 'town', 'province', 'state']

# TODO: lemenization, fix get_location --> subject, documentation, states and international capability, mongodb aws
class NLP:
    def __init__(self):
        self.ner = StanfordNERTagger(
            "/home/adam/persephone/pipeline/nlp/english.muc.7class.caseless.distsim.crf.ser.gz",
            "/home/adam/persephone/pipeline/nlp/stanford-ner.jar",
        )

    # stem, tokenize, etc. then plug into process

    '''
    @context --> dictionary that holds region_data of the thread amoung other things
    '''
    def analyze(self, text, thread_region):
        names, other_identifiers, locations = [], [], []

        # replace slang characters --> SLANG_DICT
        text = self.sanitize_words(text.lower().split()) #capitalization is so inconsistant that its best to just ignore it
        text = word_tokenize(text)  # break into list of words

        #model will more accurately identify names without stopwords, but we will still reference text for context
        text_no_stopwords = self.remove_stopwords(text) 
        tagged_entities = self.ner.tag(text_no_stopwords)
        tagged_entities.append(('', 'O')) #needed so that the final word is processed properly

        #trying to match entity classifications with adjacent words in comment:
        comment_list = zip(tagged_entities, tagged_entities[1:])

        for word, next_word in comment_list:

            try:
                # if next word is the same classification of given word, and they are adjacent then pair them together
                if (next_word[0]!='' and next_word[1] == word[1] and text.index(word[0]) == text.index(next_word[0])-1):
                    if word[1] == 'PERSON':
                        names.append((word[0], next_word[0]))
                    elif word[1] == 'LOCATION' and next_word[0] not in LOCATION_STOPWORDS: #ignore words such as "city" or "town" when combining location entities
                        locations.append((word[0], next_word[0]))

                #if word starts comment, previous word is a stopword, or previous entity is a different classification
                elif (tagged_entities.index(word) == 0) or text[text.index(word[0])-1] in ENGLISH_STOPWORDS or tagged_entities[tagged_entities.index(word)-1][1] != word[1]:
                    if word[1] == 'PERSON':
                        names.append(word[0])
                    elif word[1] == "LOCATION" and word[1] not in LOCATION_STOPWORDS:
                        locations.append(word[0])
            except Exception as e:
                logging.error(f'Error processing names: {e}')

            if word[1] != 'O' and word[1]!='PERSON' and word[1]!='LOCATION':
                other_identifiers.append(word)

        # additionally check list of female names for match
        for word in text_no_stopwords:
            if word in FEMALE_NAME_LIST:
                names.append(word)

        # pair initials with names --> 
        for name in names:
            
            # only a single name --> no initals or fullname
            if len(name) == 1:

                # see if previous or next word is a single character
                try:
                    adjacent_word = text[text.index(name[0]) + 1]

                    if len(adjacent_word) == 1:
                        names.append(name + " " + adjacent_word.upper() + ".")
                except Exception as e:
                    logging.error(f'Error when matching name initial to adjacent character: {e}')

                try:
                    previous_word = text[text.index(name[0]) - 1]

                    if len(previous_word) == 1:
                        names.append(previous_word.upper() + ". " + name)

                except Exception as e:
                    logging.error(f'Error when matching name initial to previous character: {e}')

        # Advanced location analysis is currently only available for Canada
        # get_locations will try to identify specific Canadian cities and provinces mentioned in threads
        # locations from  non-Canadian threads are exclusively analyzed with nlp model

        if thread_region == 'Canada':

            #try to find matches in text
            locations.extend(self.get_locations(text_no_stopwords))


        # unique values only
        names = list(set(names))
        locations = list(set(locations))

        flags = self.determine_flags(text)

        return {
            "names": names,
            "locations": locations,
            "other_identifiers": other_identifiers,
            "flags": flags,
        }

    # translate slang characters
    def sanitize_words(self, text_list):

        # translate slang
        for word in text_list:
            temp_word = word
            if temp_word[-1] == "1":
                temp_word = temp_word[:-1] + "one"

            for slang_character in SLANG_DICT:
                temp_word = temp_word.replace(
                    slang_character, SLANG_DICT[slang_character])

            text_list[text_list.index(word)] = temp_word

        text_list = " ".join(text_list)
        return text_list

    def remove_stopwords(self, text_list):

        filtered_text = []
        for word in text_list:

            # want to keep single characters because they are often used as initials
            if word not in ENGLISH_STOPWORDS or len(word) == 1:
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

        flags = {"professional": False,
                 "social_media": False, "keywords_found": []}

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

    '''Currently only Canadian cities'''
    def get_locations(self, text):

        locations = []

        # check if word matches any province_dict
        for word in text:
            word = word.lstrip()
            if len(word) >= 2:
                for prov_short in PROV_DICT.keys():
                    if prov_short.lower().startswith(word):
                        locations.append(PROV_DICT[prov_short].lower())
                        
            if len(word) >= 4:
                for prov_name in PROV_DICT.values():
                    if prov_name.lower().startswith(word):
                        locations.append(prov_name.lower())


            # check for partial match with Canadian cities
            try:
                if len(word) >= 6:
                    with open("./pipeline/nlp/canadian_cities.txt") as f:
                        for line in f:
                            line = line.lower().split(',')
                            city, prov = line[0].strip(), line[1].strip()

                            if city.startswith(word):
                                locations.append((city, prov))
            except Exception as e:
                logging.error(f'Error processing Canadian cities text file: {e}')

        return locations