# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='bfttl',
    version='0.1.0',
    description='brainfuck simulator to prototype the ttl machine',
    long_description=readme,
    author='Zak Kohler',
    author_email='git@y2kbugger.com',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    scripts=[],
    )
