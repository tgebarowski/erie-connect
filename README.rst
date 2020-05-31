erie_connect - Erie Connect cloud client
========================================

.. image:: https://img.shields.io/pypi/v/erie_connect.svg
    :target: https://pypi.python.org/pypi/erie_connect
    :alt: Latest PyPI version

Unofficial Python client to interact with Erie Connect cloud to retrieve information from IQsoft 26 water softener.

Installation
------------

.. code-block:: bash

    [sudo] pip install erie_connect

Usage
-----

You can import the module as `erie_connect`.

Constructor
-----------

.. code-block:: python

    ErieConnect(
        username,
        password,
        auth,
        device
    )

``username`` and ``password`` are mandatory in order to be able to authenticate and get access token. 

If authorization info is already stored somewhere you may pass it directly to constructor, so that no extra step will be performed before querying for the data.
Similarly, Device info can be passed directly to the constructor to avoid selecting default device when invoking queries.

If auth and device are not set, both Auth and Device object will be stored upon first successful data fetching.

Requirements
^^^^^^^^^^^^

Python 3.7

Disclaimer 
-------------

This is an experimental library based on network traffic sniffing, made mainly for private purposes to integrate IQsoft 26 water softener with Home Assistant.

Authors
-------

`erie_connect` Python client was written by `Tomasz Gebarowski <gebarowski@gmail.com>`_.
