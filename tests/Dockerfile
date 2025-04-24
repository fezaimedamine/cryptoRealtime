FROM python:3.10
WORKDIR /app

# Copier uniquement ce qui est nécessaire
COPY tests/ tests/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt pytest

# Vérification que les tests sont bien présents
RUN ls -l tests/

CMD ["pytest", "tests/", "-v"]  # -v pour le mode verbeux