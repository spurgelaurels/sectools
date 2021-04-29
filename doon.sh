#!/bin/bash


input="$*"
length="${#input}"
while [ $charindex -lt $length ]
do
    char="${input:$charindex:1}"
    newstring="${newstring}$char"
    charindex=$(( $charindex + 1 ))
done
if [ -z "$(echo "$char" | sed -E 's/[[:lower:]]//')" ]
then
  if [ $doit -lt 5 ] ; then
    char="$(echo $char | tr '[[:lower:]]' '[[:upper:]]')"
  fi
elif [ -z "$(echo "$char" | sed -E 's/[[:upper:]]//')" ]
then
  if [ $doit -lt 3 ] ; then
    char="$(echo $char | tr '[[:upper:]]' '[[:lower:]]')"
  fi
fi
