#!/bin/bash

ENVDIR=".blugpy"

if [ ! -d $ENVDIR ]
then
  virtualenv $ENVDIR
fi
. $ENVDIR/bin/activate

pip install django
pip install pyyaml
