
# coding: utf-8

# In[1]:


import nltk
from nltk.tokenize import word_tokenize
import random
from textblob import TextBlob


# In[2]:


GREETING_KEYWORDS = ("hello", "hi", "greetings", "hey", "whazzup")

GREETING_RESPONSES = ["hi hi", "hey", "*nods*", "good day", "oh, its you", "you talking to me ?"]


# In[3]:


def greeting(sentence):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    sentence = word_tokenize(sentence)
    for word in sentence:
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETING_RESPONSES)
        else:
            return None


# In[4]:


def preprocess(text):
    text = text.correct()
    # text = text.lower()
    clean_text = ' '.join(text.words)
    clean_text = clean_text.replace('charcot', 'chatbot')
    return clean_text


# In[5]:


def find_noun(text_tags):
    noun = None
    for word, pos in text_tags:
        if pos == 'NN':  # NN is short for noun
            noun = word
            break
    return noun    


# In[6]:


def find_verb(text_tags):
    verb = None
    partofspeech = None
    for word, pos in text_tags:
        if pos.startswith('VB'):  # any form of verb
            verb = word
            partofspeech = pos
            break

    return verb, partofspeech


# In[7]:


def find_adjective(text_tags):
    adjective = None
    for word, pos in text_tags:
        if pos == 'JJ':  # This is an adjective
            adjective = word
            break

    return adjective


# In[8]:


def find_response_pronoun(text_tags):
    response_pronoun = None
    for word, pos in text_tags:
        # Disambiguate pronouns
        if pos == 'PRP' and (word == 'you' or word == 'You'):
            response_pronoun = 'I'
        elif pos == 'PRP' and word == 'I':
            # If the user mentioned themselves, then they will definitely be the pronoun
            response_pronoun = 'You'
        elif pos == 'PRP':
            response_pronoun = word

    return response_pronoun


# In[9]:


SELF_VERBS_WITH_NOUN_CAPS_PLURAL = [
    "My last startup totally crushed the {noun} vertical",
    "Were you aware I was a serial entrepreneur in the {noun} sector?",
    "My startup is Uber for {noun}",
    "I really consider myself an expert on {noun}",
]

SELF_VERBS_WITH_NOUN_LOWER = [
    "Yeah and I know a lot about {noun}",
    "My friends always ask me about {noun}",
]

SELF_VERBS_WITH_ADJECTIVE = [
    "I'm personally building the {adjective} Economy",
    "I consider myself to be a {adjective}preneur",
]


# In[10]:


def starts_with_vowel(word):
    """Check for pronoun compability -- 'a' vs. 'an'"""
    return True if word[0] in 'aeiou' else False


# In[11]:


NONE_RESPONSES = [
    "I have no idea what you've just said",
    "huh ? can you repeat that",
    "please say that again",
    "can you rephrase that ?",
    "I don't understand",
    "Let's talk about something else",
]

COMMENTS_ABOUT_SELF = [
    "You may be right",
    "Do you really think so ?",
    "You don't know what you are talking",
    "We find ways to do it",
    "I take that as a compliment"
]


# In[12]:


def respond(ques):
    
    resp = greeting(ques)
    
    # return greeting response if ques is greeting
    if resp:
        return resp
    
    # if not greeting, then determine a suitable response
    if not resp:
        # preprocess question
        text = TextBlob(ques)
        clean_text = preprocess(text)
        
        # find parts of speech
        text = TextBlob(clean_text)
        text_tags = text.tags
        
        noun = find_noun(text_tags)
        verb = find_verb(text_tags)
        adjective = find_adjective(text_tags)
        response_pronoun = find_response_pronoun(text_tags)
        
        # comments about bot
        if response_pronoun == 'I' and (noun or adjective):
            if noun:
                if random.choice((True, False)):
                    resp = random.choice(SELF_VERBS_WITH_NOUN_CAPS_PLURAL).format(**{'noun': noun.pluralize().capitalize()})
                    return resp
                else:
                    resp = random.choice(SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})
                    return resp
            else:
                resp = random.choice(SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective}) 
                return resp
        
        # comments about self
        if response_pronoun == 'I' and verb:
            resp = random.choice(COMMENTS_ABOUT_SELF)
            return resp

        # construct own response
        resp = []

        if response_pronoun:
            resp.append(response_pronoun)

            if verb:
                verb_word = verb[0]
                if verb_word in ('be', 'am', 'is', "'m"):  
                    if response_pronoun.lower() == 'you':
                        resp.append("aren't really")
                        return " ".join(resp)
                    else:
                        resp.append(verb_word)
                        return " ".join(resp)
                    
            if noun:
                if response_pronoun.lower() == "i":
                    prop_noun = "am"
                elif response_pronoun.lower() == "you":
                    prop_noun = "are" 
                elif response_pronoun.lower in ("he", "she", "it"):
                    prop_noun = "is" 
                elif response_pronoun.lower in ("they", "we"):
                    prop_noun = "are"
                else:
                    prop_noun = "is"
                a_or_an = "an" if starts_with_vowel(noun) else "a"
                resp.append(prop_noun + " " + a_or_an + " " + noun)

                # choose a none response if it does not meet any of the crtieria above
            else:
                resp = random.choice(NONE_RESPONSES)
                return resp          

            resp.append(random.choice(("la", "bro", "lol", "bruh", "")))

            resp = " ".join(resp)
        
        else:
            resp = "yes, let's talk about something else"
        
    return resp   


# In[13]:


question = input('say something : ')


# In[14]:


while question != "bye bye":
    answer = respond(question)
    print ('bot : ', answer)
    print ('')
    question = input('say something : ')
    
print ("bot : talk to you soonest !")


# Cell > Run All to run all codes

