=================================
Welcome to EasyTXT documentation!
=================================

EasyTXT is a set of high and low level modules to help you with text
normalization and manipulation.

**PLEASE NOTE:** *EasyTXT is still in alpha stage and some functionalities
could change without deprecation warning, although in current stage this is less
likely and class parameters should remain the same. For now it's discouraged
to use it in production (if so, then on your own risk) and is for testing
purposes only.*

.. contents::

Features
========

Some of the most important features that EasyTXT provide:

* normalizes text
* break text into normalized sentences
* break text into normalized features
* converts HTML to normalized text
* text manipulation (allow or deny sentences, etc.)
* fixes text encoding
* normalizes spaces
* converts html table data into sentences or features
* html table parser which returns dict of column row info
* autocomplete works with any method or function :)
* ...

There are many more features regarding which, please refer to the documentation
with lots of examples bellow.

Installation
============
::

    pip install easytxt

easytxt requires Python 3.6+.

parse_text
==========

Text examples
-------------
In this example lets parse badly structured text and output it into multiple
formats.

Please note that calling multiple formats at the same time won't affect
performance since sentences are cached and when calling other formats,
cached sentences will be used in a process.

.. code-block:: python

    >>> from easytxt import parse_text
    >>> test_text = '  first sentence... Bad uÌˆnicode.   HTML entities &lt;3!'
    >>> pt = parse_text(test_text)
    >>> pt.sentences
    ['First sentence...', 'Bad ünicode.', 'HTML entities <3!']

Lets just get normalized text.

.. code-block:: python

    >>> pt.text
    First sentence... Bad ünicode. HTML entities <3!

Here is example how to extract features from text.

.. code-block:: python

    >>> test_text = '- color: Black - material: Aluminium. Last Sentence'
    >>> pt = parse_text(test_text)

Text parser will try to automatically detect which are regular sentences and which
are features and show only extracted features when called ``features`` attr. By
default features would get capitalized in a same way as sentences.

.. code-block:: python

    >>> pt.features
    [('Color', 'Black'), ('Material', 'Aluminium')]

Return features dictionary instead a list of tuples.

.. code-block:: python

    >>> pt.features_dict
    {'Color': 'Black', 'Material': 'Aluminium'}

Let's get a value from a specific feature.

.. code-block:: python

    >>> pt.feature('color')
    Black

*We don't need to call ``features`` property first in order to get value
with ``feature`` since this is already done in a background. Features are
also cached in a similar way as sentences to increase performance in a case
we make multiple calls.*

Although regular sentences are ignored when calling ``features`` attr, they can
still be seen when calling ``sentences`` or ``text`` attr.

.. code-block:: python

    >>> pt.sentences
    ['Color: Black.', 'Material: Aluminium.', 'Last Sentence.']
    >>> pt.text
    Color: Black. Material: Aluminium. Last Sentence.

HTML examples
-------------
In this example we will try to parse html text. There is not special argument to be
passed into ``parse_text`` in order to process HTML. Usage is exactly the same as
for ``regular text`` since ``html`` is detected and processed automatically.

.. code-block:: python

    >>> test_text = '<p>Some sentence</p> <ul><li>* Easy <b>HD</b> camera </li></ul>'
    >>> pt = parse_text(test_text)
    >>> pt.sentences
    ['Some sentence.', 'Easy HD camera.']

One of the best features of using ``parse_text`` on ``html`` is that it can extract
table data into sentences. Lets get more info regarding this feature through example.

.. code-block:: python

    from easytxt import parse_text


    test_text_html = '''
        <p>Some paragraph demo text.</p>
        <table>
            <tbody>
                <tr>
                    <td scope="row">Type</td>
                    <td>Easybook Pro</td>
                </tr>
                <tr>
                    <td scope="row">Operating system</td>
                    <td>etOS</td>
                </tr>
            </tbody>
        </table>
        <div>Text after <strong>table</strong>.</div>
    '''

    tp = parse_text(test_text_html)

    print(tp.sentences)

In example above following sentences will be printed.

.. code-block:: python

    [
        'Some paragraph demo text.',
        'Type: Easybook Pro.',
        'Operating system: etOS.',
        'Text after table.'
    ]

Although in example we used table without header and with only two columns,
``parse_text`` can easily handle tables with a header and more than two columns.
Although it can parse table with infinite number of columns, it's not advised to
``parse_text`` since sentences with table data would become hard to read. To
extract data from a table with more complex structure ``parse_table`` is recommended
to be used since it can return results as a list of dictionaries.

Custom parameters
-----------------

**language**

If we are parsing text in other language than english then we need to
specify language parameter to which language our text belong to in order
for sentences to be split properly around abbreviations.

.. code-block:: python

    >>> test_text = 'primera oracion? Segunda oración. tercera oración'
    >>> pt = parse_text(test_text, language='es')
    >>> pt.sentences
    ['Primera oracion?', 'Segunda oración.', 'Tercera oración.']

Please note that currently only ``en`` and ``es`` language parameter values
are supported. *Support for more is coming soon...*

**css_query**

In cases that we provide html string, we can with ``css_query`` parameter
select from which html nodes text would get extracted.

.. code-block:: python

    >>> test_text = '<p>Some sentence</p> <ul><li>* Easy <b>HD</b> camera </li></ul>'
    >>> pt = parse_text(test_text, css_query='p')
    >>> pt.sentences
    ['Some sentence.']

**exclude_css**

In cases that we provide html string, we can through ``exclude_css`` parameter
limit from which html nodes would be excluded from parsing.

.. code-block:: python

    >>> test_text = '<p>Some sentence</p> <ul><li>* Easy <b>HD</b> camera </li></ul>'
    >>> pt = parse_text(test_text, exclude_css=['p', 'b'])
    >>> pt.sentences
    ['Easy camera.']

**allow**

We can control which sentences we want to get extracted by providing list of
keywords into ``allow`` parameter. Keys are not case sensitive.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> pt = parse_text(test_text, allow=['first', 'third'])
    >>> pt.sentences
    ['First sentence?', 'Third sentence.']

Regex pattern is also supported as parameter value:

.. code-block:: python

    >>> pt = parse_text(test_text, allow=[r'\bfirst'])

**callow**

``callow`` is similar to ``allow`` but with exception that provided keys
are case sensitive. Regex pattern as key is also supported.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> pt = parse_text(test_text, allow=['First', 'Third'])
    >>> pt.sentences
    ['Third sentence.']

**from_allow**

We can skip sentences by providing keys in ``from_allow`` parameter.
Keys are not case sensitive and regex pattern is also supported.

.. code-block:: python

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> pt = parse_text(test_text, from_allow=['second'])
    >>> pt.sentences
    ['Second txt.', 'Third Txt.', 'FOUR txt.']

**from_callow**

``from_callow`` is similar to ``from_allow`` but with exception that
provided keys are case sensitive. Regex pattern as key is also supported.

.. code-block:: python

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> pt = parse_text(test_text, from_callow=['Second'])
    >>> pt.sentences
    ['Second txt.', 'Third Txt.', 'FOUR txt.']

Lets recreate same example as before but with lowercase key.

.. code-block:: python

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> pt = parse_text(test_text, from_callow=['second'])
    >>> pt.sentences
    []

**to_allow**

``to_allow`` is similar to ``from_allow`` but in reverse order. Here
are sentences skipped after provided key is found. Keys are not case
sensitive and regex pattern is also supported.

.. code-block:: python

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> pt = parse_text(test_text, to_allow=['four'])
    >>> pt.sentences
    ['First txt.', 'Second txt.', 'Third Txt.']

**to_callow**

``to_callow`` is similar to ``to_allow`` but with exception that
provided keys are case sensitive. Regex pattern is also supported.

.. code-block:: python

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> pt = parse_text(test_text, to_callow=['FOUR'])
    >>> pt.sentences
    ['First txt.', 'Second txt.', 'Third Txt.']

Lets recreate same example as before but with lowercase key.

.. code-block:: python

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> pt = parse_text(test_text, to_callow=['four'])
    >>> pt.sentences
    ['First txt.', 'Second txt.', 'Third Txt.', 'FOUR txt.']

**deny**

We can control which sentences we don't want to get extracted by providing
list of keywords into ``deny`` parameter. Keys are not case sensitive and
regex pattern is also supported.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> pt = parse_text(test_text, deny=['first', 'third'])
    >>> pt.sentences
    ['Second sentence.']

**cdeny**

``cdeny`` is similar to ``deny`` but with exception that provided keys
are case sensitive. Regex pattern as a key is also supported.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> pt = parse_text(test_text, deny=['First', 'Third'])
    >>> pt.sentences
    ['First sentence?', 'Second sentence.']

**normalize**

By default parameter ``normalize`` is set to ``True``. This means that any
bad encoding will be automatically fixed, stops added and line breaks
split into sentences.

.. code-block:: python

    >>> from easytxt import parse_text
    >>> test_text = '  first sentence... Bad uÌˆnicode.   HTML entities &lt;3!'
    >>> pt = parse_text(test_text)
    >>> pt.sentences
    ['First sentence...', 'Bad ünicode.', 'HTML entities <3!']

Lets try to set parameter ``normalize`` to ``False`` and see what happens.

.. code-block:: python

    >>> from easytxt import parse_text
    >>> test_text = '  first sentence... Bad uÌˆnicode.   HTML entities &lt;3!'
    >>> pt = parse_text(test_text, normalize=False)
    >>> pt.sentences
    ['First sentence...', 'Bad uÌˆnicode.', 'HTML entities &lt;3!']

**capitalize**

By default all sentences will get capitalized as we can see bellow.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> pt = parse_text(test_text)
    >>> pt.sentences
    ['First sentence?', 'Second sentence.', 'third sentence.']

We can disable this behaviour by setting parameter ``capitalize`` to ``False``.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> pt = parse_text(test_text, capitalize=False)
    >>> pt.sentences
    ['first sentence?', 'Second sentence.', 'third sentence.']

**title**

We can set our text output to title by setting parameter ``title``
to ``True``.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> pt = parse_text(test_text, title=True)
    >>> pt.text
    'First Sentence? Second Sentence. Third Sentence'

**uppercase**

We can set our text output to uppercase by setting parameter ``uppercase``
to ``True``.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> pt = parse_text(test_text, uppercase=True)
    >>> pt.sentences
    ['FIRST SENTENCE?', 'SECOND SENTENCE.', 'THIRD SENTENCE.']

**lowercase**

We can set our text output to lowercase by setting parameter ``lowercase``
to ``True``.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> pt = parse_text(test_text, lowercase=True)
    >>> pt.text
    'first sentence? second sentence. third sentence'

**min_chars**

By default ``min_chars`` has a value of 5. This means that any sentence that has
less than 5 chars, will be filtered out and not seen at the end result. This
is done to remove ambiguous sentences, especially when extracting text from
html. We can raise or decrease this limit by changing the value of ``min_chars``.

**replace_keys**

We can replace all chars in a sentences by providing tuple of search key and
replacement char in a ``replace_keys`` parameter. Regex pattern as key is
also supported and search keys are not case sensitive.

.. code-block:: python

    >>> test_text = 'first sentence! - second sentence.  Third'
    >>> pt = parse_text(test_text, replace_keys=[('third', 'Last'), ('nce!', 'nce?')])
    >>> pt.sentences
    ['First sentence?', 'Second sentence.', 'Last.']

**remove_keys**

We can remove all chars in sentences by providing list of search keys in a
``replace_keys`` parameter. Regex pattern as key is also supported and keys
are not case sensitive.

.. code-block:: python

    >>> test_text = 'first sentence! - second sentence.  Third'
    >>> pt = parse_text(test_text, remove_keys=['sentence', '!'])
    >>> pt.sentences
    ['First.', 'Second.', 'Third.']

**replace_keys_raw_text**

We can replace char values before text is split into sentences. This is
especially useful if we want to fix text before it's parsed and so that
is split into sentences correctly. It accepts ``regex`` as key values in a
``tuple``. Please note that keys are not case sensitive and regex as key
is also accepted.

Lets first show default result with badly structured text without
setting keys into ``replace_keys_raw_text``.

.. code-block:: python

    >>> test_text = 'Easybook pro 15 Color: Gray Material: Aluminium'
    >>> pt = parse_text(test_text)
    >>> pt.sentences
    ['Easybook pro 15 Color: Gray Material: Aluminium.']

As we can see from the result test text is returned as one sentence
due to missing stop keys (``.``) between sentences. Lets fix this by
adding stop keys into unprocessed text before sentence splitting
happens.

.. code-block:: python

    >>> test_text = 'Easybook pro 15 Color: Gray Material: Aluminium'
    >>> replace_keys = [('Color:', '. Color:'), ('Material:', '. Material:')]
    >>> pt = parse_text(test_text, replace_keys_raw_text=replace_keys)
    >>> pt.sentences
    ['Easybook pro 15.', 'Color: Gray.', 'Material: Aluminium.']

**remove_keys_raw_text**

Works similar as ``replace_keys_raw_text``, but instead of providing list
of tuples in order to replace chars, here we provide list of chars to remove
keys. Lets try first on a sentence without setting keys to ``rremove_keys_raw_text``.
Please note that keys are not case sensitive and regex as key is also accepted.

.. code-block:: python

    >>> test_text = 'Easybook pro 15. Color: Gray'
    >>> pt = parse_text(test_text)
    >>> pt.sentences
    ['Easybook pro 15.', 'Color: Gray.']

Text above due to stop key ``.`` was split into two sentences. Lets prevent this
by removing color and stop key at the same time and get one sentence instead.

.. code-block:: python

    >>> test_text = 'Easybook pro 15. Color: Gray'
    >>> pt = parse_text(test_text, remove_keys_raw_text=['. color:'])
    >>> pt.sentences
    ['Easybook pro 15 Gray.']

**split_inline_breaks**

By default text with chars like ``*``, `` - `` and bullet points would get split
into sentences.

Example:

.. code-block:: python

    >>> test_text = '- first param - second param'
    >>> pt = parse_text(test_text)
    >>> pt.sentences
    ['First param.', 'Second param.']

In cases when we want to disable this behaviour, we can set parameter
``split_inline_breaks`` to ``False``.

.. code-block:: python

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

.. code-block:: python

    >>> test_text = '> first param > second param'
    >>> pt = parse_text(test_text, inline_breaks=['>'])
    >>> pt.sentences
    ['First param.', 'Second param.']

Regex pattern is also supported as parameter value:

.. code-block:: python

    >>> parse_text(test_text, inline_breaks=[r'\b>'])

**stop_key**

If a sentence is without a stop key at the end, then by default it
will automatically be appended ``.``. Let see this in bellow example:

.. code-block:: python

    >>> test_text = 'First feature <br> second feature?'
    >>> pt = parse_text(test_text)
    >>> pt.sentences
    ['First feature.', 'Second feature?']

We can change our default char ``.`` to a custom one by setting our
desired char in a ``stop_key`` parameter.

.. code-block:: python

    >>> test_text = 'First feature <br> second feature?'
    >>> pt = parse_text(test_text, stop_key='!')
    >>> pt.sentences
    ['First feature!', 'Second feature?']

**sentence_separator**

In cases when we want output in text format, we can change how sentences
are merged together.

Lets see first default output in example bellow:

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> pt = parse_text(test_text)
    >>> pt.text
    First sentence? Second sentence. Third sentence.

Behind the scene simple ``join`` on a list of sentences is performed.

Now lets change default value ``' '`` of ``sentence_separator`` to our
custom one.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> pt = parse_text(test_text, sentence_separator=' > ')
    >>> pt.text
    First sentence? > Second sentence. > Third sentence.

**text_num_to_numeric**

We can convert all alpha chars that describe numeric values to actual
numbers by setting ``text_num_to_numeric`` parameter to ``True``.

.. code-block:: python

    >>> test_text = 'First Sentence. Two thousand and three has it. Three Sentences.'
    >>> pt = parse_text(test_text, text_num_to_numeric=True)
    >>> pt.sentences
    ['1 Sentence.', '2003 has it.', '3 Sentences.']

If our text is in different language we need to change language value in
our ``language`` parameter. Currently supported languages regarding
``text_num_to_numeric`` are only ``en, es, hi and ru``.

Invoked methods
---------------

For examples bellow we will use following code as basis:

.. code-block:: python

    >>> test_text = 'First txt. Second txt.'
    >>> pt = parse_text(test_text)

**__str__**

Normally we would get text by calling ``text`` property:

.. code-block:: python

    >>> pt.text
    'First txt. Second txt.'

But we can avoid calling ``text`` property by ``str`` casting.

.. code-block:: python

    >>> str(pt)
    'First txt. Second txt.'

**__iter__**

Normally we would get sentences by calling ``sentence`` property:

.. code-block:: python

    >>> pt.sentences
    ['First txt.', 'Second txt.']

But we can avoid calling ``sentence`` property and use it directly
in iteration.

.. code-block:: python

    >>> [sentence for sentence in pt]
    ['First txt.', 'Second txt.']

Another alternative:

.. code-block:: python

    >>> list(pt)
    ['First txt.', 'Second txt.']

**__add__**

.. code-block:: python

    >>> pt + 'hello world'
    >>> pt.sentences
    ['First txt.', 'Second txt.', 'Hello World.']

    >>> pt + ['Hello', 'World!']
    >>> pt.sentences
    ['First txt.', 'Second txt.', 'Hello', 'World!']

**__radd__**

.. code-block:: python

    >>> 'hello world' + pt
    >>> pt.sentences
    ['Hello World.', 'First txt.', 'Second txt.']

    >>> ['Hello', 'World!'] + pt
    >>> pt.sentences
    ['Hello', 'World!', 'First txt.', 'Second txt.', 'Hello World.']


parse_string
============
``parse_string`` is a helper method to normalize and manipulate simple
texts like titles or similar. It's also more performant than ``parse_text``
since it doesn't perform sentence split, capitalization by default ...
Basically it accepts ``str``, ``float``, ``int`` and returns normalized string.

Examples
--------
In this example lets process text with bad encoding.

.. code-block:: python

    >>> from easytxt import parse_string
    >>> test_text = 'Easybook Pro 13 &lt;3 uÌˆnicode'
    >>> parse_string(test_text)
    Easybook Pro 13 <3 ünicode

Floats, integers will get transformed to string automatically.

.. code-block:: python

    >>> test_int = 123
    >>> parse_string(test_text)
    '123'

    >>> test_float = 123.12
    >>> parse_string(test_text)
    '123.12'

Custom parameters
-----------------
**normalize**

As seen in example above, text normalization (bad encoding) is
enabled by default through ``normalize`` parameter. Lets set ``normalize``
parameter to ``False`` to disable text normalization.

.. code-block:: python

    >>> test_text = 'Easybook Pro 13 &lt;3 uÌˆnicode'
    >>> parse_string(test_text)
    Easybook Pro 13 &lt;3 uÌˆnicode

**capitalize**

We can capitalize first character in our string if needed by setting
``capitalize`` parameter to ``True``. By default is set to ``False``.

.. code-block:: python

    >>> test_text = 'easybook PRO 15'
    >>> parse_string(test_text, capitalize=True)
    Easybook PRO 15

**title**

We can set all first chars in a word uppercase while other chars in a word
become lowercase with``title`` parameter set to ``True``.

.. code-block:: python

    >>> test_text = 'easybook PRO 15'
    >>> parse_string(test_text, title=True)
    Easybook Pro 15

**uppercase**

We can set all chars in our string to uppercase by ``uppercase``
parameter set to ``True``.

.. code-block:: python

    >>> test_text = 'easybook PRO 15'
    >>> parse_string(test_text, uppercase=True)
    EASYBOOK PRO 15

**lowercase**

We can set all chars in our string to lowercase by ``lowercase``
parameter set to ``True``.

.. code-block:: python

    >>> test_text = 'easybook PRO 15'
    >>> parse_string(test_text, lowercase=True)
    easybook pro 15

**replace_keys**

We can replace chars/words in a string through ``replace_chars`` parameter.
``replace_chars`` can accept regex pattern as a lookup key and is not
case sensitive.

.. code-block:: python

    >>> test_text = 'Easybook Pro 15'
    >>> parse_string(test_text, replace_keys=[('pro', 'Air'), ('15', '13')])
    Easybook Air 13

**remove_keys**

We can remove chars/words in a string through ``remove_keys`` parameter.
``remove_keys`` can accept regex pattern as a lookup key and is not
case sensitive.

.. code-block:: python

    >>> test_text = 'Easybook Pro 15'
    >>> parse_string(test_text, remove_keys=['easy', 'pro'])
    book 15

**split_key**

Text can be split by ``split_key``. By default split index is ``0``.

.. code-block:: python

    >>> test_text = 'easybook-pro_13'
    >>> parse_string(test_text, split_key='-')
    easybook

Lets specify split index through tuple.

.. code-block:: python

    >>> test_text = 'easybook-pro_13'
    >>> parse_string(test_text, split_key=('-', -1))
    pro_13

**split_keys**

``split_keys`` work in a same way as ``split_key`` but instead of single
split key it accepts list of keys.

.. code-block:: python

    >>> test_text = 'easybook-pro_13'
    >>> parse_string(test_text, split_keys=[('-', -1), '_'])
    pro

**take**

With ``take`` parameter we can limit maximum number that are shown
at the end result. Lets see how it works in example bellow.

.. code-block:: python

    >>> test_text = 'Easybook Pro 13'
    >>> parse_string(test_text, take=8)
    Easybook

**take**

With ``skip`` parameter we can skip ignore defined number of chars.
Lets see how it works in example bellow.

.. code-block:: python

    >>> test_text = 'Easybook Pro 13'
    >>> parse_string(test_text, skip=8)
    Pro 13

**text_num_to_numeric**

We can convert all alpha chars that describe numeric values to actual
numbers by setting ``text_num_to_numeric`` parameter to ``True``.

.. code-block:: python

    >>> test_text = 'two thousand and three words for the first time'
    >>> parse_string(test_text, text_num_to_numeric=True)
    2003 words for the 1 time

If our text is in different language we need to change language value in
our ``language`` parameter. Currently supported languages are only
``en, es, hi and ru``.

**fix_spaces**

By default all multiple spaces will be removed and left with only single
one between chars. Lets test it in our bellow example:

.. code-block:: python

    >>> test_text = 'Easybook   Pro  15'
    >>> parse_string(test_text)
    Easybook Pro 15

Now lets change ``fix_spaces`` parameter to ``False`` and see what happens.

.. code-block:: python

    >>> test_text = 'Easybook   Pro  15'
    >>> parse_string(test_text, fix_spaces=False)
    Easybook   Pro  15

**escape_new_lines**

By default all new line characters are converted to empty space as we can
see in example bellow:

.. code-block:: python

    >>> test_text = 'Easybook\nPro\n15'
    >>> parse_string(test_text)
    Easybook Pro 15

Now lets change ``escape_new_lines`` parameter to ``False`` and see what happens.

.. code-block:: python

    >>> test_text = 'Easybook\nPro\n15'
    >>> parse_string(test_text, escape_new_lines=False)
    Easybook\nPro\n15

**new_line_replacement**

If ``escape_new_lines`` is set to ``True``, then by default all new line chars
will be replaced by ``' '`` as seen in upper example. We can change this
default setting by changing value of ``new_line_replacement`` parameter.

.. code-block:: python

    >>> test_text = 'Easybook\nPro\n15'
    >>> parse_string(test_text, new_line_replacement='<br>')
    Easybook<br>Pro<br>15

**add_stop**

We can add stop char at the end of the string by setting ``add_stop``
parameter to ``True``.

.. code-block:: python

    >>> test_text = 'Easybook Pro  15'
    >>> parse_string(test_text, add_stop=True)
    Easybook Pro 15.

By default ``.`` is added but we can provide our custom char if needed. Instead
of setting ``add_stop`` parameter to ``True``, we can instead of boolean value
provide char as we can see in example bellow.

.. code-block:: python

    >>> test_text = 'Easybook Pro  15'
    >>> parse_string(test_text, add_stop='!')
    Easybook Pro 15!

parse_table
===========

``parse_table`` parses/extracts data from ``HTML`` table into various formats
like ``dict``, ``list`` or just ordinary ``text``.

Please note that ``parse_text`` already parses html tables but only in
``list`` or ``text`` format and will extract also text from other nodes
if ``css`` selector is not set directly on ``table`` node.

Examples
--------

In following examples we will use two tables. One with a header and one
without it.

.. code-block:: python

    from easytxt import parse_table


    test_text_html = '''
        <p>Some paragraph demo text.</p>
        <table>
            <tbody>
                <tr>
                    <td scope="row">Type</td>
                    <td>Easybook Pro</td>
                </tr>
                <tr>
                    <td scope="row">Operating system</td>
                    <td>etOS</td>
                </tr>
            </tbody>
        </table>
        <div>Text after <strong>table</strong>.</div>
    '''

    pt = parse_table(test_text_html)

    for row in pt:
        print(row)

In example above following row data will be printed.

.. code-block:: python

    {'Type': 'Easybook Pro'}
    {'Operating system': 'etOS'}

Alternatively we can get data also as sentences.

.. code-block:: python

    print(pt.sentences)

    [
        'Type: Easybook Pro',
        'Operating system: etOS'
    ]

Or a text.

.. code-block:: python

    print(pt.text)

    * Type: Easybook Pro * Operating system: etOS

As we can see, only table html will be extracted and by design other html nodes
are ignored, so that any ambiguous text isn't processed. If header isn't explicitly
specified with a ``th`` or a ``thead`` nodes, then ``parse_table`` will automatically
assume that provided table is without header data and it will take values from first
column as header info.

Lets make a test on a more complex table with a header and multiple columns.

.. code-block:: python

    from easytxt import parse_table


    test_text_html = '''
        <table>
            <tr>
                <th>Type</th>
                <th>OS</th>
                <th>Color</th>
            </tr>
            <tr>
                <td>Easybook 15</td>
                <td>etOS</td>
                <td>Gray</td>
            </tr>
            <tr>
                <td>Easyphone x1</td>
                <td>Mobile etOS</td>
                <td>Black</td>
            </tr>
            <tr>
                <td>Easywatch abc</td>
                <td>Mobile etOS</td>
                <td>Blue</td>
            </tr>
        </table>
    '''

    pt = parse_table(test_text_html)

    for row in pt:
        print(row)

In example above following row data will be printed.

.. code-block:: python

    {'Type': 'Easybook 15', 'OS': 'etOS', 'Color': 'Gray'}
    {'Type': 'Easyphone x1', 'OS': 'Mobile etOS', 'Color': 'Black'}
    {'Type': 'Easywatch abc', 'OS': 'Mobile etOS', 'Color': 'Blue'}

Lets get table data printed as sentences.

.. code-block:: python

    print(pt.sentences)

    [
        'Type/OS/Color: Easybook 15/etOS/Gray',
        'Type/OS/Color: Easyphone x1/Mobile etOS/Black',
        'Type/OS/Color: Easywatch abc/Mobile etOS/Blue'
    ]

Or a text.

.. code-block:: python

    print(pt.text)

    * Type/OS/Color: Easybook 15/etOS/Gray * Type/OS/Color: Easyphone x1/Mobile etOS/Black * Type/OS/Color: Easywatch abc/Mobile etOS/Blue

Lets get header keys only. It only works in a table with header nodes.

.. code-block:: python

    print(pt.headers)

    ['Type', 'OS', 'Color']

Custom parameters
-----------------

examples coming soon ...
*For now please refer to the source code*

Dependencies
============

`EasyTXT` relies on following libraries in some ways:

  * ftfy_ to fix encoding.
  * pyquery_ to help with html to text conversion.
  * number-parser_ to help with numeric text to number conversion

.. _ftfy: https://pypi.org/project/ftfy
.. _pyquery: https://pypi.org/project/pyquery
.. _number-parser: https://pypi.org/project/number-parser

Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Report Bugs
-----------

Report bugs at https://github.com/sitegroove/easytxt/issues.

If you are reporting a bug, please include:

* Your operating system name and ``EasyTXT`` package version.
* Whole text sample that is being parsed and custom parameters if being set.
* Parsed text result in various formats ``text``, ``senteces``, ``features``.

Fix Bugs
--------

Look through the GitHub issues for bugs. Anything tagged with “bug” is open
to whoever wants to implement it.

Implement Features
------------------

Look through the GitHub issues for features. Anything tagged with “feature”
is open to whoever wants to implement it. We encourage you to add new test
cases to existing stack.

Write Documentation
-------------------

``EasyTXT`` could always use more documentation, whether as part of the
official ``EasyTXT`` docs or even on the web in blog posts, articles,
tutorials, and such.

Submit Feedback
---------------

The best way to send feedback is to file an issue at
https://github.com/sitegroove/easytxt/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that contributions are welcome :)

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

* The pull request should include tests unless PR contains only changes
  to docs.
* If the pull request adds functionality, the docs should be updated. Docs
  currently live in a README.rst file.
* Follow the core developers’ advice which aim to ensure code’s consistency
  regardless of variety of approaches used by many contributors.
* In case you are unable to continue working on a PR, please leave a short
  comment to notify us. We will be pleased to make any changes required to
  get it done.


Note: *Contributing section was heavily inspired by dateparser package
contributing guidelines.*
