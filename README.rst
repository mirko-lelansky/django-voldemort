##################
django-voldemort
##################

This project is a django cache backend for the voldemort cluster.

=================
Implementation
=================

---------------
Dependencies
---------------

To build and run the project you need python 3. 
To build the documentation you need sphinx.
To run the test-suite you need pytest and tox.

---------------
Installation
---------------

To install this project run first :code:`python ./setup.py test` or :code:`tox`
to run the test suite. Then you can
run :code:`python ./setup.py install (--prefix [path])` to install the python
module to you system.

-----------
Usage
-----------

Before you can use the django cache extension you must ensure that the library
is successfully installed. After that you can use the voldemort cache system.
For that you need to modify your settings.py file and add a CACHE section. The
following code can be used as an example:

.. code:: python

    CACHES = {
        'default': {
            'BACKEND': 'django_voldemort.cache.VoldemortCache',
            'LOCATION': [('http://localhost:6666', 0)],
            'OPTIONS': {
                'store_name': "test"
            }
        }
    }

.

----
Api
----

The project documentation is in the folder doc. To build the documentation for
various output formats you can use the Makefile in the doc-folder. If you want
to build only html then you can use the following command
direct :code:`python ./setup.py build_sphinx` .

==============
Contributing
==============

========
License
========

The project is licensed under the Apache 2 License -
see the LICENSE.rst file for details.
