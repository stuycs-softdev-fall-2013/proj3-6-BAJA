-- Database schema
-- version 1

DROP TABLE IF EXISTS version;
CREATE TABLE version (
    version INTEGER
);
INSERT INTO version VALUES (%(version)s);

DROP TABLE IF EXISTS game_data;
CREATE TABLE game_data (
    gd_user INTEGER,
    gd_mission INTEGER,
    gd_status INTEGER,
    gd_attributes BLOB
);

DROP TABLE IF EXISTS qmail_users;
CREATE TABLE qmail_users (
    qmu_id INTEGER PRIMARY KEY,
    qmu_address BLOB,
    qmu_first_name TEXT,
    qmu_last_name TEXT,
    qmu_password_hash BLOB,
    qmu_password_salt BLOB
);

DROP TABLE IF EXISTS qmail_emails;
CREATE TABLE qmail_emails (
    qme_id INTEGER PRIMARY KEY,
    qme_subject TEXT,
    qme_body TEXT,
    qme_time INTEGER
);

DROP TABLE IF EXISTS qmail_email_members;
CREATE TABLE qmail_email_members (
    qmm_id INTEGER PRIMARY KEY,
    qmm_email INTEGER,
    qmm_type INTEGER,
    qmm_address BLOB,
    qmm_name TEXT
);

DROP TABLE IF EXISTS qmail_attachments;
CREATE TABLE qmail_attachments (
    qma_id INTEGER PRIMARY KEY,
    qma_email INTEGER,
    qma_filename BLOB,
    qma_content BLOB
);
