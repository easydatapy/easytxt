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
        '''
        <ul><li>* FaceTime HD camera </li><li>* Multi-touch trackpad. </li></ul>
        ''',
        [
            'Next-generation Thunderbolt.',
            'FaceTime HD camera.',
            'Multi-touch trackpad.'
        ]
    )
]
