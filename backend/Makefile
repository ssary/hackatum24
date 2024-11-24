include .env

start:
	uvicorn src.main:app --reload

# Create and activate a virtual environment, then install dependencies
create_venv:
	python3 -m venv venv
	@echo "Virtual environment created. Activating and installing dependencies..."
	. venv/bin/activate && pip install -r requirements.txt

# Save the current dependencies into requirements.txt
save_requirements:
	@echo "Saving current dependencies to requirements.txt..."
	pip freeze > requirements.txt

# Activate the virtual environment (Linux/MacOS)
activate:
	@echo "Activating virtual environment..."
	. venv/bin/activate

# Install dependencies from requirements.txt
install_requirements:
	@echo "Installing dependencies from requirements.txt..."
	pip install -r requirements.txt

# Remove the virtual environment (clean-up)
remove_venv:
	@echo "Removing virtual environment..."
	rm -rf venv

# Ersetzt DOCKER_REGISTRY mit der gewünschten Registry (z. B. docker.io oder AWS ECR URL)
DOCKER_IMAGE=${DOCKER_USERNAME}/fastapi-app
DOCKER_TAG=latest

docker_build_and_push:
	@echo "Building Docker Image..."
	docker build --platform linux/amd64 -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
	@echo "Docker Image Built: ${DOCKER_IMAGE}:${DOCKER_TAG}"
	@echo "Logging into Docker Registry..."
	echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin
	@echo "Pushing Docker Image to Registry..."
	docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
	@echo "Docker Image Pushed Successfully!"
