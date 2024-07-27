from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import db
from mlxtend.frequent_patterns import fpgrowth,association_rules
import csv
from sqlalchemy import join
import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
import plotly.express as px
from website import DB_NAME
from .models import Meal, Symptom, db, CombinedData,User

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("base.html", user=current_user)

@views.route('/title')
@login_required
def title():
    return render_template('title.html', user=current_user)

@views.route('/add_meal', methods=['POST'])
@login_required
def add_meal():
    if request.method == 'POST':
        meal_name = request.form.get('inputmeal')
        meal_date = request.form.get('inputDate')
        meal_time = request.form.get('inputTime')
        
        meal_datetime = datetime.strptime(meal_date + ' ' + meal_time, '%Y-%m-%d %H:%M')
        
        new_meal = Meal(user=current_user, meal_name=meal_name, meal_datetime=meal_datetime)
        db.session.add(new_meal)
        db.session.commit()

    return redirect(url_for('views.title'))

@views.route('/add_symptom', methods=['POST'])
@login_required
def add_symptom():
    if request.method == 'POST':
        symptom_name = request.form.get('inputsymptom')
        symptom_date = request.form.get('inputdate')
        symptom_time = request.form.get('inputtime')
        
        symptom_datetime = datetime.strptime(symptom_date + ' ' + symptom_time, '%Y-%m-%d %H:%M')
        
        new_symptom = Symptom(user=current_user, symptom_name=symptom_name, symptom_datetime=symptom_datetime, severity_level=1)
        db.session.add(new_symptom)
        db.session.commit()
        

    return redirect(url_for('views.title'))




@views.route('/frequent_patterns')
def frequent_patterns():
    meal_count = Meal.query.filter_by(user_id=current_user.id).count()
    symptom_count = Symptom.query.filter_by(user_id=current_user.id).count()
    
    if meal_count < 10 or symptom_count < 10:
        return render_template('title.html', user=current_user)
    
    joined_table_data = db.session.query(Meal.meal_name, Symptom.symptom_name) \
        .join(Symptom, Meal.user_id == Symptom.user_id).all()
    
    csv_file_path = 'joined_table_data.csv'

    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Meal Name', 'Symptom Name'])
        for row in joined_table_data:
            csv_writer.writerow([row.meal_name, row.symptom_name])

    data = pd.read_csv(csv_file_path)
    
    transaction = []
    for i in range(data.shape[0]):
        transaction.append([str(data.values[i, j]) for j in range(data.shape[1])])

    transaction_np = np.array(transaction)
    transaction_np[transaction_np == 'True'] = '1'
    transaction_np[transaction_np == 'False'] = '0'
    
    te = TransactionEncoder()
    te_ary = te.fit(transaction_np).transform(transaction_np)
    data_encoded = pd.DataFrame(te_ary, columns=te.columns_)
    
    res = fpgrowth(data_encoded, min_support=0.05, use_colnames=True)
    res = association_rules(res, metric="lift", min_threshold=1)
    
    
    res = res.sort_values("confidence", ascending=False)
    
    return render_template('frequent_patterns.html', rules=res)






