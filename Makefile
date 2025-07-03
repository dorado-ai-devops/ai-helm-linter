build:
	docker build -t ai-helm-linter .

run:
	docker run -p 5001:5001 ai-helm-linter
