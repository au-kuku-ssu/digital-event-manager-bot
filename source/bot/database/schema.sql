PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS universities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS faculties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    university_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (university_id)
        REFERENCES universities(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT,
    phone TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    title TEXT,
    degree TEXT,
    position TEXT,
    workplace TEXT,
    tg_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS venues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    street TEXT NOT NULL,
    building TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS organizers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    contact_number TEXT NOT NULL UNIQUE,
    access_key INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (person_id) REFERENCES people(id)
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_id INTEGER NOT NULL,
    organizer_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (venue_id) REFERENCES venues(id),
    FOREIGN KEY (organizer_id) REFERENCES organizers(id)
);

CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    lecture_hall TEXT NOT NULL,
    time TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS event_sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    FOREIGN KEY (section_id)
        REFERENCES sections(id)
        ON DELETE CASCADE,
    FOREIGN KEY (event_id)
        REFERENCES events(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS textbook_levels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level_abbreviation TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    university_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    person_id INTEGER NOT NULL,
    FOREIGN KEY (university_id) REFERENCES universities(id),
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (person_id) REFERENCES people(id)
);

CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    section_id INTEGER NOT NULL,
    person_id INTEGER NOT NULL,
    is_poster_participant INTEGER NOT NULL,
    is_translators_participate INTEGER NOT NULL,
    has_translator_education INTEGER NOT NULL,
    textbook_level_id INTEGER NOT NULL,
    is_group_leader INTEGER NOT NULL DEFAULT 0,
    presentation_topic TEXT,
    is_notification_allowed INTEGER NOT NULL,
    password TEXT NOT NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculties(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id),
    FOREIGN KEY (section_id) REFERENCES sections(id),
    FOREIGN KEY (person_id) REFERENCES people(id),
    FOREIGN KEY (textbook_level_id) REFERENCES textbook_levels(id)
);

CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    member_count INTEGER NOT NULL,
    registration_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (section_id) REFERENCES sections(id)
);

CREATE TABLE IF NOT EXISTS group_participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    participant_id INTEGER NOT NULL,
    FOREIGN KEY (group_id)
        REFERENCES groups(id)
        ON DELETE CASCADE,
    FOREIGN KEY (participant_id)
        REFERENCES participants(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (section_id)
        REFERENCES sections(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS group_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    FOREIGN KEY (group_id)
        REFERENCES groups(id)
        ON DELETE CASCADE,
    FOREIGN KEY (topic_id)
        REFERENCES topics(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS juries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    university_id INTEGER NOT NULL,
    person_id INTEGER NOT NULL,
    is_chairman INTEGER NOT NULL,
    access_key INTEGER NOT NULL,
    FOREIGN KEY (university_id) REFERENCES universities(id),
    FOREIGN KEY (person_id) REFERENCES people(id)
);

CREATE TABLE IF NOT EXISTS section_juries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER NOT NULL,
    jury_id INTEGER NOT NULL,
    FOREIGN KEY (section_id)
        REFERENCES sections(id)
        ON DELETE CASCADE,
    FOREIGN KEY (jury_id)
        REFERENCES juries(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS technical_requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL,
    format TEXT NOT NULL,
    width REAL NOT NULL,
    height REAL NOT NULL,
    units_of_measurement TEXT NOT NULL,
    FOREIGN KEY (topic_id)
        REFERENCES topics(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS posters_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    technical_requirements_id INTEGER NOT NULL,
    words_amount INTEGER NOT NULL,
    images_amount INTEGER NOT NULL,
    FOREIGN KEY (technical_requirements_id)
        REFERENCES technical_requirements(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS jury_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jury_id INTEGER NOT NULL,
    participant_id INTEGER NOT NULL,
    organization_criteria REAL NOT NULL,
    content_criteria REAL NOT NULL,
    visuals_criteria REAL NOT NULL,
    mechanics_criteria REAL NOT NULL,
    delivery_criteria REAL NOT NULL,
    comment TEXT,
    FOREIGN KEY (jury_id) REFERENCES juries(id),
    FOREIGN KEY (participant_id) REFERENCES participants(id)
);

CREATE TABLE IF NOT EXISTS jury_scores_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jury_scores_id INTEGER NOT NULL,
    jury_id INTEGER NOT NULL,
    update_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (jury_scores_id) REFERENCES jury_scores(id),
    FOREIGN KEY (jury_id) REFERENCES juries(id)
);

CREATE TABLE IF NOT EXISTS organizer_section_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER NOT NULL,
    organizer_id INTEGER NOT NULL,
    update_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (section_id) REFERENCES sections(id),
    FOREIGN KEY (organizer_id) REFERENCES organizers(id)
);

CREATE TABLE IF NOT EXISTS organizer_participant_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id INTEGER NOT NULL,
    organizer_id INTEGER NOT NULL,
    update_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (participant_id) REFERENCES participants(id),
    FOREIGN KEY (organizer_id) REFERENCES organizers(id)
);
