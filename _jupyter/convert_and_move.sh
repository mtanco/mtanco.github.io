#!/usr/bin/env bash
nb=$1

jupyter nbconvert $nb --to markdown
mv ${nb%.ipynb}.md ../_posts/
