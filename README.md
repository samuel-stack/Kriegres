# Kriegres
------------------
Wrapper for simpler interaction with Postgres via Psycopg2

![Krieg](./images/krieg.jpg)

----------

### Why Kriegres ?
Lets be honest, Psycopg2 is somewhat tedious and repetitive to use with manually having to specify databases on a server, setting connections, generating a cursor, opening and closing connections.  I was annoyed with how I had to continue to use several repeatable actions in order to query, or adding additional actions in order to insert and return data in a format I wanted.  I decided to make a class object to automate much of the repetitive stuff and continued building on to it with whatever actions I could think of.  It became my first attempt at building a library which was a fun engineering project.

------------

### What is Kriegres ?
Kriegres is a Wrapper for interacting with Postgres SQL servers with Psycopg2. It automates the repetitive aspects of working with Psycopg2, so I can do what I actually need to do.  

-------------

### When to use Kriegres ?
I can't tell you when to use this or if its any good, but basically I'm going to use it when I have to interact with a Postgres database and for whatever reason Psycopg2 is my only means of doing so.

-------------

### How to use Kriegres ?
Check out the [Kriegres Usage Notebook](./Kriegres-Usage.ipynb)

-------------

### Who is Kriegres ?
If you never played [Borderlands 2](https://en.wikipedia.org/wiki/Borderlands_2) you probably want to know what the heck that picture is of and what it has to do with SQL.  Its a picture of a character named Krieg.  Krieg is a Psycho. I pronounce "Pyscopg2" as "Psycho-P-G-2".  Unlike other psychos in Borderlands, Krieg is good.  Unlike other ways to use postgres, this one is good (ish).
