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
In this example lets parse badly structured text and output it into multiple
formats.

Please note that calling multiple formats at the same time won't affect
performance since sentences are cached and all other formats call sentenced
under the hood.

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
-------------
In this example we will try to parse html text. There is not special argument to be
passed into ``TextParser`` in order to process HTML. Usage is exactly the same as
for ``regular text`` since ``html`` is detected and processed automatically.

    >>> test_text = '<p>Some sentence</p> <ul><li>* Easy <b>HD</b> camera </li></ul>'
    >>> text_parser = TextParser(test_text)
    >>> text_parser.sentences
    ['Some sentence.', 'Easy HD camera.']

Custom parameters
-----------------
**allow**

We can control which sentences we want to get extracted by providing list of
keywords into ``allow`` parameter.

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> text_parser = TextParser(test_text, allow=['first', 'third'])
    >>> text_parser.sentences
    ['First sentence?', 'Third sentence.']

Regex pattern is also supported as parameter value:

    >>> text_parser = TextParser(test_text, allow=[r'\bfirst'])

**callow**

``callow`` is similar to ``allow`` but with exception that provided keys
are case sensitive. Regex pattern as key is also supported.

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> text_parser = TextParser(test_text, allow=['First', 'Third'])
    >>> text_parser.sentences
    ['Third sentence.']

**deny**

We can control which sentences we don't want to get extracted by providing
list of keywords into ``deny`` parameter. Regex pattern as key is also supported.

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> text_parser = TextParser(test_text, deny=['first', 'third'])
    >>> text_parser.sentences
    ['Second sentence.']

**cdeny**

``cdeny`` is similar to ``deny`` but with exception that provided keys
are case sensitive. Regex pattern as key is also supported.

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> text_parser = TextParser(test_text, deny=['First', 'Third'])
    >>> text_parser.sentences
    ['First sentence?', 'Second sentence.']

**capitalize**

By default all sentences will get capitalized as we can see bellow.

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> text_parser = TextParser(test_text)
    >>> text_parser.sentences
    ['First sentence?', 'Second sentence.', 'Third sentence.']

We can disable this behaviour by settings parameter ``capitalize`` to ``False``.

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> text_parser = TextParser(test_text, capitalize=False)
    >>> text_parser.sentences
    ['first sentence?', 'Second sentence.', 'third sentence.']

**language**

If we are parsing text in other language than english then we need to
specify language parameter to which language our text belong to in order
for sentences to be split properly around abbreviations.

    >>> test_text = 'primera oracion? Segunda oración. tercera oración'
    >>> text_parser = TextParser(test_text, language='es')
    >>> text_parser.sentences
    ['Primera oracion?', 'Segunda oración.', 'Tercera oración.']

Please note that currently only ``en`` and ``es`` language parameter values
are supported. *Support for more is coming soon with automatic language
detection.*

**css_query**

In cases that we provide html string, we can through ``css_query`` parameter
select from which html node text would be extracted.

    >>> test_text = '<p>Some sentence</p> <ul><li>* Easy <b>HD</b> camera </li></ul>'
    >>> text_parser = TextParser(test_text, css_query='p')
    >>> text_parser.sentences
    ['Some sentence.']

**exclude_css**

In cases that we provide html string, we can through ``exclude_css`` parameter
limit from which html node text would be extracted.

    >>> test_text = '<p>Some sentence</p> <ul><li>* Easy <b>HD</b> camera </li></ul>'
    >>> text_parser = TextParser(test_text, exclude_css=['p', 'b'])
    >>> text_parser.sentences
    ['Easy camera.']

**split_inline_breaks**

By default text with chars like ``*``, `` - `` and bullet points would get split
into sentences.

Example:

    >>> test_text = '- first param - second param'
    >>> text_parser = TextParser(test_text)
    >>> text_parser.sentences
    ['First param.', 'Second param.']

In cases when we want to disable this behaviour we can set parameter
``split_inline_breaks`` to ``False``.

    >>> test_text = '- first param - second param'
    >>> text_parser = TextParser(test_text, split_inline_breaks=False)
    >>> text_parser.sentences
    ['- first param - second param.']

Please note that chars like ``.``, ``:``, ``?``, ``!`` are not considered
as inline breaks.

**inline_breaks**

In above example we saw how default char breaks by default work. In cases when
we want to split sentences by different char than default one, we can do so by
providing list of chars into ``inline_breaks`` parameter.

    >>> test_text = '> first param > second param'
    >>> text_parser = TextParser(test_text, inline_breaks=['> '])
    >>> text_parser.sentences
    ['First param.', 'Second param.']

Regex pattern is also supported as parameter value:

    >>> text_parser = TextParser(test_text, inline_breaks=[r'\b>'])

**sentence_separator**

In cases when we want output in text format, we can change how sentences
are merged together.

For example bellow is default output:

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> text_parser = TextParser(test_text)
    >>> text_parser.text
    First sentence? Second sentence. Third sentence.

Now lets change default value ``' '`` of ``sentence_separator`` to our
custom one.

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> text_parser = TextParser(test_text, sentence_separator=' > ')
    >>> text_parser.text
    First sentence? > Second sentence. > Third sentence.

**OTHER PARAMETERS**

There are also other parameters available which are currently not
documented. *Please refer for now to source code or tests to examine
their usage.*

Non documented parameters are:

* replace_keys
* remove_keys
* replace_keys_raw_text
* remove_keys_raw_text
* merge_sentences
* merge_keys
* feature_split_keys
* autodetect_html


parse_string
============
``parse_string`` is a helper method to normalize and manipulate simple
texts like titles or similar. It's also much performant than ``TextParser``
since it doesn't perform sentence split, capitalization by default ...
Basically it accepts string or float, int and returns normalized string.

Examples
--------
In this example lets normalize text with bad encoding.

    >>> from easytxt import parse_stringfrom easytxt.parsers import parse_string
    >>> test_text = 'Easybook Pro 13 &lt;3 uÌˆnicode'
    >>> parse_string(test_text)
    Easybook Pro 13 <3 ünicode

Floats, integers will get transformed to string automatically.

    >>> test_int = 123
    >>> parse_string(test_text)
    '123'

    >>> test_float = 123.12
    >>> parse_string(test_text)
    '123.12'

Custom parameters
-----------------
**normalize**

As seen in example above text normalization (fixing spaces, bad encoding) is
enabled by default through ``normalize`` parameter. Lets set ``normalize``
parameter to ``False`` to disable normalization.

    >>> test_text = 'Easybook Pro 13 &lt;3 uÌˆnicode'
    >>> parse_string(test_text)
    Easybook Pro 13 &lt;3 uÌˆnicode

**replace_keys**

We can replace chars/words in a string through ``replace_chars`` parameter.
``replace_chars`` can accept regex pattern as a lookup key and is not
case sensitive.

    >>> test_text = 'Easybook Pro 15'
    >>> parse_string(test_text, replace_keys=[('pro', 'Air'), ('15', '13')])
    Easybook Air 13

**remove_keys**

We can remove chars/words in a string through ``remove_keys`` parameter.
``remove_keys`` can accept regex pattern as a lookup key and is not
case sensitive.

    >>> test_text = 'Easybook Pro 15'
    >>> parse_string(test_text, remove_keys=['easy', 'pro'])
    book 15

**split_key**

Text can be split by ``split_key``. By default split index is ``0``.

    >>> test_text = 'easybook-pro_13'
    >>> parse_string(test_text, split_key='-')
    easybook

Lets specify split index through tuple.

    >>> test_text = 'pro_13'
    >>> parse_string(test_text, split_key=('-', -1))
    easybook

**split_keys**

``split_keys`` work in a same way as ``split_key`` but instead of single
split key it accepts list of keys.


    >>> test_text = 'easybook-pro_13'
    >>> parse_string(test_text, split_keys=[('-', -1), '_'])
    pro

**OTHER PARAMETERS**

There are also other parameters available which are currently not
documented. *Please refer for now to source code to examine their usage.*

Non documented parameters are:

* fix_spaces
* escape_new_lines
* new_line_replacement


Dependencies
============

`EasyTXT` relies on following libraries in some ways:

  * ftfy_ to fix encoding.
  * pyquery_ to help with html to text conversion.

.. _ftfy: https://pypi.org/project/ftfy/
.. _pyquery: https://pypi.org/project/pyquery/
