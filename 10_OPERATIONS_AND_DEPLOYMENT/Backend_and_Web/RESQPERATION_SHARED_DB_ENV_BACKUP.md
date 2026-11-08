# RESQPERATION Shared DB Env Backup

This file stores the previous shared database connection before switching to the local MySQL schema.

Do not commit or share this file publicly.

## Previous Shared DB Settings

```env
DB_CONNECTION=mysql
DB_HOST=192.168.112.68
DB_PORT=3306
DB_DATABASE=klint
DB_USERNAME=groupmate
DB_PASSWORD=REDACTED
DB_CONNECTION_TIMEOUT=5
```

## Current Local DB Settings

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=resqperation_db
DB_USERNAME=root
DB_PASSWORD=REDACTED
DB_CONNECTION_TIMEOUT=5
```

## How To Restore Shared DB Later

1. Open `backend-laravel/.env`.
2. Replace the current local DB settings with the previous shared DB settings above.
3. Clear Laravel config cache:

```bash
cd backend-laravel
php artisan config:clear
php artisan cache:clear
```

4. Restart the Laravel server.
