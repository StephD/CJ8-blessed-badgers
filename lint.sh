#!/bin/sh

black .
isort .
flake8
