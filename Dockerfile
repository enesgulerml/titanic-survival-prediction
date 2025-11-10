# Step 1: Base Image
FROM continuumio/miniconda3:latest

# Step 2: Set Working Directory
WORKDIR /app

# Step 3: Copy and Install Dependencies
COPY environment.yml environment.yml
RUN conda env update -n base -f environment.yml

# Step 4: Install Project Package (setup.py)
COPY setup.py setup.py
RUN pip install .

# Step 5: Copy Entire Code
COPY . .

# Step 6: Define Port (EXPOSE)
EXPOSE 80

# Step 7: Default Command (CMD)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]