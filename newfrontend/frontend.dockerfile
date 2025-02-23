# Step 1: Build React App
FROM node:18 as build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

COPY public ./public
COPY src ./src
RUN npm run build

# Step 2: Serve with Nginx
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
