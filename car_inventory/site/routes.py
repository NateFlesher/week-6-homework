from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from car_inventory.forms import CarForm
from car_inventory.models import Car, db


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


@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    my_car = CarForm()
    try:
        if request.method == 'POST' and my_car.validate_on_submit():
            make = my_car.make.data
            model = my_car.model.data
            price = my_car.price.data
            mpg = my_car.mpg.data
            max_speed = my_car.max_speed.data
            dimensions = my_car.dimensions.data
            weight = my_car.weight.data
            cost_of_production = my_car.cost_of_production.data
            user_token = current_user.token

            car = Car(make, model, price, mpg, max_speed, dimensions, weight, cost_of_production, user_token)

            db.session.add(car)
            db.session.commit()

            return redirect(url_for('site.profile'))
    
    except:
        raise Exception('Drone not created, please check your form and try again!')

    user_token = current_user.token

    cars = Car.query.filter_by(user_token = user_token)
    
    return render_template('profile.html', form = my_car, cars = cars)