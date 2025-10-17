# Use Playwright base image (already includes Chromium and dependencies)
FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=UTC \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# --- PREINSTALL CAMOUFOX ---
# This downloads and extracts Camoufox during build to avoid long runtime setup
RUN python -c "from camoufox.pkgman import CamoufoxFetcher; CamoufoxFetcher().install()"

# Copy the Django project files
COPY . /app/

# Expose the app port
EXPOSE 8001

# Run Gunicorn with higher timeout to prevent worker kills during scraping
CMD ["gunicorn", "price_alert.wsgi:application", "--bind", "0.0.0.0:8001", "--timeout", "300"]
