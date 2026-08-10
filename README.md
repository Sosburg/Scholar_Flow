# ScholarFlow Django Conversion

This is a Django conversion of the uploaded React/Vite ScholarFlow prototype.

## Included upgrades
- Django backend and templates
- user authentication
- per-user isolated workspace
- paper uploads to server storage
- statement capture and theme assignment
- synthesis view
- CSV export
- admin support
- selectable PDF reader page using pdf.js text layer

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/

## Notes
- Each user gets their own workspace automatically on registration.
- The PDF page now renders both the PDF canvas and a selectable text layer so users can highlight passages directly in the browser.
- Zoom in, zoom out, fit-width, and page navigation are included on the reader page.
