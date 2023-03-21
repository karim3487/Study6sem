#!/bin/bash

if [[ $(($#%2)) -eq 0  ]]; then
  echo "" > report
  count_of_files=0
  for (( i=1; i<$(($#+1)); i+=2 )); do
    filename=$i
    word=$((i+1))
    filename=${!filename}
    word=${!word}
    
    if [[ -f "$filename" ]]; then
      echo "$filename - существует" >> report
    else
      echo "$word" > $filename
      echo "$filename - создан" >> report
      let "count_of_files+=1"
    fi
  done
  echo "Количество созданных файлов - $count_of_files" >> report
  echo 
else
  echo "Количество элементов должно быть четным"
  exit 1
fi
