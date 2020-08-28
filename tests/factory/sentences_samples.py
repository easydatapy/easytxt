english = [
    (
        'Mr. John and Ms. Sarah are here. Say hello!!!',
        [
            'Mr. John and Ms. Sarah are here.',
            'Say hello!!!'
        ]
    ),
    (
        ('Good morning Dr. Adams. The patient is waiting for you in room'
         ' number test@mail.com.'),
        [
            'Good morning Dr. Adams.',
            'The patient is waiting for you in room number test@mail.com.'
        ]
    ),
    (
        'uÌˆnicode Bad. HTML entities &lt;3!',
        [
            'Ünicode Bad.',
            'HTML entities <3!'
        ]
    ),
    (
        'first text!! Features: *    feature1 *feature2',
        [
            'First text!!',
            'Features: feature1.',
            'Feature2.'
        ]
    ),
    (
        ('The easytxt sunglasses stand out. Perfect look; they will embellish '
         'with a classy touch. <br><br>- Metal chain with snap-hook <br>'
         '- Metal easy logo on the stem'),
        [
            'The easytxt sunglasses stand out.',
            'Perfect look; they will embellish with a classy touch.',
            'Metal chain with snap-hook.',
            'Metal easy logo on the stem.'
        ]
    ),
    (
        'Sentence First\nSecond Sentence. Price 10.000.000,00!',
        ['Sentence First.', 'Second Sentence.', 'Price 10.000.000,00!']
    ),
    (
        'First sentence. Second sentence. Third Sentence!',
        ['First sentence.', 'Second sentence.', 'Third Sentence!']
    ),
    (
        '<p><strong>Sentence First</strong><br>Second Sentence</p>',
        ['Sentence First.', 'Second Sentence.']
    ),
    (
        ('<p><strong>Someone in Berlin: Foreign power divided'
         '<br></strong>Crisis is somewhere</p>'),
        [
            'Someone in Berlin: Foreign power divided.',
            'Crisis is somewhere.'
        ]
    ),
    (
        ('<p><strong>Someone in Berlin: Foreign power divided'
         '<br><br></strong> <br> <br><br>Crisis is somewhere</p>'),
        [
            'Someone in Berlin: Foreign power divided.',
            'Crisis is somewhere.'
        ]
    ),
    (
        '''
        Beautiful
        <ul>
            <li>* Next-generation Thunderbolt.</li>
            <li>* FaceTime HD camera </li>
            <li>* Multi-touch trackpad. </li>
        </ul>
        ''',
        [
            'Beautiful.',
            'Next-generation Thunderbolt.',
            'FaceTime HD camera.',
            'Multi-touch trackpad.'
        ]
    ),
    (
        ('<p><b>Juan Jacobo Árbenz Guzmán</b> (<small>Spanish pronunciation'
         ':&#160;</small><span title="Representation in the International P'
         'honetic Alphabet (IPA)" class="IPA"><a href="/wiki/Help:IPA/Spani'
         'sh" title="Help:IPA/Spanish">[xuan xaˈkoβo ˈaɾβenz ɣuzˈman]</a></'
         'span>; September 14, 1913&#160;&#8211;&#32;January 27, 1971) was '
         'a <a href="/wiki/Guatemala" title="Guatemala">Guatemalan</a> mili'
         'tary officer and politician who served as the 25th <a href="/wiki'
         '/President_of_Guatemala" title="President of Guatemala">President'
         ' of Guatemala</a>. He was <a href="/wiki/Ministry_of_Defence_(Gua'
         'temala)" title="Ministry of Defence (Guatemala)">Minister of Nati'
         'onal Defense</a>  from 1944 to 1951, and the second democraticall'
         'y elected President of Guatemala, from 1951 to 1954. He was a maj'
         'or figure in the ten-year <a href="/wiki/Guatemalan_Revolution" t'
         'itle="Guatemalan Revolution">Guatemalan Revolution</a>, which rep'
         'resented some of the few years of <a href="/wiki/Representative_d'
         'emocracy" title="Representative democracy">representative democra'
         'cy</a> in Guatemalan history. The landmark <a href="/wiki/Decree_'
         '900" title="Decree 900">program of agrarian reform</a> Árbenz ena'
         'cted as president was very influential across <a href="/wiki/Lati'
         'n_America" title="Latin America">Latin America</a>.<sup id="cite_'
         'ref-FOOTNOTEGleijeses19923_1-0" class="reference"><a href="#cite_'
         'note-FOOTNOTEGleijeses19923-1">&#91;1&#93;</a></sup></p>'),
        [
            ('Juan Jacobo Árbenz Guzmán ( Spanish pronunciation: [xuan xaˈk'
             'oβo ˈaɾβenz ɣuzˈman] ; September 14, 1913\xa0– January 27, 19'
             '71) was a Guatemalan military officer and politician who serv'
             'ed as the 25th President of Guatemala.'),
            ('He was Minister of National Defense from 1944 to 1951, and th'
             'e second democratically elected President of Guatemala, from '
             '1951 to 1954.'),
            ('He was a major figure in the ten-year Guatemala'
             'n Revolution , which represented some of the few years of rep'
             'resentative democracy in Guatemalan history.'),
            ('The landmark program of agrarian reform Árbenz enacted as pre'
             'sident was very influential across Latin America.')
        ]
    ),
    (
        ('<p class="body-text">There were some seriously <a class="body-link"'
         ' href="https://www.digitalspy.com/tv/ustv/a28290402/stranger-things'
         '-season-4-questions/" target="_blank" data-vars-ga-outbound-link="h'
         'ttps://www.digitalspy.com/tv/ustv/a28290402/stranger-things-season-'
         '4-questions/">big questions left hanging</a> following season three'
         '\'s explosive 77-minute finale, \'The Battle of Starcourt\'.<br></p'
         '>'),
         [
             ("There were some seriously big questions left hanging following"
              " season three's explosive 77-minute finale, 'The Battle of Sta"
              "rcourt'.")
         ]
    )
]
