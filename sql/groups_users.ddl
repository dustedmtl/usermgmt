-- Table for storing groups
CREATE TABLE groups (
    group_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for the group
    group_name TEXT NOT NULL UNIQUE,             -- Group name, must be unique
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp when the group was created
);

-- Table for storing users
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique identifier for the user
    username TEXT NOT NULL UNIQUE,               -- Username, must be unique
    email TEXT NOT NULL UNIQUE,                  -- User email, must be unique
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp when the user was created
);

-- Table for storing group memberships (many-to-many relationship)
CREATE TABLE group_memberships (
    membership_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for the membership
    group_id INTEGER NOT NULL,                       -- Foreign key referring to the groups table
    user_id INTEGER NOT NULL,                        -- Foreign key referring to the users table
    role TEXT NOT NULL DEFAULT 'member',             -- Role of the user in the group (e.g., admin, member)
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Timestamp when the user joined the group
    FOREIGN KEY (group_id) REFERENCES groups(group_id) ON DELETE CASCADE, -- If a group is deleted, delete its memberships
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,    -- If a user is deleted, delete their memberships
    UNIQUE(group_id, user_id)                        -- Ensures that a user can only be in a group once
);
