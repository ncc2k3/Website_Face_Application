CREATE TABLE users (
    id SERIAL PRIMARY KEY,  -- Sử dụng SERIAL để id tự động tăng
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(150) NOT NULL,
    face_encoding BYTEA
);
