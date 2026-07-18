@echo off
REM cattoys.bat - Jane's Cat Toys Recommendation Tool launcher
REM Usage: cattoys [options]
REM   cattoys
REM   cattoys --count 5
REM   cattoys --category interactive
REM   cattoys --max-price 20

python cat_toys.py %*
