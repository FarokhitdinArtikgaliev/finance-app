@echo off

cd /d C:\Users\Администратор\finance_app

python backup_db.py

git add .

git commit -m "Auto backup"

git push