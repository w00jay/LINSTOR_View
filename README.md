# LINSTOR View
## A simple proof-of-concept SDS GUI

![LINSTOR View Animation](/LinView.gif "")

This is a barebones proof-of-concept for controlling
[LINSTOR](https://github.com/LINBIT/linstor-server)
software-defined-storage in a graphical manner.

The UI is provided by
[REMI](https://github.com/dddomodossola/remi)
and the
[LINSTOR](https://github.com/LINBIT/linstor-server)
is controlled by the
[LINSTOR Python API](https://github.com/LINBIT/linstor-api-py).  LINSTOR View uses only the PYTHON implementation and usage
of the API while the latest version offers REST API as well.

## Installation

### Install LINSTOR
You will need to install and provision a LINSTOR cluster and
backing storage first.  You can follow the first few steps in
[this guide](https://www.linbit.com/en/how-to-setup-linstor-in-openstack/)
to setup LINSTOR a controller and a satellite (both could be
on the same host with --node-type=Combined option).  Follow
the instructions in the 'Initial requirements' section.
LINSTOR distribution will also include the python API library
for LINSTOR.  The complete user guide is available
[here](https://docs.linbit.com/docs/users-guide-9.0/#s-common_administration).

### Install REMI
To install REMI, follow the instructions
[here](https://github.com/dddomodossola/remi#getting-started)
or it is as
`pip install remi` on the computer where LINSTOR controller
is running.

### Install LINSTOR View
Clone this repository onto the computer where LINSTOR
controller as well.
Edit the top sections in 'linview.py' containing some of the
defaults.  If you followed the steps from the blog post
mentioned above, change DEFAULT_VOL_GROUP line to
`DEFAULT_VOL_GROUP = 'drbdpool'`

### Starting up
Once all the setup is done, you can start the GUI by running
`python lin_view.py` from the LINSTOR View folder.  Then
point your browser to port 8008 of the LINSTOR controller.
Some of the working features include listing, creating, and
deleting LINSTOR resources from the main option.
