english = [
    ("easybook Pro 15", "easybook Pro 15"),
    (" Easybook    Pro 15 ", "Easybook Pro 15"),
    ("Easybook\nPro\n15", "Easybook Pro 15"),
    ("Easybook Pro 13 &lt;3 uÌˆnicode", "Easybook Pro 13 <3 ünicode"),
    (
        "\001\033[36;44mI&#x92;m blue, da ba dee da ba doo&#133;\033[0m",
        "I'm blue, da ba dee da ba doo…",
    ),
    ("", ""),
    (123, "123"),
    (0, "0"),
    (123.12, "123.12"),
    (0.15, "0.15"),
    (15.50, "15.5"),
    (True, "True"),
    (False, "False"),
    (None, ""),
]
