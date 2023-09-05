from setuptools import setup

setup(
    name="epicevents",
    version='0.1',
    py_modules=['epicevents.cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        epicevents=epicevents.cli:cli
    ''',)