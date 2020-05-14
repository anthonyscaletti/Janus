#First Stage
FROM golang:alpine AS build-stage

COPY /src/controller/ /go/src/controller/
COPY /src/controller/ai /go/src/controller/ai
COPY /src/entity /go/src/entity
COPY /src/handler/rest /go/src/handler/rest
COPY /src/usecase /go/src/usecase
COPY /src/static /go/static

WORKDIR /go/src/app

COPY /src/app/main.go .

RUN go build -o main .

RUN go get -d -v ./...
RUN go install -v ./...

#Second Stage
FROM golang:alpine 

COPY --from=build-stage /go/static /go/static
COPY --from=build-stage /go/bin /go/bin

EXPOSE 4000

CMD ["app"]
ENTRYPOINT ["app", "-f=7", "-s=9"]