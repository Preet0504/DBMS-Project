Drop table FORM;
CREATE TABLE FORM (
    USERNAME VARCHAR2(30) ,
    PASSWORD VARCHAR(30),
    EMAIL VARCHAR2(30) PRIMARY KEY,
    DOB DATE
);
INSERT INTO FORM VALUES(
    'FireGumz',
    '123',
    'aagam@gmail.com',
    '19-NOV-2002'
);
INSERT INTO FORM VALUES(
    'Saumil',
    'pizza',
    'saumil@gmail.com',
    '4-Nov-2003'
);
INSERT INTO FORM VALUES(
    'SabkeDaddy',
    '123',
    'preet@gmail.com',
    '5-APR-2004'
);
INSERT INTO FORM VALUES(
    'Dhruv',
    'buddy',
    'dhruv@gmail.com',
    '26-MAR-2003'
);
select * from form;