@echo off

python backups\backup_db.py

git add backups

git diff --cached --quiet
if errorlevel 1 (
    git commit -m "Auto backup"
    git push
)