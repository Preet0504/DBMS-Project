Drop table form;

CREATE TABLE FORM (
    USERNAME VARCHAR2(30) ,
    PASSWORD VARCHAR(30),
    EMAIL VARCHAR2(30) PRIMARY KEY,
    DOB DATE
);
INSERT INTO form VALUES(
    'FireGumz',
    '123',
    'aagam@gmail.com',
    '19-NOV-2002'
);
INSERT INTO form VALUES(
    'Saumil',
    'pizza',
    'saumil@gmail.com',
    '4-Nov-2003'
);
INSERT INTO form VALUES(
    'SabkeDaddy',
    '123',
    'preet@gmail.com',
    '5-APR-2004'
);
INSERT INTO form VALUES(
    'Dhruv',
    'buddy',
    'dhruv@gmail.com',
    '26-MAR-2003'
);
CREATE TABLE my_sequence (
  sequence_value movie_id
);
INSERT INTO my_sequence (sequence_value) VALUES (0);
CREATE TRIGGER my_table_trigger
BEFORE INSERT ON movies
FOR EACH ROW
BEGIN
  SELECT my_sequence.sequence_value + 1 INTO :new.id FROM dual;
  UPDATE my_sequence SET sequence_value = :new.id;
END;
create table movies(
   movie_id int primary key,
   title varchar2(256),
   description varchar2(512),
   duration int,
   language varchar2(20),
   release_date date,
   genre varchar2(20));
