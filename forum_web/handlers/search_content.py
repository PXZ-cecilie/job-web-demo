#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from ..models import Article

search_content = Blueprint('search_content', __name__)
#endpoint for search

@search_content.route('/search_content', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        kw = request.form['keyword']

        select_s = "SELECT title, details from article WHERE details LIKE %s OR title LIKE %s"
        
        cursor.execute(select_s, (kw, kw))
        
        conn.commit()
        data = cursor.fetchall()
        # all in the search box will return all the tuples
        if len(data) == 0 and kw == 'all': 
            cursor.execute("SELECT * from article")
            conn.commit()
            data = cursor.fetchall()
        return render_template('search.html', data=data)
    return render_template('search.html')
'''