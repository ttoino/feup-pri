FROM node:18-alpine as build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY . .

RUN npm run build

FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci --production

COPY --from=build /app/build ./build

CMD ["node", "build"]
