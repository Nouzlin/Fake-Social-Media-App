drop table if exists signups;

create table signups (
    ID integer primary key autoincrement,
    FirstName text not null,
    LastName text not null,
    Age integer not null,
    Country text not null,
    City text not null,
    Reference text not null
);


