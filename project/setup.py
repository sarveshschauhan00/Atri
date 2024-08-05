
# setup.py

from setuptools import setup, find_packages

setup(
    name='tic_tac_toe',
    version='1.0.0',
    description='A simple human vs. human Tic Tac Toe game',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tic_tac_toe=main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    _requires='>=3.6',
)
