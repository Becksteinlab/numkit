======
numkit
======

|docs| |build| |cov| |anaconda|

**numkit** is a small collection of numerical helper functions and
classes ("numerical first aid kit") that have been useful for
GromacsWrapper_ and related projects.

Originally, **numkit** was part of GromacsWrapper_ but was split off
into its own small package in version 0.7.0 of GromacsWrapper.

.. _GromacsWrapper: https://gromacswrapper.readthedocs.org/


Getting numkit
==============

Install with ``pip`` from PyPi with ::

    pip install numkit

or with ``conda`` from the *conda-forge* channel ::

   conda install -c conda-forge numkit

The source code is available under the BSD 3-clause license (see file
LICENSE) from GitHub in the repository
https://github.com/Becksteinlab/numkit ::

  git clone https://github.com/Becksteinlab/numkit

Python support
==============

Python 3 support for releases 3.9 - 3.12 is tested on Linux, macOS,
and Windows.

(Python 2.7 and older version of Python 3 were supported up to release 1.2.3.)

Contributing
============

Contributions are very welcome in all forms, especially through issue
reports and pull requests.

If you don't get an answer within 2 days, ping ``@orbeckst`` to send a
notification.


.. |build| image:: https://github.com/Becksteinlab/numkit/actions/workflows/ci.yaml/badge.svg?branch=main
   :alt: Build status
   :target: https://github.com/Becksteinlab/numkit/actions/workflows/ci.yaml
   
.. |docs| image:: https://readthedocs.org/projects/numkit/badge/?version=latest
   :target: https://numkit.readthedocs.org/en/latest/?badge=latest
   :alt: Documentation
   
.. |cov| image:: https://codecov.io/gh/Becksteinlab/numkit/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/Becksteinlab/numkit?branch=main
   :alt: Code Coverage

.. |anaconda| image:: https://anaconda.org/conda-forge/numkit/badges/version.svg
   :target: https://anaconda.org/conda-forge/numkit
   :alt: Anaconda package
