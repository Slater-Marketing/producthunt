@echo off
cd /d "%~dp0"
echo Starting ProductHunt Scraper at %date% %time%
python producthunt_scraper.py
echo Scraper completed at %date% %time%
pause 