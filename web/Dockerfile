FROM node:lts-alpine AS web-builder
WORKDIR /workdir
COPY . .
RUN npm ci
RUN npx ng build --prod

FROM nginx:alpine
COPY --from=web-builder /workdir/dist/web/ /usr/share/nginx/html