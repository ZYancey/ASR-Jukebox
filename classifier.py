import osascript
import spacy
from IPython.lib.pretty import pprint

from player import play, pause, previous, next, queue, like, toggle_repeat

nlp = spacy.load("en_core_web_lg")
doc = nlp(u"This is a sentence.")

phrases = {
    'START': [
        'play',
        'start',
        'begin playback',
        'start playing',
        'play music',
        'play something',
        'play anything',
        'start music',
        'play music',
        'press play',
    ],
    'STOP': [
        'stop',
        'pause',
        'quit',
        'exit',
        'break',
        'stop now',
        'press pause',
    ],
    'START_SPECIFIC': [
        'play something by',
        'play music by',
        'play a track by',
        'play songs by',
    ],
    'SEARCH': [
        'search',
        'queue',
        'search for',
    ],
    'LIKE': [
        'like',
        'heart',
        'favorite',
        'save',
        'press heart',
    ],
    'LOOP': [
        'loop',
        'repeat',
        'press loop',
    ],
    'PREV': [
        'backtrack',
        'rewind',
        'return',
        'revisit',
        'go back',
        'step back',
        'reverse',
        'retreat',
        'retrogress',
        'backpedal',
    ],
    'FFWD': [
        'advance',
        'skip',
        'skip ahead',
        'move forward',
        'jump ahead',
        'next',
        'next song',
        'go forward',
    ],
    'VOLUME_UP': [
        'increase volume',
        'turn it up',
        'make it louder',
        'boost volume',
        'raise the volume',
        'amplify',
        'crank it up',
        'pump up the volume',
        'maximize volume',
        'increase the sound'
    ],
    'VOLUME_DOWN': [
        'decrease volume',
        'turn it down',
        'make it quieter',
        'reduce volume',
        'lower the volume',
        'diminish volume',
        'quieten it down',
        'tone it down',
        'mute it',
        'minimize volume',
    ], }


def detectIntent(text):
    score = {'START': [],
             'STOP': [],
             'START_SPECIFIC': [],
             'SEARCH': [],
             'LIKE': [],
             'LOOP': [],
             'PREV': [],
             'FFWD': [],
             'VOLUME_UP': [],
             'VOLUME_DOWN': []}

    for intent in score:
        for phrase in phrases[intent]:
            sim = calculate_similarity(process_text(text), process_text(phrase))
            score[intent].append(sim)

    avg_score = {}
    for intent in score:
        num_ones = score[intent].count(1.0)
        weighted_sum = sum(score[intent]) + (num_ones * 5 if intent == 'FFWD' else num_ones * 3)
        weighted_count = len(score[intent]) + (num_ones * 1)
        avg_score[intent] = weighted_sum / weighted_count if weighted_count > 0 else 0

    pprint(avg_score)

    if max(avg_score.values()) > 0.5:
        detectedIntent = max(avg_score, key=avg_score.get)
    else:
        return 'NONE', 0
    return detectedIntent, avg_score[detectedIntent]


def process_text(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        result.append(token.lemma_)
    return " ".join(result)


def extract_keywords(text):
    doc = nlp(text.lower())
    keywords = []
    for token in doc:
        if token.pos_ == "NOUN" or token.pos_ == "PROPN" or token.pos_ == "ADJ":
            if token.text != 'songs' \
                    and token.text != 'song' \
                    and token.text != 'search' \
                    and token.text != 'play' \
                    and token.text != 'track' \
                    and token.text != 'music':
                keywords.append(token.text)
                print("Adding '" + token.text + "' to search String")
    return keywords


def calculate_similarity(text1, text2):
    base = nlp(process_text(text1))
    compare = nlp(text2)
    return base.similarity(compare)


def respond(text):
    print(text)
    detectedIntent, confidence = detectIntent(text)

    if detectedIntent == 'START_SPECIFIC':
        queue(" ".join(extract_keywords(text)), 1)
        next()
    if detectedIntent == 'SEARCH':
        queue(" ".join(extract_keywords(text)), 3)
        next()
    if detectedIntent == 'START':
        play()
    if detectedIntent == 'STOP':
        pause()
    if detectedIntent == 'LIKE':
        like()
    if detectedIntent == 'LOOP':
        toggle_repeat()
    if detectedIntent == 'PREV':
        previous()
    if detectedIntent == 'FFWD':
        next()
    if detectedIntent == 'VOLUME_UP':
        osascript.osascript("set volume output volume 60")
    if detectedIntent == 'VOLUME_DOWN':
        osascript.osascript("set volume output volume 20")

    if detectedIntent == 'NONE':
        return "Command Not Recognized!"

    return detectedIntent + ' | ' + str(round(confidence, 2))
