pyelsepa
========

This is a Python wrapper for the Fortran code ELSEPA, which does a "Dirac partial-wave calculation of elastic scattering of electrons and positrons by atoms, positive ions and molecules". ELSEPA is described in a paper by [Sablat, Jablonski and Powell (2005)](http://www.sciencedirect.com/science/article/pii/S0010465504004795) (which is, sadly, behind a paywall). The package can be downloaded at Elsevier's [Computer Physics Communications Program Library](http://www.cpc.cs.qub.ac.uk/summaries/ADUS_v1_0.html) under a researchers attribution type of license.

This Python wrapper uses [Docker](http://www.docker.com) to wrap the Fortran code in a clean environment.

Requirements
~~~~~~~~~~~~
* [Python 3](http://www.python.org/)
* [NumPy](http://www.numpy.org/)
* [Pint](https://pint.readthedocs.io)
* [Docker](http://www.docker.com/)

ELSEPA Docker image
~~~~~~~~~~~~~~~~~~~

To use the dockerized version of Elsepa, first make sure you have [Docker](http://docker.com) installed. If you are working in (a Debian/Ubuntu flavoured) GNU Linux, chances are that you can install Docker simply by doing::

    sudo apt install docker

To build the image, you should have downloaded the file [`adus_v1_0.tar.gz`](http://www.cpc.cs.qub.ac.uk/summaries/ADUS_v1_0.html), and placed it in the `docker` directory. Then from the `docker` directory (containing `Dockerfile`) run::

    docker build . -t elsepa

If you want to be sure that the container works, start an interactive session and run the H<sub>2</sub>O example::

    docker run -i -t elsepa
    ./elscatm < h2o.in
