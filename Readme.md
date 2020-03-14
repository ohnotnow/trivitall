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
The `TRIV_LEVEL` option can be any of UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL with the default being CRITICAL.  The `TRIV_VERBOSE` option will give you a lot more output :
```
Scanning the following images : {'minio/minio:RELEASE.2019-08-21T19-40-07Z', 'nginx:latest'}
Image minio/minio:RELEASE.2019-08-21T19-40-07Z has no vulnarabilties
Image nginx:latest has CRITICAL vulnarabilities. Used in service(s) {'freddy'}
###### Output from trivy scan of nginx:latest ######
b"2020-03-14T15:22:24.109Z\t\x1b[33mWARN\x1b[0m\tYou should avoid using the :latest tag as it is cached. You need to specify '--clear-cache' option when :latest image is changed"
b'2020-03-14T15:22:30.957Z\t\x1b[34mINFO\x1b[0m\tDetecting Debian vulnerabilities...'
b''
b'nginx:latest (debian 10.1)'
b'=========================='
b'Total: 2 (UNKNOWN: 0, LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 2)'
b''
b'+-----------------+------------------+----------+-------------------+---------------+--------------------------------+'
b'|     LIBRARY     | VULNERABILITY ID | SEVERITY | INSTALLED VERSION | FIXED VERSION |             TITLE              |'
b'+-----------------+------------------+----------+-------------------+---------------+--------------------------------+'
b'| libjpeg62-turbo | CVE-2019-2201    | CRITICAL | 1:1.5.2-2         |               | libjpeg-turbo: several integer |'
b'|                 |                  |          |                   |               | overflows and subsequent       |'
b'|                 |                  |          |                   |               | segfaults when attempting      |'
b'|                 |                  |          |                   |               | to compress/decompress         |'
b'|                 |                  |          |                   |               | gigapixel...                   |'
b'+-----------------+------------------+          +-------------------+---------------+--------------------------------+'
b'| tar             | CVE-2005-2541    |          | 1.30+dfsg-6       |               | Tar 1.15.1 does not properly   |'
b'|                 |                  |          |                   |               | warn the user when extracting  |'
b'|                 |                  |          |                   |               | setuid or...                   |'
b'+-----------------+------------------+----------+-------------------+---------------+--------------------------------+'
###### End of output from trivy scan of nginx:latest ######
```

## Exit codes

The script will exit with 0 if there were no issues found, 1 if there were any and 2 if something unexpected happened.
