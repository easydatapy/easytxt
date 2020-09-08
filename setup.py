import re
from setuptools import setup, find_packages


(__version__, ) = re.findall(r"__version__.*\s*=\s*[\"]([^']+)[\"]",
                             open('easytxt/__init__.py').read())


setup(
    name='easytxt',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'ftfy',
        'pyquery',
        'number-parser'
    ]
)
