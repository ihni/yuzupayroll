-- Seeder Script for Payroll Database
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

-- Clear existing data (careful with this in production)
DELETE FROM `payroll`;
DELETE FROM `work_logs`;
DELETE FROM `employees`;
DELETE FROM `roles`;
DELETE FROM `organization`;

-- Insert organization data
INSERT INTO `organization` (`name`, `total_salary_budget`, `budget_start_month`, `budget_start_day`, `budget_end_month`, `budget_end_day`) 
VALUES 
('Northern Lights Inc.', 5000000.00, 1, 1, 12, 31),
('Island Breeze Corp.', 3000000.00, 4, 1, 3, 31);

-- Insert roles with hourly rates
INSERT INTO `roles` (`name`, `hourly_rate`) 
VALUES 
('Software Developer', 35.50),
('Nurse', 28.75),
('Teacher', 25.00),
('Electrician', 30.25),
('Accountant', 32.00),
('Marketing Specialist', 27.50),
('Construction Worker', 22.00),
('Customer Service', 18.50);

-- Insert employees
INSERT INTO `employees` (`first_name`, `last_name`, `role_id`, `email`, `created_at`, `updated_at`) 
VALUES
('Juan', 'Dela Cruz', 1, 'juan.delacruz@example.com', NOW(), NOW()),
('Maria', 'Santos', 2, 'maria.santos@example.com', NOW(), NOW()),
('Jose', 'Reyes', 3, 'jose.reyes@example.com', NOW(), NOW()),
('Ana', 'Gonzales', 4, 'ana.gonzales@example.com', NOW(), NOW()),
('Pedro', 'Bautista', 5, 'pedro.bautista@example.com', NOW(), NOW()),
('Luzviminda', 'Tan', 6, 'luzviminda.tan@example.com', NOW(), NOW()),
('Ricardo', 'Lim', 7, 'ricardo.lim@example.com', NOW(), NOW()),
('Corazon', 'Ong', 8, 'corazon.ong@example.com', NOW(), NOW()),
('Eduardo', 'Sy', 1, 'eduardo.sy@example.com', NOW(), NOW()),
('Imelda', 'Chua', 2, 'imelda.chua@example.com', NOW(), NOW()),
('Anders', 'Johansson', 3, 'anders.johansson@example.com', NOW(), NOW()),
('Elin', 'Nilsson', 4, 'elin.nilsson@example.com', NOW(), NOW()),
('Lars', 'Andersson', 5, 'lars.andersson@example.com', NOW(), NOW()),
('Anna', 'Karlsson', 6, 'anna.karlsson@example.com', NOW(), NOW()),
('Johan', 'Eriksson', 7, 'johan.eriksson@example.com', NOW(), NOW()),
('Maria', 'Larsson', 8, 'maria.larsson@example.com', NOW(), NOW()),
('Per', 'Olsson', 1, 'per.olsson@example.com', NOW(), NOW()),
('Karin', 'Persson', 2, 'karin.persson@example.com', NOW(), NOW()),
('Erik', 'Svensson', 3, 'erik.svensson@example.com', NOW(), NOW()),
('Sofia', 'Gustafsson', 4, 'sofia.gustafsson@example.com', NOW(), NOW());

-- Insert work logs (random hours between 4 and 12 for last 30 days, approx 10 logs per employee)
INSERT INTO `work_logs` (`date_worked`, `hours_worked`, `employee_id`, `created_at`, `updated_at`)
SELECT 
    DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 30) DAY) AS date_worked,
    ROUND(4 + (RAND() * 8), 2) AS hours_worked,
    e.id AS employee_id,
    NOW(),
    NOW()
FROM 
    employees e
CROSS JOIN 
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) AS numbers
ORDER BY RAND()
LIMIT 200;

-- Insert payroll for last 3 months grouped by employee and month, calculating totals from work logs and roles
INSERT INTO `payroll` (`pay_period_start`, `pay_period_end`, `gross_pay`, `total_hours`, `employee_id`, `created_at`, `updated_at`)
SELECT 
    DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL m.month_offset MONTH), '%Y-%m-01') AS pay_period_start,
    LAST_DAY(DATE_SUB(CURDATE(), INTERVAL m.month_offset MONTH)) AS pay_period_end,
    SUM(wl.hours_worked * r.hourly_rate) AS gross_pay,
    SUM(wl.hours_worked) AS total_hours,
    e.id AS employee_id,
    NOW(),
    NOW()
FROM 
    employees e
JOIN 
    roles r ON e.role_id = r.id
JOIN 
    work_logs wl ON e.id = wl.employee_id
JOIN 
    (SELECT 0 AS month_offset UNION SELECT 1 UNION SELECT 2) m
WHERE 
    wl.date_worked BETWEEN DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL m.month_offset MONTH), '%Y-%m-01') 
    AND LAST_DAY(DATE_SUB(CURDATE(), INTERVAL m.month_offset MONTH))
GROUP BY 
    e.id, m.month_offset
HAVING 
    SUM(wl.hours_worked) > 0;

SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;