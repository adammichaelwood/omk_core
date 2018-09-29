========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
        | |landscape| |scrutinizer| |codacy| |codeclimate|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/omk_core/badge/?style=flat
    :target: https://readthedocs.org/projects/omk_core
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/openmusickit/omk_core.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/openmusickit/omk_core

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/openmusickit/omk_core?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/openmusickit/omk_core

.. |requires| image:: https://requires.io/github/openmusickit/omk_core/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/openmusickit/omk_core/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/openmusickit/omk_core/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/openmusickit/omk_core

.. |codecov| image:: https://codecov.io/github/openmusickit/omk_core/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/openmusickit/omk_core

.. |landscape| image:: https://landscape.io/github/openmusickit/omk_core/master/landscape.svg?style=flat
    :target: https://landscape.io/github/openmusickit/omk_core/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/REPLACE_WITH_PROJECT_ID.svg
    :target: https://www.codacy.com/app/openmusickit/omk_core
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/openmusickit/omk_core/badges/gpa.svg
   :target: https://codeclimate.com/github/openmusickit/omk_core
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/omk_core.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/omk_core

.. |commits-since| image:: https://img.shields.io/github/commits-since/openmusickit/omk_core/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/openmusickit/omk_core/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/omk_core.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/omk_core

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/omk_core.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/omk_core

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/omk_core.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/omk_core

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/openmusickit/omk_core/master.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/openmusickit/omk_core/


.. end-badges

Python Music Theory Library

* Free software: MIT license

Installation
============

::

    pip install omk_core

Documentation
=============


https://omk_core.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
