-- POSTGRESQL DATABASE SCHEMA

-- Create the database (run separately outside transaction)
-- CREATE DATABASE call_for_code_25;

-- Switch to the database (outside SQL script, in CLI or client)
-- \c call_for_code_25

-- Create ENUM type
CREATE TYPE MessageType AS ENUM ('text', 'image');

-- Create ENUM type
CREATE TYPE MessageDirection AS ENUM ('in', 'out');

-- UserProfiles table
CREATE TABLE UserProfiles (
    UserId SERIAL PRIMARY KEY,
    Username VARCHAR(50) NOT NULL,
    Phone VARCHAR(13) UNIQUE NOT NULL
);

-- MessageLogs table
CREATE TABLE MessageLogs (
    MessageId SERIAL PRIMARY KEY,
    UserId INT REFERENCES UserProfiles(UserId),
    MessageType MessageType NOT NULL,
    Direction MessageDirection NOT NULL,
    Content VARCHAR(200) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ModelRecommendation table
CREATE TABLE ModelRecommendation (
    RecommendationId SERIAL PRIMARY KEY,
    UserId INT REFERENCES UserProfiles(UserId),
    Content VARCHAR(200) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ImageMetadata table
CREATE TABLE ImageMetadata (
    ImageId SERIAL PRIMARY KEY,
    UserId INT REFERENCES UserProfiles(UserId),
    ImageUrl VARCHAR(200) NOT NULL,
    Caption VARCHAR(200) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

