.. _plugin_force_correct_typein:

Force correct typed-in text in Anki
===================================

Overview
--------

In Anki, you can ask the user to type in the answer by specifying
a field ``Answer`` in the card definition as follows::

     {{type:Answer}}

Use this plugin to hide all but the ``Again`` ease button from the user
if the user typed in an incorrect answer.

Installation
------------

- Installation via Anki: in Anki, chose from menu ``Tools > Add-Ons > Browse&Install``
  and enter number ``153498160``.

- Direct installation: download the `plugin code`_, and save it to the ``addons``
  folder in your ``Anki`` folder.

.. _plugin code: https://raw.githubusercontent.com/bgro/anki-plugins/master/src/ForceCorrectTypeIn.py
