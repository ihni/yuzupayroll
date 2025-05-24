-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema payroll_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema payroll_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `payroll_db` DEFAULT CHARACTER SET utf8 ;
USE `payroll_db` ;

-- -----------------------------------------------------
-- Table `payroll_db`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `payroll_db`.`roles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `rate` DECIMAL(10,2) NOT NULL,
  `status` ENUM('ACTIVE', 'ARCHIVED') NULL DEFAULT 'ACTIVE',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `archived_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `payroll_db`.`employees`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `payroll_db`.`employees` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `role_id` INT NOT NULL,
  `status` ENUM('ACTIVE', 'INACTIVE', 'ARCHIVED') NOT NULL DEFAULT 'ACTIVE',
  `email` VARCHAR(100) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `archived_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `role_id_idx` (`role_id` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  CONSTRAINT `fk_employees_role_id`
    FOREIGN KEY (`role_id`)
    REFERENCES `payroll_db`.`roles` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `payroll_db`.`worklogs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `payroll_db`.`worklogs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `employee_id` INT NOT NULL,
  `date` DATETIME NOT NULL,
  `hours_worked` DECIMAL(4,2) UNSIGNED NOT NULL,
  `status` ENUM('ACTIVE', 'LOCKED', 'ARCHIVED') NOT NULL DEFAULT 'ACTIVE',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `archived_at` DATETIME NULL DEFAULT NULL,
  `locked_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `employee_id_idx` (`employee_id` ASC),
  CONSTRAINT `fk_worklogs_employee_id`
    FOREIGN KEY (`employee_id`)
    REFERENCES `payroll_db`.`employees` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `payroll_db`.`payrolls`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `payroll_db`.`payrolls` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `employee_id` INT NOT NULL,
  `start_date` DATETIME NOT NULL,
  `end_date` DATETIME NOT NULL,
  `gross_pay` DECIMAL(10,2) NOT NULL,
  `net_pay` DECIMAL(10,2) NOT NULL,
  `status` ENUM('DRAFT', 'FINALIZED', 'ARCHIVED') NOT NULL DEFAULT 'DRAFT',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `archived_at` DATETIME NULL DEFAULT NULL,
  `finalized_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `employee_id_idx` (`employee_id` ASC),
  CONSTRAINT `fk_payroll_employee_id`
    FOREIGN KEY (`employee_id`)
    REFERENCES `payroll_db`.`employees` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `payroll_db`.`organization`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `payroll_db`.`organization` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `total_salary_budget` DECIMAL(10,2) NOT NULL,
  `budget_start_month` INT NOT NULL DEFAULT 1,
  `budget_start_day` INT NOT NULL DEFAULT 1,
  `budget_end_month` INT NOT NULL DEFAULT 12,
  `budget_end_day` INT NOT NULL DEFAULT 31,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `tax_rate` DECIMAL(5,4) NOT NULL DEFAULT 0.0000,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `payroll_db`.`payroll_worklogs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `payroll_db`.`payroll_worklogs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `payroll_id` INT NOT NULL,
  `worklog_id` INT NOT NULL,
  `hours_recorded` DECIMAL(5,2) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT current_timestamp,
  `snapshot_locked` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  INDEX `fk_payroll_worklogs_payroll_id_idx` (`payroll_id` ASC),
  INDEX `fk_payroll_worklogs_worklog_id_idx` (`worklog_id` ASC),
  CONSTRAINT `fk_payroll_worklogs_payroll_id`
    FOREIGN KEY (`payroll_id`)
    REFERENCES `payroll_db`.`payrolls` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_payroll_worklogs_worklog_id`
    FOREIGN KEY (`worklog_id`)
    REFERENCES `payroll_db`.`worklogs` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;