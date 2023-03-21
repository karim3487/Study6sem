#!/bin/bash

if [[ $# -ge 1 ]]; then
  for file in $@; do
    if [[ -f $file ]]; then
      echo "File $file does not exist!"
    fi
  done
else
  echo "Ошибка: нужен хотя бы один аргумент!"
fi
