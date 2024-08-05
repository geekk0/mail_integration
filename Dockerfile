# Use the official PostgreSQL image from the Docker Hub
FROM postgres:latest

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=my_db_user
ENV POSTGRES_PASSWORD=my_db_password
ENV POSTGRES_DB=my_db_name

# Expose the PostgreSQL port
EXPOSE 5432
