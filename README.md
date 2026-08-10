# ScholarFlow Django Conversion

A simplified version of Atlas.ti that allows researchers and students to extract and save quotes, take context-specific notes, and organize source material from articles or books. 

ScholarFlow mimics core features of Atlas.ti—a powerful computer-assisted qualitative data analysis software (CAQDAS) used to uncover complex patterns, build thematic networks, and manage qualitative information efficiently across multiple data types:
- **Text & Documents**: PDFs, Word files, e-books, and interview transcripts.
- **Multimedia**: Audio recordings and video files.
- **Visuals**: Images, photographs, and diagrams.
- **External Data**: Survey data, social media feeds, and web pages.

---

## Features & Upgrades
- **Django Backend**: Fully functional MVC architecture and clean template rendering.
- **User Authentication**: Secure user sign-up, login, and session management.
- **Isolated Workspaces**: Automatic creation of per-user sandboxed environments upon registration.
- **Document Management**: Direct file uploads to server storage.
- **Qualitative Coding**: Statement capture and dynamic theme/code assignment.
- **Synthesis View**: Comprehensive overview of extracted data and coding patterns.
- **Data Portability**: Clean CSV export functionality for further analysis.
- **Admin Dashboard**: Built-in Django admin support for user and document management.
- **Advanced PDF Reader**: Embedded reader powered by `pdf.js` with a selectable text layer overlay for native browser highlighting. Includes zoom controls, fit-to-width, and page navigation.

---

## Quick Start

### 1. Clone and Navigate
```bash
git clone https://github.com
cd scholarflow_django_textlayer_upgrade_v3
```

### 2. Set Up Virtual Environment
**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
**On macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies & Initialize Database
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

### 4. Launch the Server
```bash
python manage.py runserver
```
Open your browser and navigate to: **`http://127.0.0.1:8000/`**
