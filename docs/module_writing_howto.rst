Module writing howto
====================

We hope you already familiarized with the system concept, and willing to
write some test flows for the application.

You don't need to start from scratch here, to simplify your job we prepared
an application template. Clone the repository from Github

.. code-block:: console

   $ git clone https://github.com/imankulov/try_app_template.git

Then, in the project directory, type:

.. code-block:: console

   $ ./manage.py startapp --template path/to/try_app_template my_app

A new app named `my_app` will be created, you should add it to the list of your
installed apps in :file:`settings.py` or :file:`localsettings.py`.

The core of the test application is the :file:`steps.py` file where a whole
test flow is described.

Below is a summary description of the file contents:

`__flow__` variable
-------------------

Flow variable describes the flow in a nutshell, and contains the links
to steps which should be done to successfully pass the test.

.. code-block:: python

   from trytry.core.utils.lxc import lxc_setup, lxc_teardown

   __flow__ = {
       # class names in this module, which will be used as steps
       'steps': ['Step1', 'Step2'],
       # the name of LXC container template which will be used to set up
       # a base container for your user.
       'lxc_container': 'python',
       # Setup and teardown functions. You can define them as functions or,
       # exactly like steps, as strings within your module.
       # Function accept one parameter: an initialized Flow object
       'setup': lxc_setup,
       'teardown': lxc_teardown,
       # the name of your module
       'name': 'Simple Bash',
       # The short name of your module, will be used as a part of urls in tests
       'url': 'simple_bash',
       # Detailed description of your module
       'description': __doc__,
   }


Step classes
------------

Step classes are ordinary classes, but it is more convenient to inherit them
from any generic step. There are three generic steps at your service:

- :class:`trytry.core.steps.GenericStep`: a generic step to execute an arbitrary
  command in a virtual LXC environment
- :class:`trytry.simple_bash.steps.GenericStep` a generic step to execute bash
  one-liners. Can store the state of variables between commands
- :class:`trytry.simple_python.steps.GenericStep` a generic step to execute Python
  one-liners. Can store the state of variables between commands


Setup and teardown functions
----------------------------

The test flow calls setup function before starting the first test in the flow.
the :func:`trytry.core.utils.lxc.lxc_setup` is a good way to start.

Likewise, tye test flow calls teardown function after all tests have been
completed, and the :func:`trytry.core.utils.lxc.lxc_teartown` should be used
as a `lxc_setup` counterpart.

