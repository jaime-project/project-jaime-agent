VERSION=0.1.0

install i:
	virtualenv -p python3.10 env
	. env/bin/activate
	timeout 1
	pip install -r requirements.txt
	. env/bin/deactivate

build b:
	podman build . -t ghcr.io/jaime-project/jaime-agent:$(VERSION) -f Dockerfile --build-arg ARG_VERSION=$(VERSION)
	podman build . -t ghcr.io/jaime-project/jaime-agent-cluster:$(VERSION) -f Dockerfile.cluster --build-arg ARG_VERSION=$(VERSION)
	podman build . -t ghcr.io/jaime-project/jaime-agent-pushgateway:$(VERSION) -f Dockerfile.pushgateway --build-arg ARG_VERSION=$(VERSION)

push p:
	podman push ghcr.io/jaime-project/jaime-agent:$(VERSION)
	podman push ghcr.io/jaime-project/jaime-agent-cluster:$(VERSION) 
	podman push ghcr.io/jaime-project/jaime-agent-pushgateway:$(VERSION) 

compile c:
	python -m compile -b -f -o dist/ .
	rm -fr dist/repo_modules_default dist/env/
	cp -rf variables.env dist/
