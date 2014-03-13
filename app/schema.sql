/* Script for setting up the DB.
    - Clears the sign up table if it exits
    - Creates a new one
 */

drop table if exists signups;
drop table if exists groups;

create table signups (
    ID integer primary key autoincrement,
    FirstName text not null,
    LastName text not null,
    Email text not null unique,
    Country text not null,
    City text not null,
    Reference text not null
);

create table groups (
    ID integer primary key autoincrement,
    GroupName text not null unique,
    Priority text not null
);


