import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'logthon',
    'python-telegram-bot',
    'python-dotenv'
]

setuptools.setup(
    name="botster",
    version="0.2.0",
    author="Giuseppe mastrobirraio Matranga",
    author_email="matrangagiuseppe99@gmail.com",
    description="A booster framework to verticalize Telegram bot development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mastrobirraio/botster",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['botster-cli=botster.cli.__main__:execute_from_commandline'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.6'
)
