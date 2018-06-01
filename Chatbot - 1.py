
# coding: utf-8

# **Adapted from lizadaly/brobot**

# In[1]:


# hash to comment
get_ipython().system('pip install textblob')
import nltk
from nltk.tokenize import word_tokenize
import random


# ### Simple Greetings chatbot

# In[2]:


# Simple Greetings chatbot 
GREETING_KEYWORDS = ("hello", "hi","greetings", "hey" )

GREETING_RESPONSES = ["hi hi", "hey", "good day", "oh, its you" ]

def greeting(sentence):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    #tokenize the sentence 
    sentence = word_tokenize(sentence)
    for word in sentence:
        if word.lower() in GREETING_KEYWORDS:
            #return any random choice from the response
            return random.choice(GREETING_RESPONSES)
        else:
            return 'no comprehendo'


# In[3]:


question = input('say something : ')


# In[4]:


answer = greeting(question)
print (answer)


# ### TextBlob

# In[5]:


# nltk wrapper
from textblob import TextBlob


# In[6]:


question = input('say something : ')


# In[7]:


text = TextBlob(question)


# In[8]:


text.words


# In[9]:


text.words.count('you')


# In[10]:


text.tags


# In[11]:


text[:10]


# ### Pre-processing

# In[12]:


# check spelling
text = text.correct(); text


# In[13]:


# convert to lower case
text = text.lower(); text


# In[14]:


# form back sentence
clean_text = ' '.join(text.words)


# In[15]:


clean_text


# In[16]:


# replace selected words  
clean_text = clean_text.replace('charcot', 'chatbot')
clean_text


# ### Part-of-Speech Extraction

# In[17]:


text = TextBlob(clean_text)


# In[18]:


text_tags = text.tags; text_tags


# In[19]:


# Given a sentence, find the 1st noun
noun = None
for word, pos in text_tags:
    if pos == 'NN':  # NN is short for noun
        noun = word
        break
noun


# In[20]:


# Pick a candidate verb for the sentence
verb = None
partofspeech = None
for word, pos in text_tags:
    #pos refers to Part of Speech
    #VB is short for verbs
    if pos.startswith("VB"):
        verb = word
        partofspeech = pos
        break

verb, partofspeech


# In[21]:


# Given a sentence, find the 1st adjective. Returns None if no candidate found
adjective = None
for word, pos in text_tags:
    if pos == 'JJ':  # This is an adjective
        adjective = word
        break
        
adjective


# In[26]:


# Given a sentence, find the 1st pronoun 
response_pronoun = None
for word, pos in text_tags:
    # Disambiguate pronouns
    if pos == 'PRP' and word == 'you':  
        #if message have you, reply with I
        response_pronoun = 'I'
    elif pos == 'PRP' and word == 'I':
        # If the user mentioned themselves, then they will definitely be the pronoun
        response_pronoun = 'You'

response_pronoun


# ### String Formatting

# In[27]:


noun


# In[28]:


noun.pluralize()


# In[29]:


noun.pluralize().capitalize()


# In[30]:


S = 'I like {noun}'


# In[31]:


SS = S.format(**{'noun': noun}); SS


# ### Check for comment about bot

# In[33]:


"""Check if the user's input was about the bot's activities, in which case try to fashion a response
    that feels right based on their input."""

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

# initialise a response
resp = None

if response_pronoun == 'I' and (noun or adjective):
    if noun:
        if random.choice((True,False)):  #random.choice needs a list to choose from
            resp = random.choice(SELF_VERBS_WITH_NOUN_CAPS_PLURAL).format(**{'noun': noun.pluralize().capitalize()})
        else:
            resp = random.choice(SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})
    else:
        resp = random.choice(SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective})


# In[34]:


resp


# ### Comments about self and none response

# In[35]:


# Sentences we'll respond with if we have no idea what the user just said
NONE_RESPONSES = [
    "I have no idea what you've just said",
    "huh ? can you repeat that",
    "please say that again",
    "can you rephrase that ?",
    "I don't understand",
    "Let's talk about something else",
]

# If the user says something about the bot itself, use one of these responses
COMMENTS_ABOUT_SELF = [
    "You may be right",
    "Do you really think so ?",
    "You don't know what you are talking",
    "We find ways to do it",
    "I take that as a compliment"
]


# In[36]:


resp = None


# In[37]:


if not resp:  # i.e. if resp == None
    if not response_pronoun:
        resp = random.choice(NONE_RESPONSES)
    elif response_pronoun == 'I' and verb:
        resp = random.choice(COMMENTS_ABOUT_SELF)
    
# If we got through all that with nothing, use a random response
if not resp:
    resp = random.choice(NONE_RESPONSES)


# In[38]:


resp


# ### Construct own response

# In[39]:


def starts_with_vowel(word):
    """Check for pronoun compability -- 'a' vs. 'an'"""
    return True if word[0] in 'aeiou' else False


# In[44]:


"""No special cases matched, so we're going to try to construct a full sentence that uses as much
    of the user's input as possible"""
resp = []

# place the pronoun first if found
if response_pronoun:
    resp.append(response_pronoun)

    # respond if verb found
    if verb:
        verb_word = verb[0]
        if verb_word in ('be', 'am', 'is', "'m"):  
            if response_pronoun.lower() == 'you':
                # The bot will always tell the person they aren't whatever they said they were
                #if the words are in red, it means indentation is not correct
                resp.append("aren't really")
            else:
                resp.append(verb_word)
                
    # respond if noun found
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

    resp.append(random.choice(("la", "bro", "lol", "bruh", "")))

    resp = " ".join(resp)

# catch all response if nothing match the above
else:
    resp = "yes, let's talk about something else"


# In[45]:


resp

