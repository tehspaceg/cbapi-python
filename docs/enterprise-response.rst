.. _response_api:

Carbon Black Response REST API
==============================

This page documents the public interfaces exposed by cbapi when communicating with a Carbon Black Enterprise
Response server.

Main Interface
--------------

To use cbapi with Carbon Black Response, you will be using the CbEnterpriseResponseAPI.
The CbEnterpriseResponseAPI object then exposes two main methods to select data on the Carbon Black server:

.. autoclass:: cbapi.response.rest_api.CbEnterpriseResponseAPI
    :members:
    :inherited-members:

    .. :automethod:: select
    .. :automethod:: create

Queries
-------

.. autoclass:: cbapi.response.rest_api.Query
    :members:

Models
------
.. automodule:: cbapi.response.models
    :members:
    :inherited-members:
    :undoc-members:
