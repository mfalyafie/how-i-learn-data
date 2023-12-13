.PHONY: clean
## clean : clean project files
clean:
	rm -rf build/ dist/ *.egg-info .eggs .coverage htmlcov .mypy_cache
	find . -name '*__pycache__' -exec rm -rf {} +

.PHONY: deps
## deps: install dependencies
deps:
	pip install -r requirements.txt

.PHONY: check
## check: Use mypy to lint source codes
check:
	mypy main.py

.PHONY: run
## run: Run main.py
run:
	uvicorn main:app --reload --log-level debug

.PHONY: build
## build: build a docker image for production
build:
	@if docker images | grep "falyafie/core-api"; then\
		docker rmi falyafie/core-api;\
	fi
	docker build -t falyafie/core-api -f Dockerfile .

.PHONY: push
## push: push a docker image to registry
push:
	docker push falyafie/core-api


.PHONY: help
all:help
#hel: show this  help message
help: Makefile
	@echo
	@echo " Choose a command to run in "$(NAME)":"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' | sed -e 's/^/ /'
	@echo