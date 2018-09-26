=====
bfttl
=====

goal is to get tests working and then slowly evolve it more towards running on a ttl bus/clock.

Installation
------------

venvs are managed by the new standard pipenv to manage virtual environments
rather than virtualenvwrapper. Read more here:

http://docs.python-guide.org/en/latest/dev/virtualenvs/
https://docs.pipenv.org/

Install pipenv using::

    $ pacman -Syyu python-pipenv

Then clone the repo and install package + deps + dev-deps::

    $ git clone git@bitbucket.org:y2kbugger/BrainFuckTTL.git
    $ cd BrainFuckTTL
    $ pipenv install --dev


Testing
-------

The pytest suite can then be ran via::

    $ pipenv run pytest -f

or::

    $ pipenv shell
    (HTooze)$ pytest -f

Cleaning
--------

In order to run tests with a clean environment it may be necessary to remove cache and other files:

    $ git clean -idfx

Type 1 to clean if you have verified that you don't need any of the files shown.
