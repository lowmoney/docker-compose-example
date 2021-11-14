FROM node:10

RUN npm install -g serve

WORKDIR /code

COPY ./build /code/build

EXPOSE 8002

CMD ["serve", "-s", "/code/build", "-p", "8002"]