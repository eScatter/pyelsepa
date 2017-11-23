pyelsepa
========

This is a Python wrapper for the Fortran code ELSEPA, which does a "Dirac partial-wave calculation of elastic scattering of electrons and positrons by atoms, positive ions and molecules". ELSEPA is described in Salvat, Jablonski and Powell (2005) [1]_ (which is, sadly, behind a paywall). The original Fortran source can be downloaded at Elsevier's Computer Physics Communications Program Library `adus_v1_0.tar.gz`_ under a researchers attribution type of license.

This Python wrapper relies on a slightly modified version of ELSEPA, which can be found on `github`_. The difference is in the use of an environment variable that allows us to run multiple instances of ELSEPA in parallel.

Requirements
~~~~~~~~~~~~

* `Python 3`_
* `NumPy`_
* `Pint`_
* `Modified ELSEPA`_

Installing
~~~~~~~~~~

We recommend installing `pyelsepa` in a Python virtual environment. Clone this repository and do::

    pip install .

or install it with user privileges::
    
    pip install . --user

By default, it is assumed that the ELSEPA binaries are located in ``/opt/elsepa`` and that the data is located in ``/opt/elsepa/data``.

Citation
~~~~~~~~

.. [1] Salvat, Jablonski and Powell, Computer Physics Communications, Volume 165, Issue 2, 15 January 2005, Pages 157–190, http://www.sciencedirect.com/science/article/pii/S0010465504004795

.. _`Python 3`: http://www.python.org/
.. _`NumPy`: http://www.numpy.org/
.. _`Pint`: https://pint.readthedocs.io
.. _`github`: https://github.com/eScatter/elsepa
.. _`Modified ELSEPA`: https://github.com/eScatter/elsepa
.. _`adus_v1_0.tar.gz`: http://www.cpc.cs.qub.ac.uk/summaries/ADUS_v1_0.html
