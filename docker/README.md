# Docker for datawrapper

## Installation

To create Docker you need to run:

```bash
make docker
```

which is equivalent to:

```bash
make docker VERSION=latest
```

You could also provide name and version for the image itself.
Default name is `IMAGE := datawrapper`.
Default version is `VERSION := latest`.

```bash
make docker IMAGE=some_name VERSION=0.4.5
```

## Usage

```bash
docker run -it --rm \
   -v $(pwd):/workspace \
   datawrapper bash
```

## How to clean up

To uninstall docker image run `make clean_docker` with `VERSION`:

```bash
make clean_docker VERSION=0.4.5
```

like in installation, you can also choose the image name

```bash
make clean_docker IMAGE=some_name VERSION=latest
```

If you want to clean all, including `build` run `make clean`
