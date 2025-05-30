# Frontend

This folder contains the frontend assets and templates for Yuzu Payroll

## Folder Structure

- `templates/`  
  Contains all Jinja2 HTML templates organized by feature:
  - `layouts/` - Base templates (e.g., `base.html`)
  - `components/` - Reusable partial templates (e.g., navbar, footer)
  - Feature folders (e.g., `employees/`, `payrolls/`) each containing related templates
  - `errors/` - Error pages (e.g., database unavailable)

- `static/`  
  Contains static assets served directly to the client:
  - `css/` - Stylesheets
  - `js/` - JavaScript files
  - `images/` - Images, icons, logos
  - `fonts/` - Custom fonts

## Working with Templates

- Templates use Jinja2 syntax and are rendered server-side by Flask
- Use `{% extends "layouts/base.html" %}` to inherit the base layout
- Include reusable components with `{% include "components/navbar.html" %}`, etc

## Static Files

- Link CSS and JS files in your templates using `url_for('static', filename='css/style.css')` or similar
- Place all static files inside the appropriate `static/` subfolders

## Notes

- This project currently uses minimal JavaScript. Any new scripts should go under `static/js/`
- To avoid errors in development, missing template variables use the configured Jinja `Undefined` behavior (see backend config)
- If using frontend build tools in the future, add instructions here

---

Feel free to add more instructions or update this README