FROM node:14-alpine 

RUN mkdir /FrontEnd

WORKDIR /FrontEnd

COPY package.json ./

COPY package-lock.json ./

RUN npm install 

COPY . /FrontEnd/

RUN npm run build

CMD ["npm", "start"]
