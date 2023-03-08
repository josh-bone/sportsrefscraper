# https://packaging.python.org/en/latest/guides/using-testpypi/
from setuptools import setup
import codecs
import os.path

"""
The below two functions were taken dirctly from 
    https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
    
They make it so the package version can be *only* specified in __init__.py
    Without them, we'd have to track it in both this file and that one.
"""
def read(rel_path):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(current_dir, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name='sportsrefscraper',
    version=get_version("sportsrefscraper/__init__.py"),   
    description='A Python package to scrape sports-reference.com for sports statistics',
    url='https://github.com/josh-bone/sportsrefscraper',
    author='Joshua Bone',
    author_email='jbone@bu.edu',
    license_files = ('LICENSE',),
    packages=['sportsrefscraper'],
    
    # TODO: remove the unidecode dependency
    install_requires=['pandas', 
                      'numpy',
                      'matplotlib',
                      'unidecode',
                      'bs4',
                      'requests'],  # pickle?

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
)
