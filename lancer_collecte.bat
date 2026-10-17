@echo off
cd /d "%~dp0"
python "collecte_steamspy.py" >> "collecte_automatique.log" 2>&1
