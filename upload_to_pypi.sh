#!/bin/bash

pip install twine --upgrade
rm -rf dist/* *.egg-info
python setup.py sdist bdist_wheel
twine upload dist/*

