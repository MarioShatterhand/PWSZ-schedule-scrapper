#!/bin/bash

variable=$(curl --silent https://pwsztar.edu.pl/instytut-politechniczny/informatyka/harmonogramy/)

# if [ "$variable" == "<p>Aktualizacja: 2021-05-24 13:40 CEST</p>" ]
# then
#   echo Hey: $variable
# fi

echo "$variable"

