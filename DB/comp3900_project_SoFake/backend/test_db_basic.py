import pytest
import sqlite3
import os
from database.db import init_db, insert_news, get_all_news, DB_NAME

def test_basic_crud():
    """验证最基础的增删改查逻辑"""
    # 1. 初始化（确保表能建成功）
    init_db()
    
    # 2. 插入一条新闻
    test_str = "This is a basic test content."
    news_id = insert_news(test_str)
    
    # 3. 验证返回的 ID 是否有效
    assert news_id is not None
    assert news_id > 0
    
    # 4. 获取所有新闻并比对内容
    news_list = get_all_news()
    # 检查最新插入的那一条（因为 get_all_news 是 DESC 排序）
    assert news_list[0][1] == test_str
