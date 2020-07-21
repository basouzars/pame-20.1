#!/bin/bash

packagesToInstall="grep -v -f <(pip freeze | perl -pe 's|\r?\n|\n|') <(cat requirements.txt | perl -pe 's|\r?\n|\n|')"
packagesToUninstall="grep -v -f <(cat requirements.txt | perl -pe 's|\r?\n|\n|') <(pip freeze | perl -pe 's|\r?\n|\n|')"


if [ "$1" = "check" ] ; then
  pylint="$(./docker.sh exec map-api "pylint --rcfile=.pylintrc */")"
  if ! [[ "$pylint" =~ "Your code has been rated at 10.00/10" ]]; then
    echo "$pylint"
    echo
    echo "Fix the problems above"
    exit 1
  fi

  install="$(./docker.sh exec map-api $packagesToInstall)"
  if [ "$install" != "" ] ; then
    echo "Some api packages must be installed:"
    echo $install
    echo
  fi

  uninstall="$(./docker.sh exec map-api $packagesToUninstall)"
  if [ "$uninstall" != "" ] ; then
    echo "Some api packages must be uninstalled:"
    echo $uninstall
    echo
  fi

  if [ "$install" != "" ] || [ "$uninstall" != "" ] ; then
    echo "Aborting..."
    exit 1
  fi

  makemigrations="$(./api.sh 'makemigrations --dry-run')"
  runmigrations="$(./api.sh showmigrations | grep '\[ \]')"

  if [ "$makemigrations" != "No changes detected" ] || [ "$runmigrations" != "" ] ; then
    echo "Make and run migrations. Aborting..."
    exit 1
  fi

  echo ok


elif [ "$1" = "install" ] ; then
  if [ "$2" = "" ] ; then
      echo "Missing parameter: pip packages"
      exit 1
  fi

  ./api.sh check
  ./docker.sh exec map-api "pip install ${@:2}"
  ./docker.sh exec map-api "pip freeze | perl -pe 's|\r?\n|\r\n|' > requirements.txt"


elif [ "$1" = "uninstall" ] ; then
  if [ "$2" = "" ] ; then
      echo "Missing parameter: pip packages"
      exit 1
  fi

  ./api.sh check
  ./docker.sh exec map-api "pip-autoremove ${@:2}"
  ./docker.sh exec map-api "pip freeze | perl -pe 's|\r?\n|\r\n|' > requirements.txt"


elif [ "$1" = "migrate" ] ; then
  if [ "$2" = "make" ] ; then
    ./docker.sh exec map-api "python manage.py makemigrations $3 $4"
  elif [ "$2" = "run" ] ; then
    ./docker.sh exec map-api "python manage.py migrate $3 $4"
  else
    ./docker.sh exec map-api "python manage.py makemigrations"
    ./docker.sh exec map-api "python manage.py migrate $2 $3"
  fi


elif [ "$1" = "update" ] ; then
  ./docker.sh exec map-api "$packagesToUninstall | xargs pip uninstall -y"
  ./docker.sh exec map-api "$packagesToInstall | xargs pip install"
  ./api.sh migrate


elif [ "$1" = "test" ] ; then
  [[ "$2" != "" ]] && tests="base.tests.$2" || tests=""
  ./docker.sh exec map-api "python manage.py test $tests --failfast"


elif [ "$1" != "" ] ; then
  [[ "$2" != "" ]] && container="$2" || container="map-api"
  ./docker.sh exec $container python manage.py $1


else
  echo "Missing command"
fi
