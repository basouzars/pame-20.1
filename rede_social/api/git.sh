#!/bin/bash


function detect-conflict {
  CONFLICTS=$(git ls-files -u | wc -l)
  if [ "$CONFLICTS" -gt 0 ] ; then
    echo $1
    exit 1
  fi
}

function confirm {
  read -p "$1" -n 1 -r
  echo    # (optional) move to a new line
  if [[ ! $REPLY =~ ^[Yy]$ ]] ; then
      echo Operation stopped
      exit 1
  fi
}

function detect-changes {
  if [[ `git status --porcelain` ]]; then
    echo "Stash your changes to run this command"
    exit 1
  fi
}


branch=$(git branch | grep \* | cut -d ' ' -f2)
root=$(git rev-parse --show-toplevel)


if [ "$1" = "commit" ] ; then
  if [ "$2" = "" ] ; then
    echo "Missing parameter: commit message"
    exit 1
  fi

  if [ "$branch" = "master" ] || [ "$branch" = "develop" ] ; then
    echo "You should not commit on branch $branch"
    exit 1
  fi

  echo
  echo "Checking code..."
  echo

  result=$(./api.sh check)
  if [ "$result" != "ok" ] ; then
    echo "$result"
    exit 1
  fi

  git add $root
  git diff --cached
  confirm "Have you checked your code? [y/N] "

  git commit -m "$2"
  git pull
  detect-conflict "Resolve the conflict and commit"
  git push -u origin head


elif [ "$1" = "branch" ] ; then
  if [ "$2" = "" ] ; then
    echo "Missing parameter: branch name"
    exit 1
  fi
  if [ "$3" = "" ] ; then
    from_branch="develop"
  else
    from_branch=$3
  fi

  detect-changes

  git checkout $from_branch
  git pull
  git checkout -b $2
  git push -u origin head


elif [ "$1" = "merge" ] ; then
  if [ "$branch" = "master" ] || [ "$branch" = "develop" ] ; then
    echo "You cannot run this command on branch $branch"
    exit 1
  fi

  detect-changes

  git checkout develop
  git pull
  git checkout $branch
  git merge develop --no-edit
  detect-conflict "Resolve the conflict and commit"
  git push
  ./api.sh update
  ./site.sh update


elif [ "$1" = "clean" ] ; then
  git checkout develop
  git pull
  git branch --merged | sed '/^\** *develop$/d' | sed '/^\** *master$/d' | xargs git branch -d


else
  echo "Command not found: $1"
fi

git status
