# Base image using official Odoo 18 release
FROM odoo:18.0

# Switch to root user to perform administrative installation tasks
USER root

# Install system utilities and dependencies required for modern Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy python dependencies list if any custom external library is needed
# COPY requirements.txt /etc/odoo/requirements.txt
# RUN pip3 install --no-cache-dir -r /etc/odoo/requirements.txt

# Revert back to unprivileged odoo system user for secure container execution
USER odoo