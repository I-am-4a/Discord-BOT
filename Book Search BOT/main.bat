@echo off
cls
pushd %0\..
title Book Search BOT

:loop
py bsbot.py
goto loop
 
