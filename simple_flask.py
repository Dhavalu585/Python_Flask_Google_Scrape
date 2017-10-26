from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests
import regex as re
from bs4 import BeautifulSoup

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

def find_following_line(text):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.search(re.compile('Wikipedia', re.IGNORECASE), line):
            introduction = lines[i-1]
            #introduction = introduction + "" + lines[i+2]
            flash(introduction)
        if re.search('Headquarters', line):
            headquarters = lines[i+1]
            flash("Headquarters:  " + headquarters)
        if re.search('Founded', line):
            founded = lines[i+1]
            flash("Founded:  " + founded)
        if re.search('Revenue', line):
            revenue = lines[i+1]
            flash("Revenue:  " + revenue)

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    #print form.errors
    if request.method == 'POST':
        name = request.form['name']
        #print name

        if form.validate():
            # Save the comment here.
            companyName = name
            searchString1 = companyName + "+software+developer+salary+glassdoor"
            # This URL is a general URL format. Just substitue your desired search string with q='yourSearch'. Let everything else stay the same.
            page = requests.get(
                "https://www.google.com/search?q=" + companyName + "&oq=" + companyName + "&aqs=chrome.0.69i59j69i60j0j69i60l2.2584j0j7&client=ubuntu&sourceid=chrome&ie=UTF-8").text
            soup = BeautifulSoup(page, 'html.parser')

            # Use inspect page to get the exact id or class of div
            soup_string = soup.find(id="rhs_block").get_text(separator='\n') + ""
            find_following_line(soup_string)

            page = requests.get(
                "https://www.google.com/search?q=" + searchString1 + "&oq=" + searchString1 + "&aqs=chrome.0.69i59j69i60j0j69i60l2.2584j0j7&client=ubuntu&sourceid=chrome&ie=UTF-8").text
            soup = BeautifulSoup(page, 'html.parser')
            soup_string = soup.find(id="search").get_text() + ""
            salary_index = re.search(re.compile(r'The typical (.*?) Software', re.IGNORECASE), soup_string)
            if salary_index is None:
                salary_index = re.search(re.compile(r'Average salaries for (.*?) Software', re.IGNORECASE), soup_string)
            if salary_index is not None:
                salary_index = salary_index.start()
                salary_index_end = soup_string.find('.', salary_index)
                salary = soup_string[salary_index:salary_index_end]
                flash(salary)
        else:
            flash('All the form fields are required. ')

    return render_template('hello.html', form=form)


if __name__ == "__main__":
    app.run()