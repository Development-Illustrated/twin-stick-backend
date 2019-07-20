# Pull alpine to build
FROM golang:alpine AS builder

# Install git
RUN apk update && apk add --no-cache git

# Set working directory so our packages work
WORKDIR $GOPATH/src/twinstick

# Copy in our files
COPY . .

# Install our packages
RUN go get github.com/gorilla/mux  github.com/gorilla/handlers 

# Build the binary
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o /go/bin/twinstick

# From the 0kb scratch image
FROM scratch

# Copy our compiled binary over
COPY --from=builder /go/bin/twinstick /go/bin/twinstick

# Expose port 8080
EXPOSE 8080

# Run it
ENTRYPOINT ["/go/bin/support-tool-backend"]

