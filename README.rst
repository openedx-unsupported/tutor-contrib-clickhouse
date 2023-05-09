ClickHouse plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

A Tutor plugin for bring the `ClickHouse <https://clickhouse.com>`__ database to
the Tutor ecosystem.

This plugin is speculative and being used to test new Open edX analytics features.
It is not configured for production use at this time, use at your own risk!

See https://github.com/openedx/openedx-oars for more details.

Compatibility
-------------

This plugin is compatible with Tutor 15.0.0 and later.

Installation
------------

::

    pip install git+https://github.com/bmtcril/tutor-contrib-clickhouse

Usage
-----

::

    tutor plugins enable clickhouse


In case you want to use clickhouse-cloud you will need to disable the clickhouse 
service, and set the following environment variables:

::

    RUN_CLICKHOUSE: false
    CLICKHOUSE_SECURE_CONNECTION: true
    CLICKHOUSE_HOST: <clickhouse host>
    CLICKHOUSE_ADMIN_USER: <clickhouse admin user>
    CLICKHOUSE_ADMIN_PASSWORD: <clickhouse admin password>

License
-------

This software is licensed under the terms of the AGPLv3.
