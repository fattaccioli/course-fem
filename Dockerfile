FROM python:3.10-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python packages (avoid conda complexity)
RUN pip install --no-cache-dir \
    numpy \
    scipy \
    matplotlib \
    jupyter \
    jupyterlab \
    pandas \
    ipywidgets \
    tqdm \
    gmsh \
    fenics-dolfinx

# Create a non-root user
RUN useradd -m -s /bin/bash student && \
    chown -R student:student /workspace

USER student

# Expose Jupyter port
EXPOSE 8888

# Default command
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
