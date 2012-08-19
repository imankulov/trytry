LXC configuration
=================

Default configuration
---------------------

Try-try security model takes advantage of LXC containers. You shouldn't care
about LXC installation, if you just installed the package to play around on your
localhost intend to setup the web service in a *very* trusted environment.

We assume that you have a virtual or a real (bare-metal) server with operating
system supporting LXC containers. The server is probably dedicated to try-try
project, you have root privileges to it (it is required). Instructions below
assume that configuration is made for Ubuntu distribuion.

First before, install the LXC package

.. code-block:: console

   $ sudo apt-get install lxc


On-boot container launch is redundant in our environment. Open the file
:file:`/etc/default/lxc` and change value ``LXC_AUTO`` from ``"true"`` to
``"false"``

The next step is to create one or more templates to work with. Create a new
file named :file:`lxc.conf` with just one line::

  lxc.network.type = empty

Then create a new base template with minimal Ubuntu installation.

.. code-block:: console

   $ sudo lxc-create -n try-try -t ubuntu -f lxc.conf -- --trim

Option ``--trim`` creates minimalistic installation of the system.

Then create and configure a bunch of clones of this distibution. Feel free to
create as much distributions as you like. It's fun

.. code-block:: console

   $ sudo lxc-clone -o try-try -n python
   $ sudo lxc-clone -o try-try -n php
   ...

As these template images don't have access to network, if you need extra
packages in there, you should install them by chrooting in the root directory.

For instance, below is a command which can be used to install PHP accessible
via command line in the image with the name "php"

.. code-block:: console

   $ sudo chroot /var/lib/lxc/php/rootfs bash -c 'apt-get update && apt-get install --yes --force-yes php5-cli'

Then you can check how it works by issuing the command

.. code-block:: console

   $ lxc-start -n php -- php -r '$foo = "hello world\n"; echo $foo;'
   hello world


For more information about LXC managing visit https://help.ubuntu.com/12.04/serverguide/lxc.html


Speed-up lxc cloning
--------------------

By default cloning a new environment takes about 10 seconds, but this
timespan can be significantly improved by leveraging btrfs snapshots.

.. code-block:: console

   # apt-get install btrfs-tools
   # mkfs.btrfs /dev/<device-name>
   # mount /dev/<device-name> /var/lib/lxc
   # echo "/dev/<device-name> /var/lib/lxc/ btrfs defaults 0 0" >> /etc/fstab

Enjoy watching the list of btrfs subvolumes while creating new virtual images

.. code-block:: console

   # btrfs subvolume list /var/lib/lxc/
