# ================================================
# Stage 1 — Build Stage
# ================================================

# Base Image
# ------------------------------------------------
# We use a Debian-based Node image instead of Alpine
# - Alpine uses musl libc which can cause issues with Vite/Rollup
# - node:slim uses glibc and is more stable for frontend builds
FROM node:20-slim AS builder


# Set Working Directory
# ------------------------------------------------
# All commands will execute inside /app
WORKDIR /app


# Copy Dependency Files First (Docker Cache Optimization)
# ------------------------------------------------
# Copy only package.json and package-lock.json first
# This allows Docker to cache npm install step
# If application code changes but dependencies don't,
# Docker will reuse the cached layer
COPY package.json package-lock.json ./


# Install Exact Dependencies
# ------------------------------------------------
# npm ci:
# - Installs exact versions from package-lock.json
# - Faster and more reliable than npm install
# - Recommended for CI/CD and production builds
RUN npm ci


# Build-Time Environment Variable
# ------------------------------------------------
# Vite injects environment variables at build time
# Therefore we pass VITE_API_URL as a build argument
# Example : docker build --build-arg VITE_API_URL=http://localhost:8000 -t churn_frontend ./frontend
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}


# Copy Application Source Code
# ------------------------------------------------
# Now copy the rest of the frontend source files
# Done after dependency installation for better caching
COPY . .


# Build Production Bundle
# ------------------------------------------------
# This generates optimized static files inside /app/dist
# The final runtime image will only contain these static files
RUN npm run build


# ================================================
# Stage 2 — Runtime Stage
# ================================================

# Base Image
# ------------------------------------------------
# We use nginx Alpine for serving static files
# Very lightweight and production-ready
FROM nginx:1.25-alpine


# Remove Default Nginx Configuration
# ------------------------------------------------
# Remove the default config to avoid conflicts
RUN rm /etc/nginx/conf.d/default.conf


# Copy Custom Nginx Configuration
# ------------------------------------------------
# This config enables:
# - SPA routing (try_files $uri /index.html)
# - Proper static asset serving
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html


# Expose Port
# ------------------------------------------------
# Nginx listens on port 80 inside container
# This allows port mapping like: docker run -p 3000:80 image_name
EXPOSE 80


# Start Nginx Server
# ------------------------------------------------
# "daemon off" keeps nginx running in foreground
# Required for Docker containers
CMD ["nginx", "-g", "daemon off;"]