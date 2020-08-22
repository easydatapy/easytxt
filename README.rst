=================================
Welcome to EasyTXT documentation!
=================================

EasyTXT is a set of high and low level modules to help you with text
normalization and manipulation.

.. contents::

Basic Features
==============

Some of the most important features that EasyTXT provide:

* normalize text
* break text into normalized sentences
* break text into normalized features
* HTML to text
* fix text encoding
* normalize spaces
* converting html table data into sentences or features
* html table reader which returns dict of column row info

There are many more features for which please refer to the source code.
Complete documentation for all features is a work in progress.

TextParser
==========

Text examples
-------------
In this example lets parse badly structured text and output into multiple formats.

Please note that calling multiple formats at the same time won't affect performance
since sentences are cached and all other formats call sentenced under the hood.

    >>> from easytxt import TextParser
    >>> test_text = '  first sentence... Bad uÌˆnicode.   HTML entities &lt;3!'
    >>> text_parser = TextParser(test_text)
    >>> text_parser.sentences
    ['First sentence...', 'Bad ünicode.', 'HTML entities <3!']

Lets just get normalized text.

    >>> text_parser.text
    First sentence... Bad ünicode. HTML entities <3!

Here is example how to extract features from text.

    >>> test_text = 'Features - color: Black - material: Aluminium. Last Sentence'
    >>> text_parser = TextParser(test_text)

Text parser will try to automatically detect which are regular sentences and which
are features and show only extracted features when called ``features`` attr.

    >>> text_parser.features
    [('Color', 'Black'), ('Material', 'Aluminium')]

Return features dictionary instead a list of tuples.

    >>> text_parser.features_dict
    {'Color': 'Black', 'Material': 'Aluminium'}

Let's get a value from a specific feature.

    >>> text_parser.feature('color')
    Black

Although regular sentences are ignored when calling ``features`` attr, they can
still be seen when calling ``sentences`` or ``text`` attr.

    >>> text_parser.sentences
    ['Ignored text.', 'Color: Black.', 'Material: Aluminium.', 'Ignore again.']
    >>> text_parser.text
    Ignored text. Color: Black. Material: Aluminium. Ignore again.

HTML examples
------------------
In this example we will try to parse html text. There is not special argument to be
passed into ``TextParser`` in order to process HTML. Usage is exactly the same as
for ``regular text`` since ``html`` is detected and processed automatically.

    >>> test_text = '<p>Some sentence</p> <ul><li>* Easy <b>HD</b> camera </li></ul>'
    >>> text_parser = TextParser(test_text)
    >>> text_parser.sentences
    ['Some sentence.', 'Easy HD camera.']

Dependencies
============

`EasyTXT` relies on following libraries in some ways:

  * ftfy_ to fix encoding.
  * pyquery_ to help with html to text conversion.

.. _ftfy: https://pypi.org/project/ftfy/
.. _pyquery: https://pypi.org/project/pyquery/
