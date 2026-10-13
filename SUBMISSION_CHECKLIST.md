# Submission Checklist

- [ ] `python manage.py test accounts cards transactions` ends with `OK`
- [x] Django coverage report displays 82% (`accounts,cards,transactions` only)
- [ ] FastAPI create/simulate payment manually tested; add automated tests if time permits
- [ ] Register/login/refresh/logout and card APIs checked in Swagger
- [ ] Admin summary, CSV export, and admin logs checked (empty logs acceptable until logged action exists)
- [ ] Import and execute requests in Postman
- [ ] Confirm API paths in this bundle match local `config/urls.py` / FastAPI main.py
- [ ] Add actual screenshots, not sample/reference screenshots, to `screenshots/`
- [ ] Add `requirements.txt` from your current `.venv`
- [ ] Ensure `.env`, passwords, tokens, full card data, and personal DB dumps are NOT committed
- [ ] `git status` checked, commit pushed successfully
- [ ] Copy GitHub repository URL for submission
