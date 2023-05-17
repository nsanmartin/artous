from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



class PriceForm(FlaskForm):
    price = StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Convert to pesos')
