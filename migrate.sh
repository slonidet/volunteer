#!/bin/bash

cd ./src/
git checkout 7df53af174fdeaa5ebb01b94ac6217fc217ffd71
python manage.py migrate
git checkout 8c5f1e38bf75fc365944c23d0329e1c484b24b96
python manage.py migrate
git checkout 0866ff96cce331065c06bbeec4b4b82e548613ca
python manage.py migrate
git checkout 713af75d3ab5fcb9d45e4d04009abc036aa19e25
python manage.py migrate
git checkout 8d7d971e233e00608f163657b94268f0728d60d0
python manage.py migrate
git checkout master
python manage.py migrate
