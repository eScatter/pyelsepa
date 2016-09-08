pyelsepa
========

This is a Python wrapper for the Fortran code ELSEPA, which does a "Dirac partial-wave calculation of elastic scattering of electrons and positrons by atoms, positive ions and molecules". ELSEPA is described in Sablat, Jablonski and Powell (2005) [1]_ (which is, sadly, behind a paywall). The Fortran source can be downloaded at Elsevier's Computer Physics Communications Program Library `adus_v1_0.tar.gz`_ under a researchers attribution type of license.

This Python wrapper uses [Docker](http://www.docker.com) to wrap the Fortran code in a clean environment.

Requirements
~~~~~~~~~~~~
* `Python 3`_
* `NumPy`_
* `Pint`_
* `Docker`_

ELSEPA Docker image
~~~~~~~~~~~~~~~~~~~

To use the dockerized version of Elsepa, first make sure you have `Docker`_ installed. If you are working in (a Debian/Ubuntu flavoured) GNU Linux, chances are that you can install Docker simply by doing::

    sudo apt install docker

To build the image, you should have downloaded the file `adus_v1_0.tar.gz`_, and placed it in the `docker` directory. Then from the `docker` directory (containing `Dockerfile`) run::

    docker build . -t elsepa

If you want to be sure that the container works, start an interactive session and run the H<sub>2</sub>O example::

    docker run -i -t elsepa
    ./elscatm < h2o.in

.. _`Python 3`: http://www.python.org/
.. _`NumPy`: http://www.numpy.org/
.. _`Pint`: https://pint.readthedocs.io
.. _`Docker`: http://www.docker.com/
.. _`adus_v1_0.tar.gz`: http://www.cpc.cs.qub.ac.uk/summaries/ADUS_v1_0.html
.. [1] Sablat, Jablonski and Powell, Computer Physics Communications, Volume 165, Issue 2, 15 January 2005, Pages 157–190, http://www.sciencedirect.com/science/article/pii/S0010465504004795
