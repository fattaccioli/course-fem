FROM conda/miniconda3:latest

# Set working directory
WORKDIR /workspace

# Copy environment file
COPY environment.yml /tmp/environment.yml

# Create conda environment
RUN conda env create -f /tmp/environment.yml && \
    conda clean -afy

# Activate environment by default
ENV PATH /opt/conda/envs/fem-microfluidics/bin:$PATH
SHELL ["/bin/bash", "-c"]

# Install Jupyter and configure for Docker
RUN conda run -n fem-microfluidics pip install --no-cache-dir jupyter ipykernel

# Create a user (optional, for security)
RUN useradd -m -s /bin/bash student && \
    chown -R student:student /workspace

USER student

# Start Jupyter
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
