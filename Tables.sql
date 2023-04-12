CREATE TABLE FORM (
    USERNAME VARCHAR2(30) ,
    PASSWORD VARCHAR(30),
    EMAIL VARCHAR2(30) PRIMARY KEY,
    DOB DATE
);

Create table cinema (
    CINEMA_ID VARCHAR2(10) Primary KEY,
    CINEMA_NAME VARCHAR2(30),
    CITY VARCHAR2(30)
);
create table movies(
   MOVIE_ID int primary key,
   TITLE varchar2(256),
   DESCRIPTION varchar2(512),
   LENGTH int,
   LANG varchar2(20),
   RELEASE_DATE date,
   GENRE varchar2(20)
);
DROP Sequence movies_seq;
CREATE SEQUENCE movies_seq
start with 1
maxvalue 9999999
minvalue 1
CYCLE
NOCACHE
NOORDER;


create or replace trigger A_trigger
    before insert on movies
    for each ROW
BEGIN
    if :new.movie_id is null THEN
        :new.movie_id := movies_seq.nextval;
    end if;
END;
/
INSERT INTO CINEMA VALUES('1','MetroPolis','Ahmedabad');
INSERT INTO CINEMA VALUES('2','Rajhansh Cinema','Ahmedabad');
INSERT INTO CINEMA VALUES('3','I-Max','Ahmedabad');
INSERT INTO CINEMA VALUES('4','Cinemplex','Ahmedabad');
INSERT INTO CINEMA VALUES('5','City Pulse','Gandhinagar');

INSERT INTO MOVIES VALUES(DEFAULT,'JOHN WICK 4','With the price on his head ever increasing, legendary hit man John Wick takes his fight against the High Table global as he seeks out the most powerful players in the underworld, from New York to Paris to Japan to Berlin.',169,'English','24-MAR-2023','Action,Sci');
INSERT INTO MOVIES VALUES(DEFAULT,'JOHN WICK 1','With the price on his head ever increasing, legendary hit man John Wick takes his fight against the High Table global as he seeks out the most powerful players in the underworld, from New York to Paris to Japan to Berlin.',169,'English','24-MAR-2023','Action,Sci');
INSERT INTO MOVIES VALUES(DEFAULT,'JOHN WICK 2','With the price on his head ever increasing, legendary hit man John Wick takes his fight against the High Table global as he seeks out the most powerful players in the underworld, from New York to Paris to Japan to Berlin.',169,'English','24-MAR-2023','Action,Sci');
INSERT INTO MOVIES VALUES(DEFAULT,'JOHN WICK 3','With the price on his head ever increasing, legendary hit man John Wick takes his fight against the High Table global as he seeks out the most powerful players in the underworld, from New York to Paris to Japan to Berlin.',169,'English','24-MAR-2023','Action,Sci');
INSERT INTO MOVIES VALUES(DEFAULT,'DRISHYAM','When the disappearance of a policewomans son threatens to ruin Vijays family, he leaves no stone unturned in order to shield his family.',163,'Hindi','31-JULY-2015','Suspence,Thriller');
INSERT INTO MOVIES VALUES(DEFAULT,'BHARAMASTRA','Copy of Marvel',143,'Hindi','31-OCT-2022','Myth,Action,Romance');




CREATE TABLE shows (
    show_ID VARCHAR2(20),
    Cinema_Id VARCHAR2(10),
    FOREIGN KEY (CINEMA_ID) REFERENCES CINEMA(CINEMA_ID),
    MOVIE_ID INT,
    FOREIGN KEY (MOVIE_ID) REFERENCES MOVIES(MOVIE_ID),
    screen_no int,
    Constraint show_Id PRIMARY Key (SHOW_ID)
);

Create or replace Trigger insert_show_id
    before insert on SHOWS
    for each row
Begin
    :new.show_ID := :NEW.Cinema_Id || TO_CHAR(:NEW.MOVIE_ID);
end;
/
insert into shows values(DEFAULT,'1',1,2);
insert into shows values(DEFAULT,'2',3,1);
insert into shows values(DEFAULT,'3',2,2);
insert into shows values(DEFAULT,'4',2,3);
insert into shows values(DEFAULT,'1',5,1);
insert into shows values(DEFAULT,'5',4,2);
insert into shows values(DEFAULT,'1',2,2);
select * from shows;
CREATE TABLE BOOKING (
    Show_ID VARCHAR2(10),
    CINEMA_ID INT,
    MOVIE_ID INT,
    CONSTRAINT book_show FOREIGN KEY (Show_Id) REFERENCES SHOWS(show_Id),
    AVAILABLE_SEAT INT
);
CREATE TABLE TICKETS(
    TICKET_ID INT PRIMARY KEY,
    USER_ID VARCHAR2(30),
    CONSTRAINT TICKET_user FOReign KEY (USER_ID) REFERENCES form(email),
    SHOW_ID varchar(20),
    CONSTRAINT ticket_show FOREIGN Key (Show_ID) REFERENCEs Shows(show_ID),
    NO_OF_TICKET INT,
    TOTAL_COST FLOAT
);
CREATE TABLE SEATS(
    TICKET_ID INT,
    FOREIGN KEY (TICKET_ID) REFERENCES TICKETS(TICKET_ID),
    ROW_NO CHAR(2),
    SEAT_NO INT
);
CREATE TABLE BILL(
    USER_ID VARCHAR2(30),
    TICKET_ID INT,
    FOREIGN KEY (USER_ID) REFERENCES FORM(EMAIL),
    FOREIGN KEY (TICKET_ID) REFERENCES TICKETS(TICKET_ID),
    PAYMENT_METHOD VARCHAR2(20),
    STATUS CHAR(5)
);

-- DROP Table bill;
-- DROP Table SEATS;
-- DROP Table TICKETS;
-- DROP Table BOOKING;
-- DROP Table shows;
-- DROP Table movies;
-- DROP Table cinema;
-- DROP Table form;
