@echo off
python main.py < in.txt > result.txt
fc result.txt out.txt
