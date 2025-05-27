FROM php:8.2-apache

# Install PHP extensions
RUN docker-php-ext-install mysqli pdo pdo_mysql
RUN a2enmod rewrite

RUN apt-get update && \
    apt-get install -y vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
# Copy PHP frontend
COPY frontend-php/ /var/www/html/
WORKDIR /var/www/html/
