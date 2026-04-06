import pytest
import sqlite3
import os
from DB.comp3900_project_SoFake.backend.database.db import init_db, insert_news, get_all_news, DB_NAME

def test_basic_crud():
    """Verify the most basic CRUD (Create, Read, Update, Delete) logic"""
    # 1. Initialization (Ensure the table is created successfully)
    init_db()
    
    # 2. Insert a single news item
    test_str = "This is a basic test content."
    news_id = insert_news(test_str)
    
    # 3. Verify if the returned ID is valid
    assert news_id is not None
    assert news_id > 0
    
    # 4. Retrieve all news and compare the content
    news_list = get_all_news()
    # Check the most recently inserted item (since get_all_news uses DESC ordering)
    assert news_list[0][1] == test_str