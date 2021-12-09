install i:
	virtualenv -p python3.9 env
	. env/bin/activate
	timeout 1
	pip install -r requirements.txt
	. env/bin/deactivate

build b:
	docker build . -t brianwolf94/project-jaime-agent:local --no-cache

compile c:
	python -m compile -b -f -o dist/ .
	rm -fr dist/repo_modules_default dist/env/
	cp -rf variables.env dist/