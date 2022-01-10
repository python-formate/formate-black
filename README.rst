==============
formate-black
==============

.. start short_desc

**Use black with formate.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/python-formate/formate-black/workflows/Linux/badge.svg
	:target: https://github.com/python-formate/formate-black/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/python-formate/formate-black/workflows/Windows/badge.svg
	:target: https://github.com/python-formate/formate-black/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/python-formate/formate-black/workflows/macOS/badge.svg
	:target: https://github.com/python-formate/formate-black/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/python-formate/formate-black/workflows/Flake8/badge.svg
	:target: https://github.com/python-formate/formate-black/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/python-formate/formate-black/workflows/mypy/badge.svg
	:target: https://github.com/python-formate/formate-black/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.herokuapp.com/github/python-formate/formate-black/badge.svg
	:target: https://dependency-dash.herokuapp.com/github/python-formate/formate-black/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/python-formate/formate-black/master?logo=coveralls
	:target: https://coveralls.io/github/python-formate/formate-black?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/python-formate/formate-black?logo=codefactor
	:target: https://www.codefactor.io/repository/github/python-formate/formate-black
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/formate-black
	:target: https://pypi.org/project/formate-black/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/formate-black?logo=python&logoColor=white
	:target: https://pypi.org/project/formate-black/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/formate-black
	:target: https://pypi.org/project/formate-black/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/formate-black
	:target: https://pypi.org/project/formate-black/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/python-formate/formate-black
	:target: https://github.com/python-formate/formate-black/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/python-formate/formate-black
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/python-formate/formate-black/v0.1.0
	:target: https://github.com/python-formate/formate-black/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/python-formate/formate-black
	:target: https://github.com/python-formate/formate-black/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2022
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/formate-black
	:target: https://pypi.org/project/formate-black/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``formate-black`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install formate-black

.. end installation

Hooks
--------

``formate-black`` provides a single hook for formate_, which allows the black_ code formatter to be used.


``black``
^^^^^^^^^^

Calls black_, using the given keyword arguments as its configuration.

This hook only takes keyword arguments.

The max line length can be provided via the ``line_length`` keyword argument
or in the config_ table as ``line_length``.

The indent can also be set to tabs via the ``use_tabs`` keyword argument
or in the config_ table as ``indent``.

.. _formate: http://formate.readthedocs.io/
.. _black: https://black.readthedocs.io/en/latest/
.. _config: https://formate.readthedocs.io/en/latest/configuration.html#config


Example Configuration
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: toml

	[hooks]
	reformat-generics = 40
	collections-import-rewrite = 20
	noqa-reformat = 60
	ellipsis-reformat = 70

	[hooks.black]
	priority = 50

	[hooks.black.kwargs]
	string_normalization = false
	magic_trailing_comma = false

	[config]
	indent = "\t"
	line_length = 115
