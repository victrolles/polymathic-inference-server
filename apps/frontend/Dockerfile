# Build stage
FROM node:22 AS build
WORKDIR /app
COPY apps/frontend/ .
RUN npm install
RUN npm run build

# Serve stage
FROM nginx:alpine
ENV GATEWAY_SERVICE_HOST="inference-platform-gateway-service"
ENV GATEWAY_SERVICE_PORT="8000"
COPY apps/frontend/default.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80