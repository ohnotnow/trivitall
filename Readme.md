# Trivitall

This is a simple python script which gets a list of all docker swarm services and runs every container image found through
Aquasecurity's [Trivy](https://github.com/aquasecurity/trivy) security scanner.
__Note__: The script needs access to the docker socket, so make sure to scan through the code to make sure you trust it.

## Usage

First off, build the image that will run the script :
```bash
docker build -t trivitall:some-tag .
```

And on a swarm master run the image :
```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock trivitall:some-tag
```
That should produce output like this for any images found to have critial security warnings :
```
Image nginx:latest has CRITICAL vulnarabilities. Used in service(s) {'my-web-app'}
```

## Options

You can control the verbosity of the output and what security level you want to report on using environment variables :
```bash
docker run -e TRIV_VERBOSE=1 -e TRIV_LEVEL=MEDIUM,HIGH,CRITICAL --rm -v /var/run/docker.sock:/var/run/docker.sock trivitall:some-tag
```
The `TRIV_LEVEL` option can be any of UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL with the default being CRITICAL.

## Exit codes

The script will exit with 0 if there were no issues found, 1 if there were any and 2 if something unexpected happened.
