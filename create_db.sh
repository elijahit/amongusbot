#!/bin/sh

sqlite3 provadb.db -cmd "CREATE TABLE tickets(ID number, Name text, Creato text, Joined text);"
