START TRANSACTION;
DROP TABLE IF EXISTS user;
CREATE TABLE IF NOT EXISTS user (
    id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(100) NOT NULL,
    email VARCHAR(40) NOT NULL UNIQUE,
    password VARCHAR(120) NOT NULL,
    tag VARCHAR(20) NOT NULL,
    user_type VARCHAR(10) NOT NULL
);
INSERT INTO user VALUES (1,'','admin','admin','admin');


CREATE TABLE locker (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE compartment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    locker_id INT NOT NULL,
    number INT NOT NULL,
    FOREIGN KEY (locker_id) REFERENCES locker(id)
    UNIQUE (locker_id, number)
);

CREATE TABLE compartment_usage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    compartment_id INT NOT NULL,
    open_time DATETIME NOT NULL,
    close_time DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id_user),
    FOREIGN KEY (compartment_id) REFERENCES compartment(id),
    UNIQUE (user_id)  -- Garante que um usuário só possa usar um compartimento por vez.
);

CREATE TABLE locker_schedule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    compartment_id INT NOT NULL,
	user_id INT NOT NULL,
    open_time DATETIME NOT NULL,
    close_time DATETIME NOT NULL,
    retrieve_time DATETIME NOT NULL,
    end_retrieve_time DATETIME NOT NULL,
    FOREIGN KEY (compartment_id) REFERENCES compartment(id),
	FOREIGN KEY (user_id) REFERENCES user(id_user)
);

CREATE TABLE forgot_password (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) NOT NULL,
    date_time DATETIME NOT NULL,
	user_id INT NOT NULL,
	FOREIGN KEY (user_id) REFERENCES user(id),
    UNIQUE (user_id)
);

COMMIT;

drop table compartment_usage;
drop table locker_schedule;
drop table compartment;
drop table locker;