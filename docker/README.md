ELSEPA Docker image
===================

To use the dockerized version of Elsepa, first make sure you have the *latest version* of [Docker](http://docker.com) installed. 

To build the image, you should have downloaded the file [`adus_v1_0.tar.gz`](http://www.cpc.cs.qub.ac.uk/summaries/ADUS_v1_0.html), and placed it in this directory. Then run::

    docker build -t elsepa .

If you want to be sure that the container works, start an interactive session and run the H<sub>2</sub>O example::

    docker run -i -t elsepa
    ./elscatm < h2o.in

