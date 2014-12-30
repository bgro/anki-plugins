# -*- mode: Python ; coding: utf-8 -*-
# Copyright © 2014, 2015 Bernd Grobauer 
# Based in part on code taken from
#  https://ankiweb.net/shared/info/4016858745
#
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE. 

import re, random, cgi
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.utils import showWarning
from anki.hooks import addHook

from anki.hooks import wrap
from anki.template.furigana import kana
from aqt.reviewer import Reviewer

## Constants

# Model name used for Multiple Choice Cards implemented by this extension
MULTIPLE_TRIGGER_TYPE_NAME = "MultipleChoice"

# Placeholder string for buttons: place the string defined below
# in the card question section to display at that location the multiple
# choice buttons

BUTTON_PLACEHOLDER = "[[[buttons]]]"



lastCardId = 0
idxs = range(1)
showingQuestion = 0
numAns = 0


# The following hook around the corrector gives us access
# to the given answer and the correct answer for a single {{type: XXX}} field.
# There may be an easier way, but I did not find it.

def corrector(reviewer, given, correct, showBad=True, _old=None):
    reviewer.typed_given = given
    reviewer.typed_correct = correct
    return _old(reviewer, given, correct, showBad)

Reviewer.correct = wrap(Reviewer.correct, corrector, "around")

def filterQuestion(self,buf):
    """
    """

    global idxs
    global lastCardId
    global numAns

    card = self.card

    modelname = card._note._model["name"]

    if not MULTIPLE_TRIGGER_TYPE_NAME in modelname:
        # This is not a card that with a multiple choice question;
        # we do nothing
      return buf 

    # Count the number of possible answers by first counting the
    # number of given distractor fields:

    numAns = 0;
    for field in card._note._model["flds"]:
        if "Distractor" in field["name"]:
            try:
                y = int(field["name"].split("Distractor")[-1])
                numAns +=1
            except:
                pass

    # Add one for the correct answer
    numAns += 1

    # We store field index and field content in 
    # lists: here we generate lists of fitting length

    ans = range(numAns)
    ansfld = range(numAns)

    # Populate the ans and ansfld lists:

    for x in card._note._model["flds"]:
      if x["name"] == "Question":
        question = card._note.fields[x["ord"]]
      if x["name"] == "Answer":
        ansfld[0] = x
        ans[0] = card._note.fields[x["ord"]]
      elif "Distractor" in x["name"]:
          try:
              y = int(x["name"].split("Distractor")[-1])
              ansfld[y] = x
              ans[y] = card._note.fields[x["ord"]]
          except:
              pass


    txt = buf
    

    # We will shuffle the answers -- we initialize
    # the idxs list which we will later shuffle

    if len(idxs) != numAns:
        idxs = range(numAns)

    if (card.id != lastCardId):
        # Only shuffle answer buttons if we are not displaying
        # the same card as just before.
        idxs2 = idxs
        random.shuffle(idxs2)
        idxs = idxs2
        lastCardId = card.id

    replacement_text = []

    # Now, we create the answer buttons, 
    # - when prompting the question: insert the buttons with code that registers clicks
    #   and leads to the answer page
    # - when showing the answer: insert the buttons in the same order and mark
    #   right/wrong answers

    for x in idxs:
        if showingQuestion:
            if ans[x]:
                # Only show non-empty answer possiblities
                replacement_text.append("<input type=\"button\" value=\""+ans[x]+"\" onclick='py.link(\"typeans:"+str(x)+"\");py.link(\"ans\");'>")
        else:
            if ans[x]:
                # Only show non-empty answer possiblities
                if ("%s" % self.typedAnswer) == ("%s" % x):
                    # This is the answer that the user clicked upon
                    if ("%s" % self.typedAnswer) == "0":
                        # He clicked on the correct answer, so show the button green
                        replacement_text.append("<input type=\"button\" style='background-color: green' value='"+ans[x]+"'/> " )
                    else:
                        # He clicked on the wrong answer: show in red
                        replacement_text.append("<input type=\"button\" style='background-color: red' value='"+ans[x]+"'/>" )
                else:
                    # This is an answer the user did not click on
                    if x == 0:
                        # If it is the right answer, show it as green
                        replacement_text.append("<input type=\"button\" style='background-color: green' value = '"+ans[x]+"'/>" )
                    else:
                        replacement_text.append("<input type=\"button\" value='"+ans[x]+"'/>" )
    replacement_text = " ".join(replacement_text)
    txt = txt.replace(BUTTON_PLACEHOLDER,replacement_text,1)

    return txt 

def filterQuestionB(self,buf):
    return oldMungeQA(self,filterQuestion(self,buf))
    
def myShowQuestion(self):
    global showingQuestion
    showingQuestion = 1
    oldShowQuestion(self)

def myShowAnswer(self):
    global showingQuestion
    showingQuestion = 0

    oldShowAnswer(self)

def myAnswerButtons(self):

    """
    Depending on whether the right answer was given or not,
    enable the buttons for a successful test.
    """

    txt = oldAnswerButtons(self)

    card = self.card
    modelname = card._note._model["name"]
    
    if not (MULTIPLE_TRIGGER_TYPE_NAME in modelname):
        return txt

    if MULTIPLE_TRIGGER_TYPE_NAME in modelname:
        if self.typedAnswer == None or not self.typedAnswer.isdigit():
            # If the user pressed "Show Answer" instead of one of the
            # answer buttons, register a wrong answer
            ans = 99999
        else:
            ans = int(self.typedAnswer)
        if (ans == 0):
            # correct answer, remove "Again" button
            txt = txt.replace("<td","<!--td",1);
            txt = txt.replace("/td>","/td-->",1);
        if (ans >= 1):
            # wrong answer: remove all buttons but the "Again" button
            # by first removing all buttons and then selectively enabling
            # the very first button
            txt = txt.replace("<td","<!--td");
            txt = txt.replace("/td>","/td-->");
            txt = txt.replace("<!--td","<td",1);
            txt = txt.replace("/td-->","/td>",1);
    else:
        return txt

    return txt

oldMungeQA = Reviewer._mungeQA
Reviewer._mungeQA = filterQuestionB

oldShowQuestion = Reviewer._showQuestion
Reviewer._showQuestion = myShowQuestion

oldShowAnswer = Reviewer._showAnswer
Reviewer._showAnswer = myShowAnswer

oldAnswerButtons = Reviewer._answerButtons
Reviewer._answerButtons = myAnswerButtons

