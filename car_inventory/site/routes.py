from flask import Blueprint, render_template


site = Blueprint('site', __name__, template_folder='site_templates')

"""
Note in the above code, some arguments are specified when creating the
Blueprint object. The first argument, 'site', is the Blueprint's name, this is used by
Flask's routing mechanism. The second argument, __name__, is the Blueprint's import name,
Which Flask uses to locate the Blueprint's resources

"""

@site.route('/')
def home():
    return render_template('index.html')


@site.route('/profile')
def profile():
    return render_template('profile.html')