Got root on ubuntu server?
Wanna try trytry?

Make sure all extra dependencies are installed and run:

fab -H root@my-server setup

If you want also use the LXC-based container installation, type also

fab -H root@my-server lxc_setup

You can probably want to use btrfs in order to speed-up snapshot creation,
then read the documentation: http://try-try.readthedocs.org/en/latest/lxc.html
