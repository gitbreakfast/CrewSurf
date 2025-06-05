FROM openjdk:11

# Install necessary tools
RUN apt-get update && apt-get install -y \
    git \
    wget \
    unzip \
    xvfb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Install Gradle (compatible with libGDX 1.13.1)
RUN wget https://services.gradle.org/distributions/gradle-7.6-bin.zip -P /tmp \
    && unzip -d /opt/gradle /tmp/gradle-7.6-bin.zip \
    && rm /tmp/gradle-7.6-bin.zip

# Set Gradle in PATH
ENV PATH=$PATH:/opt/gradle/gradle-7.6/bin

# Set environment variables for libGDX 1.13.1
ENV LIBGDX_VERSION=1.13.1

# Create a directory for the project
RUN mkdir -p /app/project

# Default command
CMD ["bash"]
