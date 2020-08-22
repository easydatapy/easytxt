english = [
    (
        '''
        <ul>
            <li>- color: Black</li>
            <li>- material: Aluminium</li>
        </ul>
        ''',
        [
            ('Color', 'Black'),
            ('Material', 'Aluminium')
        ]
    ),
    (
        '''
        <ul>
            <li><b>FEATURES</b></li>
            <li>- color  :  Black</li>
            <li>- material: Aluminium</li>
        </ul>
        ''',
        [('Color', 'Black'), ('Material', 'Aluminium')]
    ),
    (
        '- color: Black - material: Aluminium',
        [('Color', 'Black'), ('Material', 'Aluminium')]
    ),
    (
        '* color: Black * material: Aluminium',
        [('Color', 'Black'), ('Material', 'Aluminium')]
    ),
    (
        'Ignored text * color: Black - material: Aluminium. Ignore again',
        [('Color', 'Black'), ('Material', 'Aluminium')]
    ),
]
