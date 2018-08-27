import os
from flask import Flask, request
from flask import jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, validators, ValidationError

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'asdasdasd',
    'DEBUG': True,
    'WTF_CSRF_ENABLED': False
})


class UserForm(FlaskForm):
    email = StringField(label='E-mail', validators=[
        validators.Length(min=5, max=35),
        validators.Email()
    ])
    password = StringField(label='password:', validators=[
        validators.Length(min=6, max=12)
    ])
    confirm_password = StringField(label='confirm password:', validators=[
        validators.Length(min=6, max=20)
    ])

    def validate_password(self, form):
        if self.data['password'] != self.data['confirm_password']:
            raise ValidationError('Пароль не совпадают')


@app.route('/form/user', methods=['GET', 'POST'])
def post_data():
    if request.method == 'POST':
        user_form = UserForm(request.form)
        status_output = {0: 'Проверка пройдена', 1: 'Ошибка валидации'}
        if user_form.validate():
            print('email:', request.form['email'])
            print('pass:', request.form['password'])
            status_check = jsonify(status_output[0])
            return status_check
        else:
            status_check = jsonify(status_output[1])
            error_list = jsonify(user_form.errors)
            print(user_form.errors)
            return status_check and error_list
    return 'Done!'


@app.route('/hello/<user>')
def hello_world(user):
    return 'Hello user: ' + user


@app.route('/hello/<int:num1>/<int:num2>')
def konk_nums(num1, num2):
    return 'Sum = {}'.format(num1 + num2)


@app.route('/long/<s1>/<s2>/<s3>')
def long_string(s1, s2, s3):
    mylist = [s1, s2, s3]
    return max(mylist, key=len)


@app.route('/<path:filename>')
def show_file(filename):
    if not os.path.exists('./files/' + filename):
        return '404'
    else:
        return 'Yes'


@app.route('/locales', methods=['GET', 'POST'])
def my_dict():
    my_locale = {'ru': 'russia', 'en': 'english', 'it': 'italian'}
    return jsonify(my_locale)


if __name__ == '__main__':
    app.run()