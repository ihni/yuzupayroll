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
USE `payroll_db` ;

-- -----------------------------------------------------
-- Table `payroll_db`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `payroll_db`.`roles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `hourly_rate` DECIMAL(10,2) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
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
  `email` VARCHAR(45) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
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
-- Table `payroll_db`.`work_logs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `payroll_db`.`work_logs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date_worked` DATETIME NOT NULL,
  `hours_worked` DECIMAL(4,2) NOT NULL,
  `employee_id` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `employee_id_idx` (`employee_id` ASC),
  CONSTRAINT `fk_work_logs_employee_id`
    FOREIGN KEY (`employee_id`)
    REFERENCES `payroll_db`.`employees` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `payroll_db`.`payroll`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `payroll_db`.`payroll` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `pay_period_start` DATETIME NOT NULL,
  `pay_period_end` DATETIME NOT NULL,
  `gross_pay` DECIMAL(10,2) NOT NULL,
  `total_hours` DECIMAL(5,2) NOT NULL,
  `employee_id` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
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
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;