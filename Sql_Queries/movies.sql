drop table movies;

create table movies(
   movie_id int primary key,
   title varchar2(256),
   description varchar2(512),
   duration int,
   language varchar2(20),
   release_date date,
   genre varchar2(20));
   

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
insert into movies values(DEFAULT,'Demon slayer','anime',120,'japenese','25-MAR-2023','Action');
insert into movies values(DEFAULT,'Avatar 2','nice cinematogrphy',180,'English','01-MAR-2023','Sci-fi');
insert into movies values(DEFAULT,'Jurasic World','dinosaurs',150,'Hinglish','01-APR-2023','Biology');
select * from movies;
select * from FORM

