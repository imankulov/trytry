Project concepts
================

Try-try is the Django application which allows for developers to quite
easily create test flows. There is quite a lot of similar web services,
but the majority of them use browser-side javascript interpretation
of the language in question, which effectively limit the set of languages
to be interpreted that way.

Our apprach is to use "fair server-side intepreter" in isolated environment.
Every new session creates a virtual environment where users (believe you or not)
have superuser privileges.

Test writer writes a specially crafted :file:`steps.py` file, containing test
steps, one by one, and define the environment, which everything should be
executed.

See next modules of the documentation to get more detailed view about the
application and feel free to visit our http://www.try-try.me reference
installation.

