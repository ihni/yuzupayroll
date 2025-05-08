# =========================
# Project Configuration
# =========================
export PODMAN_IGNORE_CGROUPSV1_WARNING=1
COMPOSE := podman-compose
PROJECT_NAME := payrollsys
MYSQL_USER := user
MYSQL_PASS := pass
MYSQL_DATABASE := payroll_db

# =========================
# Development commands
# =========================
.PHONY:
help:
	@echo "Payroll Management System"
	@echo "make init		- Initialize directories and permissions"
	@echo "make up			- Start the container"
	@echo "make up-detached	- Start the container detached"
	@echo "make down		- Stop the container"
	@echo "make restart		- Restart the containers"
	@echo "make logs		- View container logs"
	@echo "make clean		- Full cleanup"
	@echo "make db-shell		- Access MySQL shell"

# =========================
# Development commands
# =========================
.PHONY: init up up-detach down restart logs clean db-shell

init:
	mkdir -p storage/{db,logs}
	@echo "Storage initialized"

up: init
	@echo "Starting $(PROJECT_NAME)..."
	$(COMPOSE) up --build

up-detach:
	@echo "Starting $(PROJECT_NAME) detached..."
	$(COMPOSE) up --build --detach

down:
	@echo "Stopping container..."
	$(COMPOSE) down --timeout 2

restart: down up

logs:
	$(COMPOSE) logs --tail=100 -f

clean:
	$(COMPOSE) down --volumes --remove-orphans
	rm -rf storage
	podman system prune -f
	@echo "All containers and data removed"

db-shell:
	$(COMPOSE) exec db mysql -u$(MYSQL_USER) -p$(MYSQL_PASSWORD) $(MYSQL_DATABASE)