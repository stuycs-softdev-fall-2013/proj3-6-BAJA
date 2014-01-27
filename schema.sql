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
    qmu_address TEXT,
    qmu_first_name TEXT,
    qmu_last_name TEXT,
    qmu_password_hash TEXT,
    qmu_password_salt TEXT
);

DROP TABLE IF EXISTS qmail_mailboxes;
CREATE TABLE qmail_mailboxes (
    qmm_id INTEGER PRIMARY KEY,
    qmm_user INTEGER
);

DROP TABLE IF EXISTS qmail_emails;
CREATE TABLE qmail_emails (
    qme_id INTEGER PRIMARY KEY,
    qme_sender INTEGER,
    qme_subject TEXT,
    qme_body TEXT,
    qme_has_attachments BOOLEAN
);

DROP TABLE IF EXISTS qmail_recipients;
CREATE TABLE qmail_recipients (
    qmr_id INTEGER PRIMARY KEY,
    qmr_message INTEGER,
    qmr_recipient INTEGER,
    qmr_type INTEGER,
    qmr_address TEXT,
    qmr_name TEXT
);

DROP TABLE IF EXISTS qmail_attachments;
CREATE TABLE qmail_attachments (
    qma_id INTEGER PRIMARY KEY,
    qma_message INTEGER,
    qma_filename TEXT,
    qma_content BLOB
);
