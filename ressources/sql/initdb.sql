
-- table to contain the exercices 
CREATE TABLE exos(
    id                  integer not null primary key,
    title               text not null,                -- title to display on the exercices listing page
    problem             text not null,                -- a description of the problem to solve, some example of input /output
    possible_solution   text not null                 -- a possible solution to show when someone has finished an exercise
);


-- table to contain the users 
CREATE table users(
    id        integer not null primary key,
    name      text not null,
    email     text not null default "",
    password  text not null,
    group_id  integer not null default 0
);

-- table to contain the test a give exercises should 
-- pass to be considered as correct

CREATE TABLE tests(
    id      integer not null primary key,
    exo_id  integer not null,               -- the exercice this test is attached to
    stdin   text not null default "",       -- the input we will send to the software to test
    stdout  text not null default ""        -- the output we're supposed to receive 
);

