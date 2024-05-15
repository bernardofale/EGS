FROM node:14-alpine 

RUN mkdir /FrontEnd

WORKDIR /FrontEnd

COPY package.json ./

COPY package-lock.json ./

RUN npm install 

COPY . /FrontEnd/

CMD ["npm", "start"]
