+----------------------+------------------------------------------------------------+
| master branch status | |BuildStatus| |Docs| |MITLicense|                          |
+----------------------+------------------------------------------------------------+
| GitHub status        | |OpenIssues| |OpenPullRequests|                            |
+----------------------+------------+-----------------------------------------------+
| Versions             | NI-DMM     | |DMMLatestVersion| |DMMPythonVersion|         |
|                      +------------+-----------------------------------------------+
|                      | NI-ModInst | |ModInstLatestVersion| |ModInstPythonVersion| |
+----------------------+------------+-----------------------------------------------+
 
===========  =================================================================================================================
Info         Python bindings for NI Modular Instrument drivers. See `GitHub <https://github.com/ni/nimi-python/>`_ for the latest source.
Author       National Instruments
===========  =================================================================================================================

+-----------+-----------------------------------------------------------------------+
| WARNING!! | NI Modular Instruments Python API is currently under development. You |
|           | are welcome to use it, and we welcome feedback, but be prepared for   |
|           | changes to the APIs.                                                  |
+-----------+-----------------------------------------------------------------------+

.. _about-section:

About
=====

The **nimi-python** repository generates Python bindings (Application Programming Interface) for interacting with the Modular Instrument drivers. Currently, the following drivers are supported:

* NI-DMM (Python module: nidmm)

It is implemented as a set of `Mako templates <http://makotemplates.org>`_ and per-driver metafiles that produce a Python module for each driver. The driver is called through its public C API using the
`ctypes <https://docs.python.org/2/library/ctypes.html>`_ Python library.

**nimi-python** supports only the Windows operating system.

**nimi-python** supports CPython 3.6+. * TODO(marcoskirsch): Add PyPI version here.*

.. _installation-section:

Installation
============

In order to use nimi-python modules, you must install the corresponding driver runtime on your system. Visit `ni.com/downloads <http://www.ni.com/downloads/>`_ to download the latest driver version for your devices.

Specific Python bindings (i.e. for **NI-DMM**) can be installed with `pip <http://pypi.python.org/pypi/pip>`_::

  $ python -m pip install nidmm

Or **easy_install** from
`setuptools <http://pypi.python.org/pypi/setuptools>`_::

  $ python -m easy_install nidmm

You also can download the project source, build, and run::

  $ python TODO(marcoskirsch): how do we build?
  $ python setup.py install

.. _usage-section:

Usage
=====

The following is a basic example of using the **nidmm** module to open a session to a DMM and perform a 5.5 digits of resolution voltage measurement in the 10 V range.

.. code-block:: python

    import nidmm
    with nidmm.Session("Dev1") as session:
        session.configureMeasurementDigits(nidmm.Function.DC_VOLTS, 10, 5.5)
        print("Measurement: " + str(session.read()))

.. _support-section:

Support / Feedback
==================

The packages included in **nimi-python** package are supported by NI. For support, open
a request through the NI support portal at `ni.com <http://www.ni.com>`_.

.. _bugs-section:

Bugs / Feature Requests
=======================

To report a bug or submit a feature request, please use the
`GitHub issues page <https://github.com/ni/nimi-python/issues>`_.

Information to Include When Asking for Help
-------------------------------------------

Please include **all** of the following information when opening an issue:

- Detailed steps on how to reproduce the problem and full traceback, if
  applicable. Code samples are encouraged!

- The python version used::

  $ python -c "import sys; print(sys.version)"

- The module (i.e. **nidmm**) and its version::

  $ python -m pip list

- The version of the driver used (i.e. **NI-DMM 17.1**). Follow
  `this KB article <http://digital.ni.com/express.nsf/bycode/ex8amn>`_
  to determine the version you have installed.

- The operating system, version, and bitness. For example 64-bit Windows 7.

.. _documentation-section:

Documentation
=============

Documentation is available `here <http://nimi-python.readthedocs.io>`_.

Additional Documentation
========================

Refer to your driver documentation for device-specific information and detailed API documentation.

.. _license-section:

License
=======

**nimi-python** is licensed under an MIT-style license (see
`LICENSE <https://github.com/ni/nimi-python/blob/master/LICENSE>`_).
Other incorporated projects may be licensed under different licenses. All
licenses allow for non-commercial and commercial use.

.. |BuildStatus| image:: https://img.shields.io/travis/ni/nimi-python.svg
    :alt: Build Status - master branch
    :scale: 100%
    :target: https://travis-ci.org/ni/nimi-python

.. |Docs| image:: https://readthedocs.org/projects/nimi-python/badge/?version=latest
    :alt: Documentation Status - master branch
    :scale: 100%
    :target: https://nimi-python.readthedocs.io/en/latest/?badge=latest

.. |MITLicense| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :alt: MIT License
    :scale: 100%
    :target: https://opensource.org/licenses/MIT

.. |CoverageStatus| image:: https://coveralls.io/repos/github/ni/nimi-python/badge.svg?branch=master
    :alt: Test Coverage - master branch
    :scale: 100%
    :target: https://coveralls.io/github/ni/nimi-python?branch=master

.. |DMMLatestVersion| image:: http://img.shields.io/pypi/v/nidmm.svg
    :alt: Latest NI-DMM Version
    :scale: 100%
    :target: http://pypi.python.org/pypi/nidmm

.. |ModInstLatestVersion| image:: http://img.shields.io/pypi/v/nimodinst.svg
    :alt: Latest NI-ModInst Version
    :scale: 100%
    :target: http://pypi.python.org/pypi/nimodinst

.. |DMMPythonVersion| image:: http://img.shields.io/pypi/pyversions/nidmm.svg
    :alt: NI-DMM supported Python versions
    :scale: 100%
    :target: http://pypi.python.org/pypi/nidmm

.. |ModInstPythonVersion| image:: http://img.shields.io/pypi/pyversions/nimodinst.svg
    :alt: NI-ModInst supported Python versions
    :scale: 100%
    :target: http://pypi.python.org/pypi/nimodinst

.. |OpenIssues| image:: https://img.shields.io/github/issues/ni/nimi-python.svg
    :alt: Open Issues + Pull Requests
    :scale: 100%
    :target: https://github.com/ni/nimi-python/issues

.. |OpenPullRequests| image:: https://img.shields.io/github/issues-pr/ni/nimi-python.svg
    :alt: Open Pull Requests
    :scale: 100%
    :target: https://github.com/ni/nimi-python/pulls

..  |CoverageStatus|
