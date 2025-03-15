FROM node:22-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

FROM base AS dev
EXPOSE 3000
CMD [ "npm", "run", "dev" ]

FROM base AS build
RUN npm run build

FROM nginx:stable-alpine AS prod
COPY --from=build /app/.next /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]