# Usa a imagem oficial do Node.js como base
FROM node:14-alpine 

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app 

# Copia os arquivos de package.json e package-lock.json para o diretório de trabalho
COPY package*.json ./ 

# Instala as dependências do projeto
RUN npm install 

# Copia o resto dos arquivos do projeto para o diretório de trabalho
COPY . . 

# Define o comando para iniciar a aplicação quando o contêiner for executado
CMD ["npm", "start"]
