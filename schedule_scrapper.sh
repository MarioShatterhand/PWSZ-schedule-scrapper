#!/bin/bash

variable=$(curl --silent https://pwsztar.edu.pl/instytut-politechniczny/informatyka/harmonogramy/ | htmlq "#rozmCZ > p:nth-child(8)")

echo $variable