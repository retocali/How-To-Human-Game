from random import randint

# How much the user has to type in
MAX_INPUT_LENGTH = 10

# Used for timing in the day
START_TIME = 6
INCREMENT = 2
HALF_HOUR = 30
STEP_INCREMENT = 45

dateStuff = ["run","cry","fight"]
sleepStuff = ["sleep","dream"]

# Various items that are used to make the sentences be more diverse
persons = ["significant other", "boss", "coworker"]
areas   = ["your home", "your workplace", "the streets", "a restaurant"]
objects = ["phone", "wallet", "bag"]
indent = "    "

# The titles that the player can earn
titles = {
        "Scarlet Letter" : {
                # Sentences earn the titles either as a single sentence or tuple of sentences
                "You decide to go on Tinder.", 
                "Your casual conversation with your boss turns into a steaming hot talking.",
                "Your casual conversation with your coworker turns into a steaming hot talk.",
                ("You flirt with your boss.","You sleep at your workplace."),
                ("You flirt with your coworker.", "You sleep at your workplace."),
                "You go on a date with your boss.",
                "You go on a date with your coworker."
        },
        "Bum" : {
            "You quit your job.", 
            "You're fired from work",
            "You run to the streets.", 
            "You sleep at the streets.",
        },
        "Hero" : {
            "You catch up to the mugger and take back your phone.",
            "You catch up to the mugger and take back your wallet.",
            "You catch up to the mugger and take back your bag."     
        }
}

def gerundOfword(x):
    # Gives the -ing form of a word
    return x[:-1]+(x[-1] if x[-1] != 'e' else '') + (x[-1] if x[-1] == 'n' else '') +"ing"

def parse(words):
    p = 0 # person_count
    a = 0 # area_count
    o = 0 # objectcount

    time = START_TIME-INCREMENT
    singles, combos, non_adjacent_combos = setup(p, a, o);
    first_part = set()
    phrases = []
    
    for i in range(len(words)):
        
        time += INCREMENT
        # Update persons and areas and sentences
        a, p, o = singles.get(words[i])[1]
        singles, combos, non_adjacent_combos = setup(p, a, o);

        # Single Inputs
        single_time = give_time(time)
        phrases.append(single_time+singles.get(words[i], "")[0])

        # Check for non-adjacent combos
        if words[i] in non_adjacent_combos:
            first_part.add((words[i],time))
        for word,prev_time in first_part:
            if non_adjacent_combos[word][0] == words[i]:
                phrases.append(give_time(time, HALF_HOUR)+non_adjacent_combos[word][1])
                

        # Check for two inputs
        if (i == len(words)-1):
            continue # To avoid an index out of range error
        # Does the next event 45 minutes later
        double_time = indent+give_time(time, STEP_INCREMENT)
        phrases.append(double_time+combos.get((words[i], words[i+1]), ""))

        # Check for three inputs
        if (i == len(words)-2):
            continue # To avoid an index out of range error
        # Does the next event 1:30 minutes later
        triple_time = indent*2+give_time(time, 2*STEP_INCREMENT)
        phrases.append(triple_time+combos.get((words[i], words[i+1], words[i+2]), ""))


    return phrases


def setup(person_count, area_count, object_count):
    # Single Inputs
    a = area_count
    p = person_count
    o = object_count

    singles = {
    #   word    : standard output                                   new areas|persons|objects after using these actions
        "wake"  : ("Your eyes start to open"+".",                          ( a , p , o )),
        "run"   : ("You run to " + areas[area_count]+".",                  (a+1, p , o )),
        "sleep" : ("You sleep at " + areas[area_count]+".",                ( a , p , o )),
        "cry"   : ("Tears start to fall down your face"+".",               ( a , p , o )),
        "eat"   : ("You are eating at " + areas[area_count]+".",           ( a , p , o )),
        "dream" : ("You dream about random things for a while"+".",        ( a , p , o )),
        "work"  : ("You work with your " + persons[person_count]+".",      ( 1 , 1 ,o+1)),
        "talk"  : ("You talk with your " + persons[person_count]+".",      ( a , p , o )),
        "flirt" : ("You flirt with your " + persons[person_count]+".",     ( a , p , o )),
        "smile" : ("You smile with your " + persons[person_count]+".",     ( a , p , o )),
        "fight" : ("You get mad at your " + persons[person_count]+".",     (a+1,p+1, o )),
        "browse": ("You browse through your " + objects[object_count]+".", ( a , p ,o+1))
    }
    
    # Variable inputs
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
        ("flirt","dream")  : "You fantasize! What wonders!",

        ("sleep","smile")  : "Sweet dreams. Ah~",
        ("sleep", "wake")  : "You take a nap at " + areas[area_count]+".",
        ("sleep", "dream") : "You fall asleep and are beginning to dream"+".",
        
        ("run", "work")    : "You go to work.",
        ("run", "smile")   : "You feel good because you're exercising"+".",
        ("run", "talk")    : "You exercise with your " +persons[person_count] +".",
        ("run", "cry")     : "While you were running, you tripped and lost your "+objects[object_count],
        ("run", "fight")   : "While you were running, a mugger stole your "+objects[object_count],
        
        ("work", "run")    : "You quit your job.",
        ("work", "browse") : "You go on reddit while working...",
        ("work", "talk")   : "You talked with random clients during work.",
        ("work", "eat")    : "You eat at your desk since you have a lot of work to do.",
        
        ("eat", "fight")   : "You start a food fight.",
        ("eat", "run")     : "You vomit all that you ate.",
        ("eat", "wake")    : "You find yourself eating your pillow.",
        ("eat", "sleep")   : "You have a midnight snack and binge eat.",
        ("eat", "browse")  : "You feel lonely as you eat alone and browse through instagram.",
        
        ("cry", "run")     : "You run away from your problem.",
        ("cry", "eat")     : "You munch on ice cream and popcorns as you watch movies on Netflix.",
        ("cry", "talk")    : "You have a hard time talking to your " +persons[person_count] +" and cry.",
        
        ("dream","smile")  : "Sweet dreams. Ah~",
        ("dream", "wake")  : "'Wow, that was a weird dream...'",
        ("dream", "cry")   : "You have a nightmare and feel scared"+".",
        ("dream", "run")   : "Someone has been running all over your mind. Who though?",
        ("dream", "flirt") : "Someone has been running all over your mind. Who though?",
        
        ("fight", "eat")   : "You fight and bite their ears off!",
        ("fight", "sleep") : "You get knocked out by " +persons[person_count],
        ("fight", "cry")   : "RIP. Lost a fight against " +persons[person_count],
        ("fight", "talk")  : "Although a fight ensued with your " +persons[person_count] + "you managed to talk it out.",
        ("fight", "run")   : "You run away from a fight with your " + persons[person_count] + " to " + areas[area_count] +".",

        ("browse", "smile"): "Haha! You found some dank memes!",
        ("browse", "run")  : "You quickly browse through facebook.",
        ("browse", "eat")  : "You order interesting food online from Grubhub"+".",
        ("browse", "sleep"): "You fell asleep while browsing through your phone.",
        ("browse", "dream"): "You search on Amazon for a new " +objects[object_count],
        ("browse", "run")  : "There's a new workout fad you found so online you decide to try it out.",
        ("browse", "fight"):"You get into a heated argument through Facebook with your " + persons[person_count]+".",

        ("wake","smile")   : "It is a lovely day.",
        ("wake","cry")     : "You wake up feeling awful.",
        ("wake","work")    : "You are late to work! Gotta rush!",
        ("wake","flirt")   : "You wake up and are happy to see bae.",
        ("wake","sleep")   : "The alarm started pounding and you pushed it off ... ...",
        ("wake","talk")    : "You wake up to your phone ringing from " +persons[person_count],
        ("wake", "run")    : "You are running for your dear life---'GASP!' Oh, you just woke.",
        ("wake","fight")   : "You get angry and kick your sister for waking you up from a beauty's sleep.",
        ("wake","browse")  : "As you groggily wake up, you browse through your phone and it drops onto your sleepy face.",
                
        # Adjacent but no order ones
        ("talk", "flirt")  : "Your casual conversation with your " +persons[person_count] + "turns into a steaming hot talk." + "\nIf you were a vegetable, you'd be a cute-cumber.",
        ("flirt", "talk")  : "Your casual conversation with your " +persons[person_count] + "turns into a steaming hot talk."+"\nIf you were a vegetable, you'd be a cute-cumber.",
        
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
        
        # Three Input
        ("work" , "fight", "run"  ) : "You're fired from work",
        ("work" , "sleep", "wake" ) : "You pull an all-nighter",
        ("run"  , "fight", "cry"  ) : "The mugger gets away as you despair.",
        ("run"  , "fight", "talk" ) : "You lose the mugger, but you find the police and file a report.",
        ("run"  , "fight", "smile") : "You catch up to the mugger and take back your " + objects[object_count] + ".",
        ("sleep" , "wake", "work")  : "You're late for work",

        ("eat"  , "cry" , "sleep") : "You binge eat and cry yourself to sleep over " +persons[person_count],       
        ("cry"  , "eat" , "sleep") : "You binge eat and cry yourself to sleep over " +persons[person_count],       
        ("eat"  , "sleep" , "cry") : "You binge eat and cry yourself to sleep over " +persons[person_count],       
        ("eat"  , "sleep" , "cry") : "You binge eat and cry yourself to sleep over " +persons[person_count],       
    }
    

    non_adjacent_combos = {
        # First >  Second = Result
        "sleep" : ("wake", "You wake up and realize, it was all a dream")

    }
    combos.update(static_combos)
    return singles, combos, non_adjacent_combos

def strip(phrase):
    # Strips whitespace and time from a line
    first = False
    for i in range(len(phrase)):
        if phrase[i] == ":":
            if not first:
                first = True
                continue
            return phrase[i+2:] 

def match(phrases):
    # finds titles that match the phrases
    matched = set()
    # Doubled because their both iterators
    phrases = list(map(strip,phrases))
    for phrase in phrases:
        for title in titles.keys():
            if phrase in titles[title]:
                matched.add(title)
            for second_phrase in phrases:
                if (phrase, second_phrase) in titles[title]:
                    matched.add(title)
    return matched 
    
def reset():
    # resets the game
    response = []
    count = START_TIME
    words = set([
        "flirt",      "eat", 
        "smile",     "talk", 
        "fight",      "cry", 
        "wake",      "run", 
        "work",    "sleep",
        "dream",   "browse",
    ])
    return response, count, words

def give_time(hours, minutes=0):
    FULL_HOURS = 12
    current_time = ""
    hours += minutes // 60
    minutes %= 60
    if (hours % FULL_HOURS == 0):
        current_time += "12"
    else:
        current_time += str(hours % FULL_HOURS)
    current_time += ":"+("00"+str(minutes))[-2:] # Right pad minutes
    if (hours // FULL_HOURS):
        current_time += "PM: "
    else:
        current_time += "AM: "
    return current_time


random_title = list(titles.keys())[randint(0,len(titles)-1)]
done = False
response, count, words = reset()


# Instructions
print("""
Welcome to How to Human
-----------------------

  Please type in 10 words
  Press enter after typing
  each word in a particular
  order to see if you can 
  get the following title:
    
""")
print("Title: ",random_title, "\n")


# Main input loop
while not done:
        
    # Take in user input
    print("Words Left:",words)
    user = input(give_time(count));
    if user in words:
        if user == "end":
            parse(response)
            break
        words.remove(user)
        
        response.append(user)
        count += INCREMENT;
    else:
        print("Not in list\n")

    # End and show players their story
    if len(response) == MAX_INPUT_LENGTH:
        print("",
              " Story ",
              "-------", sep='\n')
        phrases = parse(response)
        
        # Prints all the lines
        for line in phrases:
            if line[-1] != ' ': # The line is empty
                print(line)

        # Finds the titles and checks
        earned = match(phrases)
        output = str(earned) if len(earned) > 0 else "None Earned"
        print("|"+"-" * (len(output)+2)+"|")
        print("| " + output + " |")
        print("|"+"-" * (len(output)+2)+"|")

        # End Conditions
        if random_title not in earned:
            print("|-----------|",
                  "| Try again |",
                  "|-----------|", sep= '\n')
            response, count, words = reset()
        else:
            done = True
            print("|----------|",
                  "| You Win! |",
                  "|----------|", sep= '\n')
        
