from setuptools import setup, find_packages

setup(
    name='easytxt',
    version='0.0.4',
    description='Text manipulation and normalization library.',
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    author='Rok Grabnar',
    author_email='grabnarrok@gmail.com',
    url='https://github.com/sitegroove/easytxt',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'ftfy',
        'pyquery',
        'number-parser'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
