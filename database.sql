/*
	Project Name : Rabo
	Group : 06
	Members : Sumaiya Akter, 011191180 & Muhib Al Hasan, 011191083
*/



DROP DATABASE IF EXISTS Rabo;
CREATE DATABASE IF NOT EXISTS Rabo;
USE Rabo;

CREATE TABLE project
  (
     id         INT(11) PRIMARY KEY AUTO_INCREMENT,
     name       VARCHAR(255) NOT NULL,
     `desc`     VARCHAR(255),
     created_at DATETIME NULL,
     deadline DATETIME NULL
  );


CREATE TABLE notice
  (
     id         INT(11) PRIMARY KEY AUTO_INCREMENT,
     data       TEXT,
     posted_at  DATETIME NULL,
     type       VARCHAR(11),
     title 		VARCHAR(150),
     project_id INT(11) NOT NULL,
     CONSTRAINT project_notice FOREIGN KEY (project_id) REFERENCES project (id) ON DELETE CASCADE ON UPDATE CASCADE
  );



CREATE TABLE `user`
  (
     id         INT(11) PRIMARY KEY AUTO_INCREMENT,
     first_name VARCHAR(20) NOT NULL,
     last_name  VARCHAR(20) NOT NULL,
     password   VARCHAR(255) NOT NULL,
     email      VARCHAR(100) UNIQUE NOT NULL,
     picture    VARCHAR(255),
     bio        VARCHAR(255),
     created_at DATETIME NOT NULL
  );


CREATE TABLE sessions (
  id         INT(11) PRIMARY KEY AUTO_INCREMENT,
  session_id VARCHAR(255) NOT NULL UNIQUE,
  created_at DATETIME NOT NULL,
  user_id    INT(11),

  CONSTRAINT session FOREIGN KEY(user_id) REFERENCES `user`(id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE message
  (
     id         INT(11) PRIMARY KEY AUTO_INCREMENT,
     send_at    DATETIME NULL,
     msg_text       TEXT NOT NULL,
     project_id INT(11) NOT NULL,
     sent_by    INT(11),
     
     CONSTRAINT conversation FOREIGN KEY (project_id) REFERENCES project (id) ON DELETE CASCADE ON UPDATE CASCADE,
     CONSTRAINT msg_sent_by FOREIGN KEY (sent_by) REFERENCES `user` (id) ON DELETE SET NULL ON UPDATE CASCADE
  );


CREATE TABLE notification
  (
     id         INT(11) PRIMARY KEY AUTO_INCREMENT,
     data       TEXT,
     created_at DATETIME NULL,
     type       VARCHAR(10),
     sent_to    INT(11) NOT NULL,
     sent_by    INT(11) NULL,
     project_id INT(11) NULL,
     
     CONSTRAINT noti_sent_to FOREIGN KEY (sent_to) REFERENCES `user` (id) ON DELETE CASCADE ON UPDATE CASCADE,
     CONSTRAINT noti_sent_by FOREIGN KEY (sent_by) REFERENCES `user` (id) ON DELETE SET NULL ON UPDATE CASCADE,
     CONSTRAINT noti_sent_from FOREIGN KEY (project_id) REFERENCES `project` (id) ON DELETE CASCADE ON UPDATE CASCADE
  );


CREATE TABLE task
  (
     id           INT(11) PRIMARY KEY AUTO_INCREMENT,
     label        VARCHAR(255),
     `desc`       VARCHAR(255),
     deadline     DATETIME NULL,
     urgency      VARCHAR(11),
     created_at   DATETIME NULL,
     completed_at DATETIME NULL,
     category     VARCHAR(50) NOT NULL,
     managed_by   INT(11),
     created_by   INT(11),
     project_id   INT(11) NOT NULL,
     assigned_to  INT(11) NULL,

     CONSTRAINT has FOREIGN KEY (project_id) REFERENCES project (id) ON DELETE CASCADE ON UPDATE CASCADE,
     CONSTRAINT manages FOREIGN KEY (managed_by) REFERENCES `user`(id) ON DELETE SET NULL ON UPDATE CASCADE,
     CONSTRAINT task_assigned_to FOREIGN KEY (assigned_to) REFERENCES `user`(id) ON DELETE SET NULL ON UPDATE CASCADE,
     CONSTRAINT created_task FOREIGN KEY (created_by) REFERENCES `user`(id) ON DELETE SET NULL ON UPDATE CASCADE
  );


CREATE TABLE task_dependency (
  independent int(11) NOT NULL, 
  dependent   int(11) NOT NULL, 
  CONSTRAINT pk_task_dependency PRIMARY KEY (independent, dependent),
  CONSTRAINT independent FOREIGN KEY (independent) REFERENCES task (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT dependant FOREIGN KEY (dependent) REFERENCES task (id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE feedback
  (
     id       INT(11) PRIMARY KEY AUTO_INCREMENT,
     given_by INT(11) NULL,
     given_to INT(11) NULL,
     data     TEXT,
     given_at DATETIME NULL,

     CONSTRAINT feedback_given_to FOREIGN KEY (given_to) REFERENCES task (id) ON DELETE SET NULL ON UPDATE CASCADE,
     CONSTRAINT feedback_given_by FOREIGN KEY (given_by) REFERENCES `user` (id) ON DELETE SET NULL ON UPDATE CASCADE
  );


CREATE TABLE works_on
  (
     project_id INT(11) NOT NULL,
     user_id    INT(11) NOT NULL,
     role       VARCHAR(10),
     CONSTRAINT pk_works PRIMARY KEY (project_id, user_id),

     CONSTRAINT fkworks_on870897 FOREIGN KEY (project_id) REFERENCES project (id) ON DELETE CASCADE ON UPDATE CASCADE,
     CONSTRAINT fkworks_on729755 FOREIGN KEY (user_id) REFERENCES `user` (id) ON DELETE CASCADE ON UPDATE CASCADE
  );


CREATE TABLE Status (
  id         int(11) NOT NULL AUTO_INCREMENT, 
  type       varchar(20), 
  `from`     datetime NULL, 
  `to`       datetime NULL, 
  task_id    int(11) NOT NULL, 
  created_by int(11) NULL, 
  CONSTRAINT pk_status PRIMARY KEY (id, task_id),
  CONSTRAINT created FOREIGN KEY (created_by) REFERENCES `user` (id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT status_history FOREIGN KEY (task_id) REFERENCES task(id)
  );



CREATE TABLE Subscription (
  id         int(11) PRIMARY KEY AUTO_INCREMENT, 
  amount     int(10) NOT NULL, 
  start_date datetime NOT NULL, 
  end_date   datetime NOT NULL, 
  txn_type   varchar(10) NOT NULL, 
  card_no    int(11) NOT NULL, 
  txn_by     int(11) NOT NULL,
  CONSTRAINT subs FOREIGN KEY (txn_by) REFERENCES `user` (id) ON DELETE CASCADE ON UPDATE CASCADE
);