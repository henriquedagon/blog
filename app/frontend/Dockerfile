# Origin image
FROM node

# Working dir
WORKDIR /app

# Add "/app/node_modules/.bin" to PATH
ENV PATH /app/node_modules/.bin:$PATH

# Install packages to leverage cache
COPY package.json /app/
COPY package-lock.json /app/
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent
RUN npm install axios --silent

COPY . ./

# start app
CMD ["npm","start"]