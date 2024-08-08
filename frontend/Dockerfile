FROM node:20-alpine as build

WORKDIR /app

COPY package*.json ./

RUN npm install

# add app
COPY . .

# build app
RUN npm run build

FROM nginx:latest as prod

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 3001/tcp

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]