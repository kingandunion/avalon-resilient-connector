#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='avalon',
    version='1.0.0',
    license='MIT',
    author='King & Union',
    author_email='support@kingandunion.com',
    url='https://www.kingandunion.com/',
    description="Resilient Circuits Components for Avalon",
    long_description="Resilient Circuits Components for Avalon",
    install_requires=[
        'resilient_circuits>=30.0.0'
    ],
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
    ],

    # if you change any of these make sure you run:
    # pip install -e ./avalon/
    entry_points={
        "resilient.circuits.components": [
            "AvalonActions = avalon.components.avalon_actions:AvalonActions",
            "AvalonRefreshFunction = avalon.components.avalon_refresh:AvalonRefreshFunction"
        ],
        "resilient.circuits.configsection": ["gen_config = avalon.util.config:config_section_data"],
        "resilient.circuits.customize": ["customize = avalon.util.customize:customization_data"],
        "resilient.circuits.selftest": ["selftest = avalon.util.selftest:selftest_function"]
    }
)