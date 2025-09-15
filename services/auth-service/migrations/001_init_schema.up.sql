-- +goose Up
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	email VARCHAR(255) UNIQUE NOT NULL,
	password_hash VARCHAR(255) NOT NULL,
	is_active BOOLEAN DEFAULT true,
	is_verified BOOLEAN DEFAULT true,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	last_login_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE refresh_tokens (
	token VARCHAR(255) PRIMARY KEY,
	user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
	expires_at TIMESTAMP NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	revoked_at TIMESTAMP
);

CREATE TABLE roles (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50) UNIQUE NOT NULL,
	description TEXT
);

CREATE TABLE user_roles (
	user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
	role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
	UNIQUE(user_id, role_id)
);

INSERT INTO roles (name, description) VALUES
('admin', 'Администратор'),
('user', 'Обычный пользователь');
