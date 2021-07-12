#!/bin/sh

# echo "** Running black"
# black .
# echo "** Running isort"
# isort .
# # echo "** Running flake8"
# # flake8
echo "** Running the pre-commit big boss"
pre-commit run --all-file
