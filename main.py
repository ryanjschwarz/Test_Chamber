from flask import Flask, render_template, request, redirect
import urllib2
from bs4 import BeautifulSoup
import lxml
import re
import random
import numpy as np
import re
import json
import random

""""
def generate_random_word():
  random_wiki = "https://en.wikipedia.org/wiki/Special:Random"

  #Open the page with urllib2
  page = urllib2.urlopen(random_wiki)
  finalurl = page.geturl()


  #Parse the webpage using BeautifulSoup. lxml parser is fast
  soup = BeautifulSoup(page, 'lxml')

  #Find all paragraphs on the wikipedia article
  #The .findAll() function returns a list
  paragraph_boxes = soup.findAll('p')


  clean_paragraph = ""
  #Iterates through the paragraph_boxes list and deletes the html tags and extra whitespace
  for paragraph in paragraph_boxes:
    clean_paragraph += paragraph.text.strip() + " "

  #Removes all of the propper nouns (words that have capital letters but are not following a period) from clean_paragraph
  no_pnoun_paragraph = re.sub(r'([^.])( [A-Z]\w*)', r'\1', clean_paragraph)

  #Adds only the alphabetic characters to a new string
  paragraph_alpha = ""
  for i in no_pnoun_paragraph:
    if i.isalpha() == True or i == " " or i == "-":
      paragraph_alpha += i

  #Make all words lowercase
  paragraph_lower = ""
  for i in paragraph_alpha:
    paragraph_lower += i.lower()

  #Remove the 'u that signifies unicode from string
  paragraph_lower = paragraph_lower.encode('utf-8')

  #Adds all of the words from paragraph_lower to a list
  word_list = paragraph_lower.split()

  #Remove all small words that are less than 3 letters
  big_word_list = []

  for item in word_list:
    if len(item) > 3:
      big_word_list.append(item)

  #Function that generates random words    

  random_number = random.randint(0, len(big_word_list))
  random_word = big_word_list[random_number]
  return [random_word, finalurl]
"""
scrubber = open('bullets.txt', 'r')
new_content = ""
for line in scrubber:
    # print(type(line))
    new_line = re.sub("\d", "#", line)
    #new_line = new_line.replace("/", " / ")
    new_content += new_line
scrubber.close()

#print(new_content)

writer = open("bullets.txt", "w")
new_content = new_content.strip().replace('\n\n', '\n')
new_content = new_content.strip().replace('...', ' / ')
#writer.write(new_content.strip().replace('**', '\n'))
writer.write(new_content)

writer.close()
#if letter == "/":
#  letter = "/ "
#print (line)

with open('bullets.txt', 'r') as bullets:

    parsesA = []
    parsesB = []
    parsesC = []
    parses = []
    verbs = []
    verbsA = []
    verbsB = []
    verbsC = []
    delimeters = "--", ";", "\n"
    regexPattern = "|".join(map(re.escape, delimeters))

    for bullet in bullets:

        a = re.split(regexPattern, bullet)
        #print (a[0].split())
        verbs.append(a[0].split()[1])
        verbsA.append(a[0].split()[1])

        #print(verbs)

        item = a[0].replace('\u2008', ' ').replace('\u2009', ' ')
        parsesA.append(item)

        if (len(a) >= 3):
            item = a[1].replace('\u2008', ' ').replace('\u2009', ' ')
            verbs.append(a[1].split()[0])
            verbsB.append(a[1].split()[0])
            parsesB.append(item)

        if (len(a) >= 4):
            #print (len(a))
            item = a[2].replace('\u2008', ' ').replace('\u2009', ' ')
            verbs.append(a[2].split()[0])
            verbsC.append(a[2].split()[0])
            parsesC.append(item)
    #print(verbs)
    #print(parsesA)


#print(parsesA)
#Takes the pairs of words that follow other words
def make_pairs(parses):
    for parse in parses:
        #print (parse)
        for i in range(len(parse.split()) - 1):
            yield (parse.split()[i], parse.split()[i + 1])


#print(parsesA)
pairsA = make_pairs(parsesA)
pairsB = make_pairs(parsesB)
pairsC = make_pairs(parsesC)

def getRandom(section, dict):
    try:
        a = np.random.choice(dict[section[-1]])
        return a
    except:
        #print("key exception")
        return ""


def buildBullet(*args):  #TODO ADD data input
    #Test Data
    sampleSize = 5
    action = ['- ', random.choice(verbs)]
    impact = [';', random.choice(verbs)]
    result = ['--', random.choice(verbs)]

    #print(action)
    #print(impact)
    #print(result)

    for i in range(sampleSize):
        action.append(getRandom(action, word_dict))
        impact.append(getRandom(impact, word_dict))
        result.append(getRandom(result, word_dict))

    return (' '.join((action) + (impact) + (result)))

#START RANDOM BULLET CODE

word_dict = {}
word_dictA = {}
word_dictB = {}
word_dictC = {}

def add_keys(pairs, dict):
    for word1, word2 in pairs:
      #print(word1 + " " + word2)
      if word1 in dict.keys():
          dict[word1].append(word2)

      else:
          dict[word1] = [word2]

#add_keys(pairsA, word_dictA)
add_keys(make_pairs(parsesA), word_dictA)
add_keys(make_pairs(parsesB), word_dictB)
add_keys(make_pairs(parsesC), word_dictC)
add_keys(pairsA, word_dict)
add_keys(pairsB, word_dict)
add_keys(pairsC, word_dict)
#add_keys(pairsC, word_dictC)

#with open('test_pickle.txt', 'wb') as handle:
#  pickle.dump(word_dictA, handle)

#print (word_dictA)
#print(word_dictA)

a = open("dictfile.txt", "r+")
a.write(json.dumps(word_dict))
a.close()

a = open("dictfileA.txt", "r+")
a.write(json.dumps(word_dictA))
a.close()

a = open("dictfileB.txt", "r+")
a.write(json.dumps(word_dictB))
a.close()

a = open("dictfileC.txt", "r+")
a.write(json.dumps(word_dictC))
a.close()

def build_bullet(rel_dic, *args):  # Designed to do one section of a bullet
    section = []
    verbs = []

    if (rel_dic == word_dictA):
      verbs = verbsA
    
    elif (rel_dic == word_dictB):
      verbs = verbsB
    
    elif (rel_dic == word_dictC):
      verbs = verbsC

    #Case one - section only has action verb
    if (len(args) == 0):
        #print (verbs)
        section.append(random.choice(verbs))
        #verb = random.choice(list(rel_dic.keys()))
        #print (rel_dic.keys())
        #section.append(verb)
        
        while (section[-1] in rel_dic.keys()):
            #print (section[-1])
            section.append(getRandom(section, rel_dic))

        return ' '.join(section)

    elif (len(args) == 1 and args[0] in rel_dic.keys()):
        section.append(args[0])
        while (section[-1] in rel_dic.keys()):
            section.append(getRandom(section, rel_dic))
        return ' '.join(section)

    #If the two words are next to eachother (i.e. led msn)
    elif (len(args) == 2):
        #running = []
        if (args[1]) in rel_dic.get(args[0]):
            section.append(args[0])
            section.append(args[1])
            while (section[-1] in rel_dic.keys()):
                section.append(getRandom(section, rel_dic))
            return ' '.join(section)

        #If the two words are related but not directly next to each other in the dict (i.e. led, sorties)
        else:
            flag = False
            section.append(args[0])
            while (section[-1] in rel_dic.keys()):#Change this to hit an end state
                section.append(getRandom(section, rel_dic))
                #print(section)
                if (section[-1] in rel_dic.keys()
                        and args[1] in rel_dic.get(section[-1])):
                    section.append(args[1])
                    flag = True
            if not flag:
                section.append(args[1])
                while (section[-1] in rel_dic.keys()):
                    section.append(getRandom(section, rel_dic))

        return ' '.join(section)
        #print('stop')

    else:
        print("something went wrong")

##END RANDOM BULLET CODE

#Set up website with index.html
app = Flask('app')

@app.route('/')
def hello_world():
    return render_template('index.html')

#When the button is clicked on html, execute the function
@app.route('/submit', methods = ['POST'])
def sumbit():
  #Saves the array result of generate_random_words() to return_results. This allows both variables to be taken.
  #return_results = generate_random_word()
  print (verbs)
  return_results = '- ' + build_bullet(word_dictA).strip() + '; ' + build_bullet(word_dictB).strip() + "--" + build_bullet(word_dictC).strip() 
  #Bullet outcome here
  #Sets both values in the array to variables
  #display_word = return_results
  #display_url = return_results

  #return render_template('index.html', display_word=display_word, display_url=display_url)
  #display_word=display_word
  return render_template('index.html',display_word = return_results)


if 'app' == '__main__':
    app.run()

app.run(host='0.0.0.0', port=8080)