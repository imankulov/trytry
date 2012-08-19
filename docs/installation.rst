Project Installation
====================

We should admit. The project is quite hard to install. And the first thing,
it is pretty much useless in Windows environment.

We tested its work on Debian, Ubuntu and Gentoo. Ubuntu should be considered
as the best variant for installing on, no matter locally or remotely.

Local installation
------------------

Local installation differs from remote one in that sense that it is considered
as "development" rather than production. Usually you don't need no LXC
containers, no special webserver, nothing like this. Just a plain old::

   $ ./manage.py runserver

Although even that it can be not easy to install.

So, there are the steps you need to make:

Clone the repository, create a new virtual environment, and install all the
dependencies

.. code-block:: console

   $ git clone https://github.com/imankulov/trytry.git
   $ cd ./trytry
   $ mkvirtualenv --system-site-packages trytry
   $ workon trytry
   $ pip install -r requirements.pip

Copy localsettings.py.example to localsettings.py and adjust it according
to your needs

.. code-block:: console

   $ cp -a trytry/localsettings.py.example trytry/localsettings.py
   $ editor trytry/localsettings.py

Type ``./manage.py trytry_sanity_check``. It is a special command which tries
to estimate the envornment it works within, and give some advice on how to
fix. Usually it asks to setup a timelimit system package, which is as trivial
as

.. code-block:: console

   $ sudo apt-get install timelimit

And then do

.. code-block:: console

   $ ./manage.py syncdb --migrate
   $ ./manage.py runserver

Then go to http://localhost:8000 . I hope it will work for you.

Okay, it's not very hard when it works, but if it doesn't .. yeah, it doesn't.


Remote installation
-------------------

We wrote a fabric script which is intender to transform your bare Ubuntu server
to a fully fledged try-try platform. The script and accompanying files reside
in the :file:`deploy` subdirectory of the project.

First before, make sure you have root ssh access to the server. Many
Ubuntu-based virtual servers don't provide SSH root access, assuming that
you use "sudo" when it is needed, but the fabric script we created won't work
unless you run it as root.

Then, review :file:`server_configs` directory, and change something according
to your needs.

Then, launch a basic setup installation command:

.. code-block:: console

   fab -H root@servername setup

The same command can be used to update the project. Then, providing you need
LXC setup, run:

.. code-block:: console

   fab -H root@servername lxc_setup

The command creates a number of LXC containers, as described in the to
of :file:`fabfile.py`.

Hopefully, it work out. If so, then visit the webpage of your remote server.
Nginx should respond with a funny collage of some geeky guys.
