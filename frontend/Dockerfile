FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

# add app
COPY . .

# start app
CMD ["npm", "start"]
