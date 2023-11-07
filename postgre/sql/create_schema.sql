-- table user
create table if not exists users (
    id serial primary key,
    name varchar(50) not null,
    userName varchar(50) not null unique,
    email varchar(50) not null unique,
    password varchar(100) not null unique
);