FROM node:22

WORKDIR /app

COPY package*.json ./
COPY *.js ./
RUN npm install

COPY src src
COPY public public

EXPOSE 3000

CMD ["npm", "start"]