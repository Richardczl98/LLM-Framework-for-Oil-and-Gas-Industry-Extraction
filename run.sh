#!/bin/bash

for round in {2..8}; do
    mkdir "result-240702-gpt4o-news-round-$round"
    mkdir "result-240702-gpt4o-spe-round-$round"
    bash script/tst-spe-18.sh
    mv "result/* result-240702-gpt4o-spe-round-$round"
    bash script/tst-news-13+1.sh
    mv "result/* result-240702-gpt4o-news-round-$round"
done


