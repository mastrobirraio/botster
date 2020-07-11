import os
import sys

from setuptools import find_packages, setup
from setuptools.command.install import install

REQUIREMENTS = [
    'logthon',
    'python-telegram-bot',
    'python-dotenv'
]
VERSION = '0.2.1'


def readme():
    with open('README.md') as f:
        return f.read()


class VerifyVersionCommand(install):
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')
        if tag != VERSION:
            info = 'Git tag: {} does not match the version of this app: {}'.format(tag, VERSION)
            sys.exit(info)


setup(
    name="botster",
    version=VERSION,
    author="Giuseppe mastrobirraio Matranga",
    author_email="matrangagiuseppe99@gmail.com",
    description="A booster framework to verticalize Telegram bot development",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/mastrobirraio/botster",
    packages=find_packages(),
    entry_points={
        'console_scripts': ['botster-cli=botster.cli.__main__:execute_from_commandline'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS,
    python_requires='>=3.6',
    cmdclass={'verify': VerifyVersionCommand}
)
