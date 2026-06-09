import shutil
from datetime import datetime

filename = datetime.now().strftime(
    "backups/finance_%Y%m%d_%H%M.db"
)

shutil.copy(
    "finance.db",
    filename
)

print("Backup created:", filename)