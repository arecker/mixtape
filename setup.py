from setuptools import setup
setup(
    entry_points = {
        'console_scripts': ['mixtape=mixtape.__main__:main'],
    },
    name='mixtape',
    install_requires=[
        'python-slugify==8.0.4',
        'yt-dlp==2024.12.23',
    ],
    extras_require={
        'dev': [
            'ipdb',
            'ipython',
            'isort',
            'jedi-language-server',
            'pyflakes',
        ]
    }
)
