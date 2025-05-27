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

-- Insert roles with default statuses (no ARCHIVED)
INSERT INTO `roles` (`name`, `rate`, `status`, `archived_at`) VALUES
('Software Developer', 35.50, 'ACTIVE', NULL),
('Nurse', 28.75, 'ACTIVE', NULL),
('Teacher', 25.00, 'ACTIVE', NULL),
('Electrician', 30.25, 'ACTIVE', NULL),
('Accountant', 32.00, 'ACTIVE', NULL),
('Marketing Specialist', 27.50, 'ACTIVE', NULL),
('Construction Worker', 22.00, 'ACTIVE', NULL),
('Customer Service', 18.50, 'ACTIVE', NULL);

-- Insert employees with default statuses (no ARCHIVED)
INSERT INTO `employees` (
    `first_name`, `last_name`, `role_id`, `email`, `status`, `created_at`, `updated_at`, `archived_at`
) VALUES
('Juan', 'Dela Cruz', 1, 'juan.delacruz@example.com', 'ACTIVE', NOW(), NOW(), NULL),
('Maria', 'Santos', 2, 'maria.santos@example.com', 'INACTIVE', NOW(), NOW(), NULL),
('Jose', 'Reyes', 3, 'jose.reyes@example.com', 'INACTIVE', NOW(), NOW(), NULL),
('Ana', 'Gonzales', 4, 'ana.gonzales@example.com', 'ACTIVE', NOW(), NOW(), NULL),
('Pedro', 'Bautista', 5, 'pedro.bautista@example.com', 'ACTIVE', NOW(), NOW(), NULL),
('Luzviminda', 'Tan', 6, 'luzviminda.tan@example.com', 'ACTIVE', NOW(), NOW(), NULL),
('Ricardo', 'Lim', 7, 'ricardo.lim@example.com', 'INACTIVE', NOW(), NOW(), NULL),
('Corazon', 'Ong', 8, 'corazon.ong@example.com', 'ACTIVE', NOW(), NOW(), NULL),
('Eduardo', 'Sy', 1, 'eduardo.sy@example.com', 'ACTIVE', NOW(), NOW(), NULL),
('Imelda', 'Chua', 2, 'imelda.chua@example.com', 'INACTIVE', NOW(), NOW(), NULL),
('Anders', 'Johansson', 3, 'anders.johansson@example.com', 'ACTIVE', NOW(), NOW(), NULL),
('Elin', 'Nilsson', 4, 'elin.nilsson@example.com', 'ACTIVE', NOW(), NOW(), NULL),
('Lars', 'Andersson', 5, 'lars.andersson@example.com', 'ACTIVE', NOW(), NOW(), NULL),
('Anna', 'Karlsson', 6, 'anna.karlsson@example.com', 'INACTIVE', NOW(), NOW(), NULL),
('Johan', 'Eriksson', 7, 'johan.eriksson@example.com', 'ACTIVE', NOW(), NOW(), NULL),
('Maria', 'Larsson', 8, 'maria.larsson@example.com', 'ACTIVE', NOW(), NOW(), NULL),
('Per', 'Olsson', 1, 'per.olsson@example.com', 'ACTIVE', NOW(), NOW(), NULL),
('Karin', 'Persson', 2, 'karin.persson@example.com', 'ACTIVE', NOW(), NOW(), NULL),
('Erik', 'Svensson', 3, 'erik.svensson@example.com', 'ACTIVE', NOW(), NOW(), NULL),
('Sofia', 'Gustafsson', 4, 'sofia.gustafsson@example.com', 'ACTIVE', NOW(), NOW(), NULL);

-- Insert worklogs (~30 per employee) with statuses ACTIVE or LOCKED only, no ARCHIVED
INSERT INTO `worklogs` (`employee_id`, `date`, `hours_worked`, `status`, `created_at`, `updated_at`, `archived_at`, `locked_at`)
SELECT 
    e.id,
    DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 90) DAY),
    ROUND(4 + (RAND() * 8), 2),
    ELT(FLOOR(1 + (RAND() * 2)), 'ACTIVE', 'LOCKED'),
    NOW(),
    NOW(),
    NULL,
    IF(RAND() < 0.3, NOW(), NULL)
FROM 
    employees e,
    (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL
     SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL
     SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL
     SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19 UNION ALL SELECT 20 UNION ALL
     SELECT 21 UNION ALL SELECT 22 UNION ALL SELECT 23 UNION ALL SELECT 24 UNION ALL SELECT 25 UNION ALL
     SELECT 26 UNION ALL SELECT 27 UNION ALL SELECT 28 UNION ALL SELECT 29 UNION ALL SELECT 30) AS x;

-- Insert payrolls for last 3 months, finalized only if all linked worklogs are locked, else draft
INSERT INTO `payrolls` (
    `employee_id`, `start_date`, `end_date`, `gross_pay`, `net_pay`,
    `status`, `created_at`, `updated_at`, `archived_at`, `finalized_at`
)
SELECT 
    e.id,
    DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL m.month_offset MONTH), '%Y-%m-01'),
    LAST_DAY(DATE_SUB(CURDATE(), INTERVAL m.month_offset MONTH)),
    SUM(w.hours_worked * r.rate),
    ROUND(SUM(w.hours_worked * r.rate) * (1 - o.tax_rate), 2),
    CASE
        WHEN MIN(w.status) = 'LOCKED' THEN 'FINALIZED'
        ELSE 'DRAFT'
    END AS status,
    NOW(), NOW(),
    NULL,
    CASE
        WHEN MIN(w.status) = 'LOCKED' THEN NOW()
        ELSE NULL
    END AS finalized_at
FROM 
    employees e
JOIN roles r ON r.id = e.role_id
JOIN worklogs w ON w.employee_id = e.id
JOIN organization o
JOIN (SELECT 0 AS month_offset UNION ALL SELECT 1 UNION ALL SELECT 2) m
WHERE w.date BETWEEN DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL m.month_offset MONTH), '%Y-%m-01')
                 AND LAST_DAY(DATE_SUB(CURDATE(), INTERVAL m.month_offset MONTH))
GROUP BY e.id, m.month_offset, r.rate, o.tax_rate;

-- Link payroll_worklogs
INSERT INTO `payroll_worklogs` (`payroll_id`, `worklog_id`, `hours_recorded`, `created_at`, `snapshot_locked`)
SELECT
    p.id,
    w.id,
    w.hours_worked,
    NOW(),
    1
FROM payrolls p
JOIN worklogs w ON w.employee_id = p.employee_id
WHERE w.date BETWEEN p.start_date AND p.end_date;

SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;