/* Script for setting up the DB.
    - Clears the sign up table if it exits
    - Creates a new one
 */

drop table if exists signups;

create table signups (
    ID integer primary key autoincrement,
    FirstName text not null,
    LastName text not null,
    Email text not null unique,
    Country text not null,
    City text not null,
    Reference text not null
);


