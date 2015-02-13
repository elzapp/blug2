#!/bin/bash

ENVDIR=".blugpy"

if [ ! -d $ENVDIR ]
then
  virtualenv $ENVDIR
fi
. $ENVDIR/bin/activate

if python -c "import django" 2>/dev/null
then
  echo "found django"
else
  pip install django
fi
if python -c "import yaml" 2>/dev/null
then
  echo "found yaml"
else
  pip install pyyaml
fi
if python -c "import pytz" >/dev/null
then
  echo "found pytz"
else
  pip install pytz
fi
export DJANGO_SETTINGS_MODULE=dsettings
