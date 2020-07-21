#!/bin/bash

root="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


if [ "$1" = "up" ] ; then
  api_up="docker-compose -f $root/api/docker-compose.local.yml up"
  site_up="docker-compose -f $root/site/docker-compose.local.yml up"

  if [ "$(uname)" = "Darwin" ] ; then
    osascript -e "
      tell app \"Terminal\"
        do script \"$api_up\"
      end tell
    " >> /dev/null 2>&1
    osascript -e "
      tell app \"Terminal\"
        do script \"$site_up\"
      end tell
    " >> /dev/null 2>&1
  else
    /git-bash.exe -c "$api_up" &
    /git-bash.exe -c "$site_up" &
  fi


elif [ "$1" = "down" ] ; then
  docker-compose -f $root/api/docker-compose.local.yml down
  docker-compose -f $root/site/docker-compose.local.yml down


elif [ "$1" = "deploy" ] ; then
  if [ "$2" = "--prod" ] ; then
    docker-compose -p prod-api -f $root/api/docker-compose.prod.yml up -d
    docker-compose -p prod-site -f $root/site/docker-compose.prod.yml up -d
  elif [ "$2" = "--stage" ] ; then
    docker-compose -p stage-api -f $root/api/docker-compose.stage.yml up -d
    docker-compose -p stage-site -f $root/site/docker-compose.stage.yml up -d
  else
    echo "Warning: do not run this command locally"
  fi


elif [ "$1" = "undeploy" ] ; then
  if [ "$2" = "--prod" ] ; then
    docker-compose -p prod-site -f $root/site/docker-compose.prod.yml down
    docker-compose -p prod-api -f $root/api/docker-compose.prod.yml down
  elif [ "$2" = "--stage" ] ; then
    docker-compose -p stage-site -f $root/site/docker-compose.stage.yml down
    docker-compose -p stage-api -f $root/api/docker-compose.stage.yml down
  else
    echo "Warning: do not run this command locally"
  fi


elif [ "$1" = "logs" ] ; then
  if [ "$2" = "" ] ; then
    echo "Missing parameter: docker container"
    exit 1
  fi

  docker logs --tail 20 $2


elif [ "$1" = "bash" ] ; then
  if [ "$2" = "" ] ; then
    echo "Missing parameter: container id"
    exit 1
  fi

  docker exec -ti $2 //bin//bash


elif [ "$1" = "exec" ] ; then
  if [ "$2" = "" ] ; then
    echo "Missing parameter: container id"
    exit 1
  fi

  if [ "$3" = "" ] ; then
    echo "Missing parameter: exec command"
    exit 1
  fi

  echo "${@:3}" | docker exec -i $2 //bin//bash


else
  echo "Command not found: $1"
fi
