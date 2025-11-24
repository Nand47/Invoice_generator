# Invoice Generator

Simple Django app to create invoices, add items, and generate PDFs.

## Features
- Create and list invoices
- Add line items to invoices
- Generate PDF for an invoice
- Basic UI with Bootstrap

## Prerequisites
- Python 3.8+
- Git
- (Optional) system libraries required by any PDF library you use (wkhtmltopdf / WeasyPrint)

## Quick start (Windows PowerShell)
1. Clone the repo (if not already):
   ```
   git clone https://github.com/Nand47/Invoice-Generator.git
   cd "Invoice-Generator"
   ```

2. Create & activate virtualenv:
   ```
   python -m venv venv
   .\venv\Scripts\Activate
   ```

3. Install dependencies:
   - If repository has requirements.txt:
     ```
     pip install -r requirements.txt
     ```
   - Otherwise install Django and any PDF lib you use:
     ```
     pip install django
     # e.g. pip install weasyprint
     ```

4. Apply migrations and create superuser:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. Run development server:
   ```
   python manage.py runserver
   ```
   Open http://127.0.0.1:8000/

## Common tasks
- Create invoice: Visit the Create Invoice page.
- Add items: Use Add Items for a selected invoice.
- Generate PDF: Click Generate PDF next to an invoice.

## Git / GitHub
To push local main branch and set upstream:
```
git add .
git commit -m "Initial commit"
git push -u origin main
```

If you need to remove local git history:
```
# from project root
rm -rf .git    # Git Bash
# or
Remove-Item -Recurse -Force .git   # PowerShell
```

## Customization
- Templates: `template/invoices/`
- URL patterns: `invoices/urls.py`
- Views: `invoices/views.py`
- Settings: `invoice_generator/settings.py` (configure DB, static, email, PDF backend)

## Troubleshooting
- NoReverseMatch for missing URL name: ensure the template uses URL names defined in `invoices/urls.py`.
- CSRF errors on AJAX: pass the CSRF token in request headers.

## Contributing
PRs and issues are welcome. Keep changes small and focused.

## License
MIT License — add LICENSE file if required.
