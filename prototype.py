from random import randint


dateStuff = ["run","cry","fight"]
sleepStuff = ["sleep","dream"]

persons = ["significant other", "boss", "coworker"]
areas   = ["your home", "your workplace", "the streets", "a restaurant"]
objects = ["phone", "wallet", "bag"]

titles = {
        "Cheater" : {
                "You decide to go on Tinder.", 
                "Your casual conversation with your boss turns into a steaming hot talk.",
                "Your casual conversation with your coworker turns into a steaming hot talk.",
                ("You flirt with your boss","You sleep at your workplace"),
                ("You flirt with your coworker", "You sleep at your workplace"),
                "You go on a date with your boss",
                "You go on a date with your coworker"
        },
        "Bum" : {
            "You quit your job.", 
            "You're fired from work",
            "You run to the streets", 
            "You sleep at the streets",
        }
        # "Hero",
        # "Average Joe",
        # "Debbie Downer",
        # "Lucky",
        # "Traveller",
        # "Socialite",
        # "Collector"
}

def gerundOfword(x):
    # Gives the -ing form of a word
    return x[:-1]+(x[-1] if x[-1] != 'e' else '') + (x[-1] if x[-1] == 'n' else '') +"ing"


def parse(words):
    p = 0 # person_count
    a = 0 # area_count
    o = 0 # objectcount

    time = 6
    singles, combos, non_adjacent_combos = setup(p, a, o);
    first_part = set()
    phrases = []
    for i in range(len(words)):
        # Calculate Time
        if (time % 12 == 0):
            current_time = 12
        else:
            current_time = time % 12
        if (time//12):
            ending = "PM"
        else: 
            ending = "AM"
        time += 2
        

        # Update persons and areas
        a, p, o = singles.get(words[i])[1]
        
        singles, combos, non_adjacent_combos = setup(p, a, o);

        # Single Inputs
        single_time = str(current_time)+":00"+ending+": "
        phrases.append(single_time+singles.get(words[i], "")[0])

        # Check for non-adjacent combos
        if words[i] in non_adjacent_combos:
            first_part.add((words[i],time))
        for word,prev_time in first_part:
            if non_adjacent_combos[word][0] == words[i]:
                time = prev_time # Since the only non-adjacent was it was all a dream
                if (time % 12 == 0):
                    current_time = 12
                else:
                    current_time = time % 12
                if (time//12):
                    ending = "PM: "
                else:
                    ending = "AM: "
                phrases.append(str(current_time)+":00"+ending+non_adjacent_combos[word][1])
                

        # Check for two inputs
        if (i == len(words)-1):
            continue # To avoid an index out of range error
        double_time = "    "+str(current_time)+":45"+ending+": "
        phrases.append(double_time+combos.get((words[i], words[i+1]), ""))

        # Check for three inputs
        if (i == len(words)-2):
            continue # To avoid an index out of range error
        triple_time = "    "*2+str(current_time+1)+":30"+ending+": "
        phrases.append(triple_time+combos.get((words[i], words[i+1], words[i+2]), ""))
    return phrases


def setup(person_count, area_count, object_count):
    # Single Inputs
    a = area_count
    p = person_count
    o = object_count
    singles = {
    #   word    : standard output                         new   areas|persons|objects
        "flirt" : ("You flirt with your " + persons[person_count],  ( a , p , o )),
        "smile" : ("You smile with your " + persons[person_count],  ( a , p , o )),
        "fight" : ("You get mad at your " + persons[person_count],  (a+1,p+1, o )),
        "wake"  : ("Your eyes start to open",                      ( a , p , o )),
        "work"  : ("You work with your " + persons[person_count],   ( 1 , 1 ,o+1)),
        "dream" : ("You dream about random things for a while",    ( a , p , o )),
        "eat"   : ("You are eating at " + areas[area_count],        ( a , p , o )),
        "talk"  : ("You talk with your " + persons[person_count],   ( a , p , o )),
        "cry"   : ("Tears start to fall down your face",           ( a , p , o )),
        "run"   : ("You run to " + areas[area_count],               (a+1, p , o )),
        "sleep" : ("You sleep at " + areas[area_count],             ( a , p , o )),
        "browse": ("You go on the internet",                       ( a , p ,o+1))
    }
    
    # Variable Inputs
    combos = {}
    combos.update({ (x, "cry")     : ("You %s, resulting in you crying")  % x for x in words})
    combos.update({ (x, "smile")   : ("You %s, resulting in you smiling") % x for x in words})

    combos.update({ ("dream", x)   : ("You dream about " + gerundOfword(x)) for x in words})
    combos.update({ ("smile", x)   : ("You smile because you are " + gerundOfword(x)) for x in words})

    combos.update({("sleep" , x, "wake") : "You dream about " + gerundOfword(x)  for x in words})

    combos.update({ ("flirt", "eat", x)   : ("Your date got ruined") for x in dateStuff})
    combos.update({ (x, "run")   : ("You sleepwalk") for x in sleepStuff})

    combos.update({ ("sleep", "talk", x)   : ("You sleeptalk about " + gerundOfword(x)) for x in sleepStuff})
    combos.update({ ("dream", "talk", x)   : ("You sleeptalk about " + gerundOfword(x)) for x in sleepStuff})

    static_combos = {
        # Two Input
        ("run", "work")    : "You go to work.",
        ("work", "run")    : "You quit your job.",
        ("eat", "fight")   : "You start a food fight.",
        ("work", "browse") : "You go on reddit and pretend to do work.",
        ("browse", "smile"): "You find some dank memes.",
        ("fight", "run")   : "You run away from a fight with your " + persons[person_count] + " to " + areas[area_count] +".",
        ("cry", "talk")    : "You cry but decide to talk it out with your " + persons[person_count]+".",
        ("run", "cry")     : "While you were running, you tripped and cracked your phone screen. RIP. *sobs*",
        ("fight", "talk")  : "You fight but decide to talk it out with your " + persons[person_count]+".",
        ("browse", "fight"):"You get into a heated argument through Facebook with your " + persons[person_count]+".",
        ("sleep", "wake")  : "You take a nap at " + areas[area_count]+".",
        ("dream", "wake")  : "You wake up from a nightmare"+".",
        ("work", "eat")    : "You eat at your desk since you have a lot of work to do.",
        ("cry", "work")    : "You get frustrated during work and start crying."+".",
        ("run", "smile")   : "You feel good because you're exercising"+".",
        ("sleep", "dream") : "You fall asleep and are beginning to dream"+".",
        ("browse", "eat")  : "You order interesting food online from Grubhub"+".",
        ("dream", "cry")   : "You have a nightmare and feel scared"+".",
        ("talk", "flirt")  : "Your casual conversation with your " +persons[person_count] + "turns into a steaming hot talk.",
        ("run","talk")     : "You exercise with your " +persons[person_count] +".",
        ("wake","flirt")   : "You wake up and ardpee happy to see bae.",
        ("wake","smile")   : "It is a lovely day.",
        ("wake","cry")     : "You wake up feeling awful.",
        ("wake","talk")    : "You wake up to your phone ringing from " +persons[person_count],
        ("wake","work")    : "You are late to work! Gotta rush!",
        ("wake","sleep")   : "The alarm started pounding and you pushed it off ... ...",
        ("wake","browse")  : "As you groggily wake up, you browse through your phone and it drops onto your sleepy face.",
        ("wake","fight")   : "You get angry and kick your sister for waking you up from a beauty's sleep.",
        ("eat","run")      : "You vomit all that you ate.",
        ("dream","run")    : "Someone has been running all over your mind. Who though?",
        ("dream","flirt")  : "Someone has been running all over your mind. Who though?",
        ("cry", "run")     : "You run away from your problem.",
        ("cry", "talk")    : "You have a hard time talking to your " +persons[person_count] +" and cry.",
        ("browse", "run")  : "There's a new workout fad you found so online you decide to try it out.",
        ("sleep","smile")  : "Sweet dreams. Ah~",
        ("dream","smile")  : "Sweet dreams. Ah~",
        ("eat", "sleep")   : "You have a midnight snack and binge eat.",
        ("cry", "eat")     : "You munch of ice cream and popcorns as you watch movies on Netflix.",
        ("browse","sleep") : "You fell asleep while browsing through your phone.",
        ("browse","dream") : "You fantasize over someone you see on social media.",
        ("eat", "browse")  : "You feel lonely as you eat alone and browse through instagram.",
        ("browse","run")   : "You quickly browse through facebook.",
        ("fight","eat")    : "You fight and bite their ears off!",
        ("fight","sleep")  : "You get knocked out by " +persons[person_count],
        ("fight", "cry")   : "RIP. Lost a fight against " +persons[person_count],
        ("browse", "smile"): "Haha! You found some dank memes!",
        ("fight", "smile") : "You get into a playfight with your " +persons[person_count],
        ("fight", "talk")  : "Although a fight ensued with your " +persons[person_count] + "you managed to talk it out.",
        ("dream", "wake")  : "'Wow, that was a weird dream...'",
        ("wake", "run")    : "You are running for your dear life---'GASP!' Oh, you just woke.",
        ("work", "talk")   : "You talked with random clients during work.",
        ("work", "browse") : "You go on reddit while working...",

        # Adjacent but no order ones
        ("talk", "flirt")  : "Your casual conversation with your " +persons[person_count] + "turns into a steaming hot talk." + "\nIf you were a vegetable, you'd be a cute-cumber.",
        ("flirt", "talk")  : "Your casual conversation with your " +persons[person_count] + "turns into a steaming hot talk."+"\nIf you were a vegetable, you'd be a cute-cumber.",
        ("eat", "wake")    : "You find yourself eating your pillow.",
        ("browse", "flirt"): "You decide to go on Tinder.",
        ("flirt", "browse"): "You decide to go on Tinder.",
        ("browse", "talk") : "You go on social media"+".",
        ("talk", "browse") : "You go on social media"+".",
        ("flirt", "eat")   : "You go on a date with your "+persons[person_count]+".",
        ("eat", "flirt")   : "You go on a date with your "+persons[person_count]+".",
        ("sleep", "cry")   : "You cry yourself to sleep"+".",
        ("cry", "sleep")   : "You cry yourself to sleep"+".",
        ("cry", "smile")   : "You cry tears of joy"+".",
        ("smile", "cry")   : "You cry tears of joy"+".",

        ("smile", "fight") : "You playfight with "+persons[person_count]+".",
        ("fight", "smile") : "You playfight with "+persons[person_count]+".",

        ("flirt","run")    : "You have a good run with your " +persons[person_count] + ".",
        ("run","flirt")    : "You have a good run with your " +persons[person_count] + ".",
        ("cry","work")     : "You are upset over work.",
        ("work","cry")     : "You are upset over work.",
        ("flirt","work")   : "You flirt with your coworker.",
        ("work","flirt")   : "You flirt with your coworker.",
        ("smile","work")   : "You got a pay raise at work!",
        ("work","smile")   : "You got a pay raise at work!",
        ("eat","talk")     : "You're eating while you talk. Gross.",
        ("talk","eat")     : "You're eating while you talk. Gross.",
        ("flirt","dream")  : "You fantasize! What wonders!",
        
        # Three Input
        ("work" , "fight", "run"  ) : "You're fired from work",
        ("work" , "sleep", "wake" ) : "You pull an all-nighter",
        ("run"  , "fight", "cry"  ) : "The mugger gets away as you despair.",
        ("run"  , "fight", "talk" ) : "You lose the mugger, but you find the police and file a report.",
        ("run"  , "fight", "smile") : "You catch up to the mugger and take back your " + objects[object_count] + ".",
        ("sleep" , "wake", "work") : "You're late for work",
        ("work" , "fight", "run")  : "You're fired from work",
        ("work" , "sleep", "wake") : "You pull an all-nighter",

        ("eat"  , "cry" , "sleep") : "You binge eat and cry yourself to sleep over " +persons[person_count],       
        ("cry"  , "eat" , "sleep") : "You binge eat and cry yourself to sleep over " +persons[person_count],       
        ("eat"  , "sleep" , "cry") : "You binge eat and cry yourself to sleep over " +persons[person_count],       
        ("eat"  , "sleep" , "cry") : "You binge eat and cry yourself to sleep over " +persons[person_count],       
    }
    

    non_adjacent_combos = {
    # First  >  Second = Result
        "sleep" : ("wake", "You wake up and realize, it was all a dream")

    }
    combos.update(static_combos)
    return singles, combos, non_adjacent_combos
def strip(phrase):
    first = False
    for i in range(len(phrase)):
        if phrase[i] == ":":
            if not first:
                first = True
                continue
            return phrase[i+2:] 

def match(phrases):
    # Doubled because their both iterators
    phrases2 = map(strip,phrases)
    phrases = map(strip,phrases)
    matched = set()
    for phrase in phrases:
        for title in titles.keys():
            if phrase in titles[title]:
                matched.add(title)
            for second_phrase in phrases2:
                if (phrase, second_phrase) in titles[title]:
                    matched.add(title)
    return matched
    
    
def reset():
    response = []
    count = 6
    words = set([
        "flirt",      "eat", 
        "smile",     "talk", 
        "fight",      "cry", 
        "wake",      "run", 
        "work",    "sleep",
        "dream",   "browse",
    ])
    return response, count, words



random_title = list(titles.keys())[randint(0,len(titles)-1)]
done = False
response, count, words = reset()
print("\n Welcome to How to Human\n"+"-"*25,"\n\n - Please type in 10 words\n   Press enter after typing\n   each word. to see if you\n   can get the following title:\n")
print("title: ",random_title, "\n")

while not done:
    
    current_time = ""
    if (count % 12 == 0):
        current_time += "12:00"
    else:
        current_time += str(count % 12)+":00"
    if (count//12):
        current_time += "PM: "
    else:
        current_time += "AM: "
    # Take in user input
    print("Words Left:",words)
    user = input(current_time);
    if user in words:
        if user == "end":
            parse(response)
            break
        words.remove(user)
        
        response.append(user)
        count += 2;

    else:
        print("Not in list\n")
    # End and show players their story
    if len(response) == 10:
        print("\n Story \n-------")
        phrases = parse(response)
        for line in phrases:
            if line[-1] != ' ': # The line is empty
                print(line)
        print("Titles:",match(phrases))
        if random_title not in match(phrases):
            print("-"*14,"\n- Try again -\n"+("-"*14))
            response, count, words = reset()
        else:
            done = True
            print("-"*12,"\n- You win! -\n"+("-"*12))
        

class Event:
    def __init__(triggers, phrase, person_change, area_change, object_change, good_change):
        self.triggers = triggers
        self.phrase = phrase
        self.person_change = person_count
        self.area_change = area_count
        self.object_change = object_count
        self.good_change = good_change
    def match(words, person_count, area_count, object_count, good_count):
        if words == trigger:
            person_count += self.person_change
            area_count += self.area_change
            object_count += self.object_change
            good_count += self.good_change
        return person_count, area_count, object_count, good_count   
        
