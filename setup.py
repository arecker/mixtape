import setuptools


setuptools.setup(
    name='mixtape',
    version='0.0.0',
    url='https://github.com/arecker/mixtape.git',
    author='Alex Recker',
    author_email='alex@reckerfamily.com',
    description='the commandline mixtape manager',
    packages=['mixtape'],
    entry_points = {
        'console_scripts': ['mixtape=mixtape.__main__:main'],
    },
    install_requires=[
        'yt-dlp', # always latest
        'PyYAML==6.0.2',
        'mutagen==1.47.0',
    ],
    extras_require={
        'dev': [
            'jedi-language-server',
        ],
    },
)
