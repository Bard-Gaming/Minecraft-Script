from setuptools import setup, find_packages
from minecraft_script.common import version
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

DESCRIPTION = 'Minecraft Script Programming language'

# Setting up
setup(
    name="minecraft_script",
    version=version,
    author="Joyful-Bard",
    author_email="<christophe@dronne.fr>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    package_data={'minecraft_script': [
        'lexer/grammar/*', 'config.json',
        'compiler/build_templates/*',
        'compiler/build_templates/math/*', 'compiler/build_templates/builtins/*',
        'compiler/build_templates/tags/*', 'compiler/build_templates/tags/blocks/*',
    ]},
    install_requires=[],
    keywords=['minecraft', 'mc', 'script', 'language'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)