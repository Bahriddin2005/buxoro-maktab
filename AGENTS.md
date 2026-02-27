# AGENTS.md

## Cursor Cloud specific instructions

This is a Django 5.2.5 monolith (Python 3.12) — an online test/exam platform ("Buxoro Bilimdonlar Maktabi"). It uses SQLite, in-memory caching, and WhiteNoise for static files, so there are no external service dependencies.

### Services

| Service | Command | Notes |
|---|---|---|
| Django dev server | `python3 manage.py runserver 0.0.0.0:8000` | The only service needed for development |

### Key commands

- **Install deps:** `pip install -r requirements.txt`
- **Migrations:** `python3 manage.py migrate`
- **Tests:** `python3 manage.py test accounts tests_app analytics` (app test stubs are empty; the root-level `test_excel_export.py` is a standalone script, not a standard Django test)
- **Lint:** `pyright` (config in `pyproject.toml` with type checking off)
- **System check:** `python3 manage.py check`
- **Collect static:** `python3 manage.py collectstatic --noinput`
- **Create superuser:** requires `--first_name` and `--last_name` flags due to custom User model (`REQUIRED_FIELDS = ['email', 'first_name', 'last_name']`)
- **Load sample data:** `python3 create_sample_data.py` (creates teacher1/student1/student2 users and sample tests)

### Gotchas

- The custom `accounts.User` model requires `first_name`, `last_name`, and `email` as `REQUIRED_FIELDS`. When using `createsuperuser --noinput`, pass `--first_name=X --last_name=Y`.
- The app login page (`/accounts/login/`) requires user verification (`is_verified=True`). The admin superuser created via `createsuperuser` has `is_verified=False` by default. Use the Django admin panel (`/admin/`) to log in with the superuser, or set `is_verified=True` on the user.
- `ALLOWED_HOSTS` includes `localhost` and `127.0.0.1`; bind to `0.0.0.0:8000` for access.
- `STATICFILES_STORAGE` uses `whitenoise.storage.CompressedManifestStaticFilesStorage`; run `collectstatic` before first server start to avoid missing-file warnings.
- `~/.local/bin` may not be on PATH; prefix commands with `export PATH="$HOME/.local/bin:$PATH"` or add it to shell profile.

### Demo credentials (after running `create_sample_data.py`)

| User | Username | Password | Role |
|---|---|---|---|
| Admin | admin | admin123 | superuser |
| Teacher | teacher1 | teacher123 | teacher |
| Student | student1 | student123 | student (verified) |
| Student 2 | student2 | student123 | student (unverified) |
