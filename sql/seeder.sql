SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

-- Clear existing data (be careful with this in production)
DELETE FROM `payroll_worklogs`;
DELETE FROM `payrolls`;
DELETE FROM `worklogs`;
DELETE FROM `employees`;
DELETE FROM `roles`;
DELETE FROM `organization`;

-- Insert organization data
INSERT INTO `organization` (
    `name`, `total_salary_budget`, `budget_start_month`, `budget_start_day`, 
    `budget_end_month`, `budget_end_day`, `tax_rate`
) VALUES (
    'Northern Lights Inc.', 5000000.00, 1, 1, 12, 31, 0.05
);

-- Insert roles with hourly rates
INSERT INTO `roles` (`name`, `rate`) VALUES
('Software Developer', 35.50),
('Nurse', 28.75),
('Teacher', 25.00),
('Electrician', 30.25),
('Accountant', 32.00),
('Marketing Specialist', 27.50),
('Construction Worker', 22.00),
('Customer Service', 18.50);

-- Insert employees
INSERT INTO `employees` (
    `first_name`, `last_name`, `role_id`, `email`, `created_at`, `updated_at`
) VALUES
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

-- Insert worklogs (random hours between 4 and 12 for the past 90 days, ~30 logs per employee)
INSERT INTO `worklogs` (`employee_id`, `date`, `hours_worked`, `status`, `created_at`, `updated_at`)
SELECT 
    e.id AS employee_id,
    DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 90) DAY) AS date,
    ROUND(4 + (RAND() * 8), 2) AS hours_worked,
    'ACTIVE' AS status,
    NOW() AS created_at,
    NOW() AS updated_at
FROM 
    employees e
CROSS JOIN 
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION 
     SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 
     UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15 
     UNION SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION SELECT 20 
     UNION SELECT 21 UNION SELECT 22 UNION SELECT 23 UNION SELECT 24 UNION SELECT 25 
     UNION SELECT 26 UNION SELECT 27 UNION SELECT 28 UNION SELECT 29 UNION SELECT 30) AS numbers
ORDER BY RAND()
LIMIT 1000;

-- Insert payrolls for last 3 months grouped by employee and month, calculating totals from worklogs and roles
INSERT INTO `payrolls` (
    `employee_id`, `pay_period_start`, `pay_period_end`, `gross_pay`, `net_pay`, 
    `status`, `created_at`, `updated_at`, `archived_at`, `finalized_at`
)
SELECT 
    e.id AS employee_id,
    DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL m.month_offset MONTH), '%Y-%m-01') AS pay_period_start,
    LAST_DAY(DATE_SUB(CURDATE(), INTERVAL m.month_offset MONTH)) AS pay_period_end,
    SUM(wl.hours_worked * r.rate) AS gross_pay,
    SUM(wl.hours_worked * r.rate) * (1 - o.tax_rate) AS net_pay,
    'FINALIZED' AS status,
    NOW() AS created_at,
    NOW() AS updated_at,
    NULL AS archived_at,
    NOW() AS finalized_at
FROM 
    employees e
JOIN 
    roles r ON e.role_id = r.id
JOIN 
    worklogs wl ON e.id = wl.employee_id
JOIN
    organization o -- assuming single row org table
JOIN 
    (SELECT 0 AS month_offset UNION SELECT 1 UNION SELECT 2) m
WHERE 
    wl.date BETWEEN DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL m.month_offset MONTH), '%Y-%m-01') 
    AND LAST_DAY(DATE_SUB(CURDATE(), INTERVAL m.month_offset MONTH))
GROUP BY 
    e.id, m.month_offset
HAVING 
    SUM(wl.hours_worked) > 0;

-- Optional: Link payroll_worklogs with the worklogs used in each payroll (snapshot_locked=1 to lock them)
INSERT INTO `payroll_worklogs` (`payroll_id`, `worklog_id`, `hours_recorded`, `created_at`, `snapshot_locked`)
SELECT
    p.id AS payroll_id,
    wl.id AS worklog_id,
    wl.hours_worked AS hours_recorded,
    NOW() AS created_at,
    1 AS snapshot_locked
FROM
    payrolls p
JOIN
    worklogs wl ON wl.employee_id = p.employee_id
WHERE
    wl.date BETWEEN p.pay_period_start AND p.pay_period_end;

SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;