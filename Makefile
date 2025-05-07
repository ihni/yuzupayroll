COMPOSE=podman-compose

.PHONY: help
help:
	@echo "Commands"
	@echo "	make up			Start the container"
	@echo "	make down		Stop the container"
	@echo "	make rebuild		Rebuild and start fresh"
	@echo "	make logs		View logs"
	@echo "	make clean		Remove all data"

# Start the container
.PHONY: up
up:
	$(COMPOSE) up --build

# Stop the container
.PHONY: down
down:
	$(COMPOSE) down

# Rebuild and start fresh
.PHONY: rebuild
rebuild:
	$(COMPOSE) down --volumes
	$(COMPOSE) up --build

# View logs
.PHONY: logs
logs:
	$(COMPOSE) logs -f

# Remove all data
.PHONY: clean
clean:
	$(COMPOSE) down --volumes --remove-orphans
	rm -rf mysql_data
	rm -rf logs
