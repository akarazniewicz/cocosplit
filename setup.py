from setuptools import setup 

setup(
    packages=['cocosplit'],
    entry_points={
        'console_scripts':[
            'cocosplit=cocosplit.cocosplit:main'
        ]
    },
    url='https://github.com/themantalope/cocosplit'
)