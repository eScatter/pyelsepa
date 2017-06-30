#!/usr/bin/env python

from setuptools import setup
from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyelsepa',
    version='0.1.1',
    long_description=long_description,
    description='Wrapper for ELSEPA: Dirac partial-wave calculation'
    ' of elastic scattering of electrons and positrons by atoms, positive'
    ' ions and molecules.',
    license='Apache v2',
    author='Johan Hidding',
    author_email='j.hidding@esciencecenter.nl',
    url='https://github.com/eScatter/pyelsepa.git',
    packages=['elsepa'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Physics'],
    install_requires=[
        'pint==0.8.1', 'numpy==1.13.0', 'docker==2.4.0', 'cslib', 'noodles[prov,numpy]==0.2.3'],
    extras_require={
        'test': ['pytest']
    },
)
