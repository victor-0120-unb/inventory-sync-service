CREATE DATABASE IF NOT EXISTS solstice_checkin;

USE solstice_checkin;


-- =========================
-- ATTENDEES
-- =========================

CREATE TABLE IF NOT EXISTS attendees (
    attendee_id INT AUTO_INCREMENT PRIMARY KEY,
    qr_code VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    status ENUM('PENDING', 'CHECKED_IN') NOT NULL DEFAULT 'PENDING',
    checked_in_at TIMESTAMP NULL
);


-- =========================
-- PRINT JOBS
-- =========================

CREATE TABLE IF NOT EXISTS print_jobs (
    job_id VARCHAR(100) PRIMARY KEY,
    attendee_id INT NOT NULL,
    status ENUM('PENDING', 'COMPLETED') NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,

    FOREIGN KEY (attendee_id)
        REFERENCES attendees(attendee_id),

    UNIQUE (attendee_id)
);


-- =========================
-- MOCK ATTENDEES
-- =========================

INSERT IGNORE INTO attendees
(qr_code, full_name, status)
VALUES
('QR-1001', 'Amina Wanjiku', 'PENDING'),
('QR-1002', 'Brian Otieno', 'PENDING'),
('QR-1003', 'Carol Mwangi', 'PENDING');