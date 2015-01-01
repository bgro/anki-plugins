.. _plugin_multiple_choice:

Multiple Choice Quiz in Anki
============================

Overview
--------

The plugin supports the creation of multiple-choice questions. The possible
answers (once correct and several wrong ones) are displayed as click-able
buttons.

.. figure:: images/multiple_choice_example_question.png
   :scale: 50 %

   Example multiple choice card


The plugin further only allows the user to click any other than the
"Again" ease button if the correct answer has been provided.

.. figure:: images/multiple_choice_example_right_answer.png
   :scale: 50 %

   Example: correct answer has been given


If
a wrong answer has been given, only the "Again" button is displayed
along with the correct answer:

.. figure:: images/multiple_choice_example_wrong_answer.png
   :scale: 50 %

   Example: wrong answer has been given


This code for this plugin was based on the `"Multi-choice Quiz" plugin`_ but
by now has been almost completely rewritten in order to make the plugin 
more stable.

Installation
------------

- Installation via Anki: in Anki, chose from menu ``Tools > Add-Ons > Browse&Install``
  and enter number ``1300062419``.

- Direct installation: download the `plugin code`_, and save it to the ``addons``
  folder in your ``Anki`` folder.

.. _plugin code: https://raw.githubusercontent.com/bgro/anki-plugins/master/src/MultipleChoiceQuiz.py
 

Usage instructions
------------------

- Create a card model whose name contains the string ``MultipleChoice`` 
- In that model, define the following fields:

  - ``Answer``
  - ``Distractor1``
  - ``Distractor2``
  - ... (up to at most ``Distractor9``)

  You probably want to add a field ``Question`` for posing the question,
  but it is up to you how you design your card.

- When defining the card layout, use the string ``[[[buttons]]]`` to
  determine the place at which the answer buttons will be displayed:
  - when the question is shown, at this place the buttons with
    the possible answers will be shown
  - when the answer is shown, at this place the buttons will be
    shown with the correct answer button highlighted in green and a
    possible wrongly pressed answer button highlighted in red.

- When creating a card, fill in the correct answer into field ``Answer``
  and fill in as many distractors as you like in the remaining fields
  (you can leave distractor fields empty, if you want)

.. _"Multi-choice Quiz" plugin: https://ankiweb.net/shared/info/4016858745
