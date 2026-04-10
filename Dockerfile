FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

ARG GITHUB_USERNAME=richard-rikk
ARG GITHUB_EMAIL=rikk.richard@gmail.com
ARG USERNAME=devuser
ARG USER_UID=1000
ARG USER_GID=1000

# Add a non-root user
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    usermod -aG sudo $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install LaTeX + Python
RUN apt-get update && apt-get install -y \
    texlive-latex-extra texlive-latex-recommended \
    texlive-fonts-recommended texlive-fonts-extra  \
    texlive-lang-european \
    git \
    python3 \
    python3-pip \
    && apt-get clean

# Install Ruff
RUN pip3 install --no-cache-dir ruff tqdm

# Set working directory
WORKDIR /workspace

# Copy script into container
COPY compile.py /usr/local/bin/compile.py

# Make it executable
RUN chmod +x /usr/local/bin/compile.py

# Config Git
RUN git config --global user.name "${GITHUB_USERNAME}" && \
    git config --global user.email "${GITHUB_EMAIL}" && \
    echo "source /usr/share/bash-completion/completions/git" >> ${DEV_USER_HOME_FOLDER}/.bashrc
 
USER $USERNAME

CMD ["bash"]
