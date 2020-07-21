#!/bin/bash

if [ "$1" = "update" ] ; then
  ./docker.sh exec map-site "npm install"


else
  echo "Command not found: $1"
fi
