Python bindings to the FIWARE-IdM modified Keystone
===================================================

This is an extended client for the OpenStack Identity API, implemented by Keystone. It adds python bindings to the extra functionality added to Keystone through extensions implemented at `GING Keystone <http://github.com/ging/keystone>`_. The CLI part of the client is not binded, no work is done in that regard as is not a project-requirement at the time of this writting and because the OpenStack keystoneclient CLI is deprecated. If requested could be developed in the future, although probably as a contribution to `OpenStack Client <https://github.com/openstack/python-openstackclient>`_.

The master repository is on `GitHub <http://github.com/ging/python-keystoneclient>`_.

This code is a fork of `OpenStack KeystoneClient <http://github.com/openstack/python-keystoneclient>`_. The future goal is to contribute back all the bindings for the extensions that get accepted in Keystone from the complementary project `GING Keystone <http://github.com/ging/keystone>`_.

