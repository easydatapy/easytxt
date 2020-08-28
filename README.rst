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

parse_text
==========

Text examples
-------------
In this example lets parse badly structured text and output it into multiple
formats.

Please note that calling multiple formats at the same time won't affect
performance since sentences are cached and all other formats call sentenced
under the hood.

    >>> from easytxt import parse_text
    >>> test_text = '  first sentence... Bad uÌˆnicode.   HTML entities &lt;3!'
    >>> pt = parse_text(test_text)
    >>> pt.sentences
    ['First sentence...', 'Bad ünicode.', 'HTML entities <3!']

Lets just get normalized text.

    >>> pt.text
    First sentence... Bad ünicode. HTML entities <3!

Here is example how to extract features from text.

    >>> test_text = 'Features - color: Black - material: Aluminium. Last Sentence'
    >>> pt = parse_text(test_text)

Text parser will try to automatically detect which are regular sentences and which
are features and show only extracted features when called ``features`` attr.

    >>> pt.features
    [('Color', 'Black'), ('Material', 'Aluminium')]

Return features dictionary instead a list of tuples.

    >>> pt.features_dict
    {'Color': 'Black', 'Material': 'Aluminium'}

Let's get a value from a specific feature.

    >>> pt.feature('color')
    Black

Although regular sentences are ignored when calling ``features`` attr, they can
still be seen when calling ``sentences`` or ``text`` attr.

    >>> pt.sentences
    ['Ignored text.', 'Color: Black.', 'Material: Aluminium.', 'Ignore again.']
    >>> pt.text
    Ignored text. Color: Black. Material: Aluminium. Ignore again.

HTML examples
-------------
In this example we will try to parse html text. There is not special argument to be
passed into ``parse_text`` in order to process HTML. Usage is exactly the same as
for ``regular text`` since ``html`` is detected and processed automatically.

    >>> test_text = '<p>Some sentence</p> <ul><li>* Easy <b>HD</b> camera </li></ul>'
    >>> pt = parse_text(test_text)
    >>> pt.sentences
    ['Some sentence.', 'Easy HD camera.']

Custom parameters
-----------------

**language**

If we are parsing text in other language than english then we need to
specify language parameter to which language our text belong to in order
for sentences to be split properly around abbreviations.

    >>> test_text = 'primera oracion? Segunda oración. tercera oración'
    >>> pt = parse_text(test_text, language='es')
    >>> pt.sentences
    ['Primera oracion?', 'Segunda oración.', 'Tercera oración.']

Please note that currently only ``en`` and ``es`` language parameter values
are supported. *Support for more is coming soon with automatic language
detection.*

**css_query**

In cases that we provide html string, we can through ``css_query`` parameter
select from which html node text would be extracted.

    >>> test_text = '<p>Some sentence</p> <ul><li>* Easy <b>HD</b> camera </li></ul>'
    >>> pt = parse_text(test_text, css_query='p')
    >>> pt.sentences
    ['Some sentence.']

**exclude_css**

In cases that we provide html string, we can through ``exclude_css`` parameter
limit from which html node text would be extracted.

    >>> test_text = '<p>Some sentence</p> <ul><li>* Easy <b>HD</b> camera </li></ul>'
    >>> pt = parse_text(test_text, exclude_css=['p', 'b'])
    >>> pt.sentences
    ['Easy camera.']

**allow**

We can control which sentences we want to get extracted by providing list of
keywords into ``allow`` parameter.

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> pt = parse_text(test_text, allow=['first', 'third'])
    >>> pt.sentences
    ['First sentence?', 'Third sentence.']

Regex pattern is also supported as parameter value:

    >>> pt = parse_text(test_text, allow=[r'\bfirst'])

**callow**

``callow`` is similar to ``allow`` but with exception that provided keys
are case sensitive. Regex pattern as key is also supported.

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> pt = parse_text(test_text, allow=['First', 'Third'])
    >>> pt.sentences
    ['Third sentence.']

**from_allow**

We can skip sentences by providing keys in ``from_allow`` parameter.
Regex pattern as key is also supported.

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> pt = parse_text(test_text, from_allow=['second'])
    >>> pt.sentences
    ['Second txt.', 'Third Txt.', 'FOUR txt.']

**from_callow**

``from_callow`` is similar to ``from_allow`` but with exception that
provided keys are case sensitive. Regex pattern as key is also supported.

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> pt = parse_text(test_text, from_callow=['Second'])
    >>> pt.sentences
    ['Second txt.', 'Third Txt.', 'FOUR txt.']

Lets recreate same example as before but with lowercase key.

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> pt = parse_text(test_text, from_callow=['second'])
    >>> pt.sentences
    []

**to_allow**

``to_allow`` is similar to ``from_allow`` but in reverse order. Here
are sentences skipped after provided key is found. Regex pattern as key
is also supported.

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> pt = parse_text(test_text, to_allow=['four'])
    >>> pt.sentences
    ['First txt.', 'Second txt.', 'Third Txt.']

**to_callow**

``to_callow`` is similar to ``to_allow`` but with exception that
provided keys are case sensitive. Regex pattern as key is also supported.

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> pt = parse_text(test_text, to_callow=['FOUR'])
    >>> pt.sentences
    ['First txt.', 'Second txt.', 'Third Txt.']

Lets recreate same example as before but with lowercase key.

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> pt = parse_text(test_text, to_callow=['four'])
    >>> pt.sentences
    ['First txt.', 'Second txt.', 'Third Txt.', 'FOUR txt.']

**deny**

We can control which sentences we don't want to get extracted by providing
list of keywords into ``deny`` parameter. Regex pattern as key is also supported.

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> pt = parse_text(test_text, deny=['first', 'third'])
    >>> pt.sentences
    ['Second sentence.']

**cdeny**

``cdeny`` is similar to ``deny`` but with exception that provided keys
are case sensitive. Regex pattern as key is also supported.

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> pt = parse_text(test_text, deny=['First', 'Third'])
    >>> pt.sentences
    ['First sentence?', 'Second sentence.']

**normalize**

By default parameter ``normalize`` is set to ``True``. This means that any
bad encoding will be automatically fixed, stops added and line breaks
split into sentences.

    >>> from easytxt import parse_text
    >>> test_text = '  first sentence... Bad uÌˆnicode.   HTML entities &lt;3!'
    >>> pt = parse_text(test_text)
    >>> pt.sentences
    ['First sentence...', 'Bad ünicode.', 'HTML entities <3!']

Lets try to set parameter ``normalize`` to ``False`` and see what happens.

    >>> from easytxt import parse_text
    >>> test_text = '  first sentence... Bad uÌˆnicode.   HTML entities &lt;3!'
    >>> pt = parse_text(test_text, normalize=False)
    >>> pt.sentences
    ['First sentence...', 'Bad uÌˆnicode.', 'HTML entities &lt;3!']

**capitalize**

By default all sentences will get capitalized as we can see bellow.

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> pt = parse_text(test_text)
    >>> pt.sentences
    ['First sentence?', 'Second sentence.', 'Third sentence.']

We can disable this behaviour by setting parameter ``capitalize`` to ``False``.

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> pt = parse_text(test_text, capitalize=False)
    >>> pt.sentences
    ['first sentence?', 'Second sentence.', 'third sentence.']

**uppercase**

We can set our text output to uppercase by setting parameter ``uppercase``
to ``True``.

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> pt = parse_text(test_text, capitalize=False)
    >>> pt.sentences
    ['FIRST SENTENCE?', 'SECOND SENTENCE.', 'THIRD SENTENCE.']

**lowercase**

We can set our text output to lowercase by setting parameter ``lowercase``
to ``True``.

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> pt = parse_text(test_text, capitalize=False)
    >>> pt.text
    'first sentence? second sentence. third sentence'

**min_chars**

description coming soon ...

**replace_keys**

We can replace all chars in sentences by providing tuple of key and
replacement char in a ``replace_keys`` parameter. Regex pattern as key is
also supported.

    >>> test_text = 'first sentence! - second sentence.  Third'
    >>> pt = parse_text(test_text, replace_keys=[('third', 'Last'), ('nce!', 'nce?')])
    >>> pt.sentences
    ['First sentence?', 'Second sentence.', 'Last.']

**remove_keys**

We can remove all chars in sentences by providing list keys in a
``replace_keys`` parameter. Regex pattern as key is also supported.

    >>> test_text = 'first sentence! - second sentence.  Third'
    >>> pt = parse_text(test_text, remove_keys=['sentence', '!'])
    >>> pt.sentences
    ['First.', 'Second.', 'Third.']

**replace_keys_raw_text**

examples coming soon ...

**remove_keys_raw_text**

examples coming soon ...

**split_inline_breaks**

By default text with chars like ``*``, `` - `` and bullet points would get split
into sentences.

Example:

    >>> test_text = '- first param - second param'
    >>> pt = parse_text(test_text)
    >>> pt.sentences
    ['First param.', 'Second param.']

In cases when we want to disable this behaviour we can set parameter
``split_inline_breaks`` to ``False``.

    >>> test_text = '- first param - second param'
    >>> pt = parse_text(test_text, split_inline_breaks=False)
    >>> pt.sentences
    ['- first param - second param.']

Please note that chars like ``.``, ``:``, ``?``, ``!`` are not considered
as inline breaks.

**inline_breaks**

In above example we saw how default char breaks by default work. In cases when
we want to split sentences by different char than default one, we can do so by
providing list of chars into ``inline_breaks`` parameter.

    >>> test_text = '> first param > second param'
    >>> pt = parse_text(test_text, inline_breaks=['> '])
    >>> pt.sentences
    ['First param.', 'Second param.']

Regex pattern is also supported as parameter value:

    >>> parse_text(test_text, inline_breaks=[r'\b>'])

**stop_key**

If a sentence is without a stop key at the end, then by default it
will automatically be appended ``.``. Let see this in bellow example:

    >>> test_text = 'First feature <br> second feature?'
    >>> pt = parse_text(test_text)
    >>> pt.sentences
    ['First feature.', 'Second feature?']

We can change our default char ``.`` to a custom one by setting our
desired char in a ``stop_key`` parameter.

    >>> test_text = 'First feature <br> second feature?'
    >>> pt = parse_text(test_text, stop_key='!')
    >>> pt.sentences
    ['First feature!', 'Second feature?']

**stop_keys_ignore**

examples coming soon ...

**sentence_separator**

In cases when we want output in text format, we can change how sentences
are merged together.

For example bellow is default output:

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> pt = parse_text(test_text)
    >>> pt.text
    First sentence? Second sentence. Third sentence.

Now lets change default value ``' '`` of ``sentence_separator`` to our
custom one.

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> pt = parse_text(test_text, sentence_separator=' > ')
    >>> pt.text
    First sentence? > Second sentence. > Third sentence.

**text_num_to_numeric**

examples coming soon ..

**autodetect_html**

examples coming soon ..

Invoked methods
---------------

For examples bellow we will use following code as basis:

    >>> test_text = 'First txt. Second txt.'
    >>> pt = parse_text(test_text)

**__str__**

Normally we would get text by calling ``text`` property:

    >>> pt.text
    'First txt. Second txt.'

But we can avoid calling ``text`` property by ``str`` casting.

    >>> str(pt)
    'First txt. Second txt.'

**__iter__**

Normally we would get sentences by calling ``sentence`` property:

    >>> pt.sentences
    ['First txt.', 'Second txt.']

But we can avoid calling ``sentence`` property and use it directly
in iteration.

    >>> [sentence for sentence in pt]
    ['First txt.', 'Second txt.']

Another alternative:

    >>> list(pt)
    ['First txt.', 'Second txt.']

**__add__**

    >>> pt + 'hello world'
    >>> pt.sentences
    ['First txt.', 'Second txt.', 'Hello World.']

    >>> pt + ['Hello', 'World!']
    >>> pt.sentences
    ['First txt.', 'Second txt.', 'Hello', 'World!']

**__radd__**

    >>> 'hello world' + pt
    >>> pt.sentences
    ['Hello World.', 'First txt.', 'Second txt.']

    >>> ['Hello', 'World!'] + pt
    >>> pt.sentences
    ['Hello', 'World!', 'First txt.', 'Second txt.', 'Hello World.']


parse_string
============
``parse_string`` is a helper method to normalize and manipulate simple
texts like titles or similar. It's also much performant than ``parse_text``
since it doesn't perform sentence split, capitalization by default ...
Basically it accepts string or float, int and returns normalized string.

Examples
--------
In this example lets normalize text with bad encoding.

    >>> from easytxt import parse_string
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

**capitalize**

We can capitalize first character in our string if needed by setting
``capitalize`` parameter to ``True``. By default is set to ``False``.

    >>> test_text = 'easybook PRO 15'
    >>> parse_string(test_text, capitalize=True)
    Easybook PRO 15

**uppercase**

We can set all chars in our string to uppercase by setting ``uppercase``
parameter to ``True``.

    >>> test_text = 'easybook PRO 15'
    >>> parse_string(test_text, uppercase=True)
    EASYBOOK PRO 15

**lowercase**

We can set all chars in our string to lowercase by setting ``lowercase``
parameter to ``True``.

    >>> test_text = 'easybook PRO 15'
    >>> parse_string(test_text, lowercase=True)
    easybook pro 15

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

    >>> test_text = 'easybook-pro_13'
    >>> parse_string(test_text, split_key=('-', -1))
    pro_13

**split_keys**

``split_keys`` work in a same way as ``split_key`` but instead of single
split key it accepts list of keys.


    >>> test_text = 'easybook-pro_13'
    >>> parse_string(test_text, split_keys=[('-', -1), '_'])
    pro

**text_num_to_numeric**

We can convert all alpha chars that describe numeric values to actual
numbers by setting ``text_num_to_numeric`` parameter to ``True``.

    >>> test_text = 'two thousand and three words for the first time'
    >>> parse_string(test_text, text_num_to_numeric=True)
    2003 words for the 1 time

If our text is in different language we need to change language value in
our ``language`` parameter. Currently supported languages are only
``en, es, hi and ru``.

**fix_spaces**

By default all multiple spaces will be removed and left with only single
one between chars. Lets test it in our bellow example:

    >>> test_text = 'Easybook   Pro  15'
    >>> parse_string(test_text)
    Easybook Pro 15

Now lets change ``fix_spaces`` parameter to ``False`` and see what happens.

    >>> test_text = 'Easybook   Pro  15'
    >>> parse_string(test_text, fix_spaces=False)
    Easybook   Pro  15

**escape_new_lines**

By default all new line characters are converted to empty space as we can
see in example bellow:

    >>> test_text = 'Easybook\nPro\n15'
    >>> parse_string(test_text)
    Easybook Pro 15

Now lets change ``escape_new_lines`` parameter to ``False`` and see what happens.

    >>> test_text = 'Easybook\nPro\n15'
    >>> parse_string(test_text, escape_new_lines=False)
    Easybook\nPro\n15

**new_line_replacement**

If ``escape_new_lines`` is set to ``True``, then by default all new line chars
will be replaced by ``' '`` as seen in upper example. We can change this
default setting by changing value of ``new_line_replacement`` parameter.

    >>> test_text = 'Easybook\nPro\n15'
    >>> parse_string(test_text, new_line_replacement='<br>')
    Easybook<br>Pro<br>15

**add_stop**

We can add stop char at the end of the string by setting ``add_stop``
parameter to ``True``.

    >>> test_text = 'Easybook Pro  15'
    >>> parse_string(test_text, add_stop=True)
    Easybook Pro 15.

By default ``.`` is added but we can provide our custom char if needed. Instead
of setting ``add_stop`` parameter to ``True``, we can instead of boolean value
provide char as we can see in example bellow.

    >>> test_text = 'Easybook Pro  15'
    >>> parse_string(test_text, add_stop='!')
    Easybook Pro 15!

parse_table
===========

description coming soon ...

Examples
--------

description coming soon ...

Custom parameters
-----------------

**pq**

description coming soon ...

**allow_cols**

description coming soon ...

**callow_cols**

description coming soon ...

**deny_cols**

description coming soon ...

**cdeny_cols**

description coming soon ...

**separator**

description coming soon ...

**header**

description coming soon ...

**skip_row_without_value**

description coming soon ...

Dependencies
============

`EasyTXT` relies on following libraries in some ways:

  * ftfy_ to fix encoding.
  * pyquery_ to help with html to text conversion.
  * number-parser_ to help with numeric text to number conversion

.. _ftfy: https://pypi.org/project/ftfy
.. _pyquery: https://pypi.org/project/pyquery
.. _number-parser: https://pypi.org/project/number-parser