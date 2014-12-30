# -*- mode: Python ; coding: utf-8 -*-
# Copyright © 2014, 2015 Bernd Grobauer 
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

