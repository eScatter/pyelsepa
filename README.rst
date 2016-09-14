pyelsepa
========

This is a Python wrapper for the Fortran code ELSEPA, which does a "Dirac partial-wave calculation of elastic scattering of electrons and positrons by atoms, positive ions and molecules". ELSEPA is described in Sablat, Jablonski and Powell (2005) [1]_ (which is, sadly, behind a paywall). The Fortran source can be downloaded at Elsevier's Computer Physics Communications Program Library `adus_v1_0.tar.gz`_ under a researchers attribution type of license.

This Python wrapper uses `Docker`_ to wrap the Fortran code in a clean environment.

Requirements
~~~~~~~~~~~~

* `Python 3`_
* `NumPy`_
* `Pint`_
* `Docker`_

ELSEPA Docker image
~~~~~~~~~~~~~~~~~~~

To use the dockerized version of Elsepa, first make sure you have the *latest version* of `Docker`_ installed. If you are working in (a Debian/Ubuntu flavoured) GNU Linux, please follow the instructions in the `Docker installation manual`_.

To build the image, you should have downloaded the file `adus_v1_0.tar.gz`_, and placed it in the `docker` directory. Then from the `docker` directory (containing `Dockerfile`) run::

    docker build -t elsepa .

If you want to be sure that the container works, start an interactive session and run the :math:`H_2O` example::

    docker run -i -t elsepa
    ./elscatm < h2o.in

Installing
~~~~~~~~~~

We recommend installing `pyelsepa` in a Python virtual environment. Clone this repository and do::

    pip install .

or install it with user privileges::
    
    pip install . --user

Citation
~~~~~~~~

.. [1] Sablat, Jablonski and Powell, Computer Physics Communications, Volume 165, Issue 2, 15 January 2005, Pages 157–190, http://www.sciencedirect.com/science/article/pii/S0010465504004795

.. _`Python 3`: http://www.python.org/
.. _`NumPy`: http://www.numpy.org/
.. _`Pint`: https://pint.readthedocs.io
.. _`Docker`: http://www.docker.com/
.. _`Docker installation manual`: https://docs.docker.com/engine/installation/
.. _`adus_v1_0.tar.gz`: http://www.cpc.cs.qub.ac.uk/summaries/ADUS_v1_0.html
