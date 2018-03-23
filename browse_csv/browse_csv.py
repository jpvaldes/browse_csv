from flask import render_template, url_for, redirect, Flask
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from pathlib import Path
from werkzeug.utils import secure_filename
from wtforms import SubmitField
# from app import app
from .io import load_data, save_decision

# create application
app = Flask('browse_csv')
bootstrap = Bootstrap(app)

# view function with route decorators
@app.route('/')
@app.route('/index')
def index():
    app_path = Path(app.instance_path)
    data_file = app_path / 'data' / 'data.csv'
    contents = False
    if data_file.exists():
        contents = True
    return render_template('index.html', contents=contents)


class DecisionForm(FlaskForm):
    class Meta:
        csrf = False
    submit_yes = SubmitField(label='Yes')
    submit_no = SubmitField(label='No')
    submit_na = SubmitField(label="Don't know")


@app.route('/content/<int:idx>', methods=['GET', 'POST'])
def content(idx):
    button_form = DecisionForm()
    app_path = Path(app.instance_path)
    data_file = app_path / 'data' / 'data.csv'
    decisions_file = app_path / 'data' / 'decision.csv'
    cards = load_data(str(data_file))
    total_entries = len(cards)
    has_next = True if idx + 1 < total_entries else False
    has_prev = True if idx > 0 else False
    entry_ref = {'entry': f'{idx + 1}', 'total_entries': f'{total_entries}'}
    next_url = url_for('content', idx=(idx + 1)) if has_next else None
    prev_url = url_for('content', idx=(idx - 1)) if has_prev else None
    if button_form.validate_on_submit():
        yes = 'true' if button_form.submit_yes.data else 'false'
        no = 'true' if button_form.submit_no.data else 'false'
        na = 'true' if button_form.submit_na.data else 'false'
        save_decision(decisions_file, idx, yes, no, na)
        return redirect(next_url)
    return render_template('content.html', card=cards.iloc[idx], ref=entry_ref,
                           button_form=button_form,
                           next_url=next_url, prev_url=prev_url)


class CSVUploadForm(FlaskForm):
    class Meta:
        csrf = False
    csv = FileField('Choose a valid CSV file and press submit:',
                    validators=[FileRequired(message='Please, choose a file'),
                                FileAllowed(['csv'], 'csv file')])
    submit = SubmitField()


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = CSVUploadForm()
    app_path = Path(app.instance_path)
    data_path = app_path / 'data'
    data_path.mkdir(parents=True, exist_ok=True)
    if form.validate_on_submit():
        f = form.csv.data
        filename = secure_filename(f.filename)
        data_file = data_path / 'data.csv'
        f.save(str(data_file))
        return redirect(url_for('index'))

    return render_template('upload.html', form=form)

