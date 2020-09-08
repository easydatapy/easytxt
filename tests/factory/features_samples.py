english = [
    (
        """
        <ul>
            <li>- color: Black</li>
            <li>- material: Aluminium</li>
        </ul>
        """,
        [("Color", "Black"), ("Material", "Aluminium")],
    ),
    (
        """
        <ul>
            <li><b>FEATURES</b></li>
            <li>- color  :  Black</li>
            <li>- material: Aluminium</li>
        </ul>
        """,
        [("Color", "Black"), ("Material", "Aluminium")],
    ),
    (
        "- color: Black - material: Aluminium",
        [("Color", "Black"), ("Material", "Aluminium")],
    ),
    (
        "* color: Black * material: Aluminium",
        [("Color", "Black"), ("Material", "Aluminium")],
    ),
    (
        "Ignored text * color: Black - material: Aluminium. Ignore again",
        [("Color", "Black"), ("Material", "Aluminium")],
    ),
    (
        '<div data-feature-name="productOverview" data-csa-c-id="grr9d-d4ip31-ls'
        '8bb2-er6xco" data-cel-widget="productOverview_feature_div"><div><table>'
        "<tbody><tr><td>Type of product</td><td>Convertible</td></tr><tr><td>Voi"
        "ce command</td><td>Touchscreen</td></tr><tr><td>Operating System</td><t"
        "d>Windows 10</td></tr><tr><td>Wireless Communication Technology</td><td"
        ">Bluetooth, Wi-Fi</td></tr><tr><td>Brand</td><td>Lenovo</td></tr></tbod"
        'y></table> <script type="text/javascript">function logProductOverviewMe'
        "tric(metric) {if (typeof window.ue !== 'undefined' && typeof metric !"
        "== 'undefined' && typeof window.ue.count !== 'undefined') {window.u"
        "e.count(metric, ((window.ue.count(metric) || 0) + 1));}}if(window.ue &&"
        " ue.count) {logProductOverviewMetric('productOverviewDesktopRendered'"
        ');}if(window.ue && ue.tag){ue.tag("productoverviewtag");}</script></div'
        "></div>",
        [
            ("Type of product", "Convertible"),
            ("Voice command", "Touchscreen"),
            ("Operating System", "Windows 10"),
            ("Wireless Communication Technology", "Bluetooth, Wi-Fi"),
            ("Brand", "Lenovo"),
        ],
    ),
]
