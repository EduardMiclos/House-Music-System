import sys, os
import pytest
import sqlite3 as sql

sys.path.append(os.path.join('..', 'Database'))
from DatabaseManager import DatabaseManager


"""
The __connect method should return False if the
specified database does not exist.
"""
def test_connect_wrong_path():
    wrong_path = "wrongpath"
    db_manager = DatabaseManager(wrong_path)

    assert db_manager._DatabaseManager__connect() == False

"""
The program should add a '.db' to the path of the
database in case it doesn't exist.
"""
def test_dbname_incomplete_input(db_manager):
    assert db_manager.db_name.endswith('.db')

"""
If the path to the database is complete, the program
shouldn't add a second '.db'.
"""
def test_dbname_complete_input():
    db_manager = DatabaseManager(pytest.db_path + '.db')
    
    assert db_manager.db_name.endswith('db')
    assert not db_manager.db_name.endswith('.db.db')

"""
Using the db_manager fixture, a connection should
be established.
"""
def test_db_connect(db_manager):
    assert db_manager._DatabaseManager__connect() == True

"""
If the opening mode is wrong, the program should
raise a sqlite3.OperationalError.
"""
def test_db_connect_wrong_openmode(db_manager):
    wrong_openmode = "wrongopenmode"

    with pytest.raises(sql.OperationalError):
       db_manager._DatabaseManager__connect(open_mode = wrong_openmode)



