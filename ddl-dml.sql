START TRANSACTION;
DROP TABLE IF EXISTS user;
CREATE TABLE IF NOT EXISTS user (
    id_user INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(100) NOT NULL,
    email VARCHAR(40) NOT NULL UNIQUE,
    password VARCHAR(120) NOT NULL,
    tag VARCHAR(20) NOT NULL,
    user_type VARCHAR(10) NOT NULL
);
INSERT INTO user VALUES (1,'','admin','admin','admin');


CREATE TABLE Lockers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE Compartments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    locker_id INT NOT NULL,
    numero INT NOT NULL,
    FOREIGN KEY (locker_id) REFERENCES Lockers(id)
);

CREATE TABLE CompartmentUsage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    compartment_id INT NOT NULL,
    data_abertura DATETIME NOT NULL,
    data_retirada DATETIME,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (compartment_id) REFERENCES Compartments(id),
    UNIQUE (user_id)  -- Garante que um usuário só possa usar um compartimento por vez.
);

CREATE TABLE locker_schedules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    compartment_id INT NOT NULL,
	user_id INT,
    open_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    close_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    retrieve_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    end_retrieve_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (compartment_id) REFERENCES lockers(locker_id),
	FOREIGN KEY (user_id) REFERENCES Users(id),
);

COMMIT;
