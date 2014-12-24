# -*- mode: Python ; coding: utf-8 -*-
# Copyright © 2014, 2015 Bernd Grobauer 
# Based in part on code by 
#
# License: GNU GPL, version 2 or later;
# http://www.gnu.org/copyleft/gpl.html


import re, random, cgi
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.utils import showWarning
from anki.hooks import addHook

from anki.hooks import wrap
from anki.template.furigana import kana
from aqt.reviewer import Reviewer

## Constants

# Model name used for cards that force correct typing in of answer
# as implemented by this extension
TYPE_CHECK_TRIGGER = "ForceCorrectTypeIn"



# The following hook around the corrector gives us access
# to the given answer and the correct answer for a single {{type: XXX}} field.
# There may be an easier way, but I did not find it.

def corrector(reviewer, given, correct, showBad=True, _old=None):
    reviewer.typed_given = given
    reviewer.typed_correct = correct
    return _old(reviewer, given, correct, showBad)

Reviewer.correct = wrap(Reviewer.correct, corrector, "around")

def myAnswerButtons(self):

    """
    Depending on whether the right answer was given or not,
    enable the buttons for a successful test.
    """

    txt = oldAnswerButtons(self)

    card = self.card
    modelname = card._note._model["name"]
    
    if not (TYPE_CHECK_TRIGGER in modelname):
        return txt


    if self.typed_given == self.typed_correct:
        # correct answer, remove "Again" button
        txt = txt.replace("<td","<!--td",1);
        txt = txt.replace("/td>","/td-->",1);
    else:
        # wrong answer: remove all buttons but the "Again" button
        # by first removing all buttons and then selectively enabling
        # the very first button
        txt = txt.replace("<td","<!--td");
        txt = txt.replace("/td>","/td-->");
        txt = txt.replace("<!--td","<td",1);
        txt = txt.replace("/td-->","/td>",1);

    return txt

oldAnswerButtons = Reviewer._answerButtons
Reviewer._answerButtons = myAnswerButtons

