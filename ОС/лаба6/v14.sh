#!/bin/bash
ARG="$1"

# print usage if no agument passed
if [[ -h "$ARG" ]];then
	echo "Usage: bash $0 [ ROMAN ]"
	echo "Example: bash $0 MCMXCVIII"
	exit 1
fi

to_decimal() {
  local ROMAN=$1
  local INUM=0
  local PREV=0
 
  for ((i=${#ROMAN}-1;i>=0;i--));do
    case "${ROMAN:$i:1}" in
    M)  VAL=1000 ;;
    D)  VAL=500 ;;
    C)  VAL=100 ;;
    L)  VAL=50 ;;
    X)  VAL=10 ;;
    V)  VAL=5 ;;
    I)  VAL=1 ;;
    esac
 
    if [[ $VAL -lt $PREV ]]
    then
       let INUM-=VAL
    else
       let INUM+=VAL
    fi
 
    PREV=$VAL
  done
 
  echo "$INUM"
}

for num in $@; do
  to_decimal "$num"
done
