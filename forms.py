from datetime import datetime
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, ValidationError, Length, Optional
from customenums import GenresEnum, StatesEnum
import phonenumbers

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    
    def validate_genres(self, field):
        values = [ choice.value for choice in GenresEnum ]
        
        errorValue = ""
        for value in field.data:
            if value not in values:
                errorValue = value
                break

        if errorValue is not "":
            raise ValidationError('{0} is not an acceptable value', errorValue)
        
    
    
    name = StringField(
        'name', validators=[DataRequired(), Length(-1,120)]
    )
    city = StringField(
        'city', validators=[DataRequired(), Length(-1,120)]
    )
    state = SelectField(
        'state', validators=[DataRequired(),  AnyOf( [ choice.value for choice in StatesEnum ] )],
        choices=StatesEnum.choices()
    )
    address = StringField(
        'address', validators=[DataRequired(), Length(-1,120)]
    )
    phone = StringField(
        'phone',
        validators=[Length(-1,120),Optional()]
    )
    image_link = StringField(
        'image_link',
        validators=[Length(-1,500),URL(),Optional()]
    )
    genres = SelectMultipleField(
        'genres', 
        validators=[DataRequired()],
        choices=GenresEnum.choices()
    )
    facebook_link = StringField(
        'facebook_link',
        validators=[Length(-1,120),URL(),Optional()]
    )
    website_link = StringField(
        'website_link',
        validators=[Length(-1,120),URL(),Optional()]
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description',
        validators=[Length(-1,120),Optional()]
    )



class ArtistForm(Form):
    def validate_genres(self, field):
        values = [ choice.value for choice in GenresEnum ]
        
        errorValue = ""
        for value in field.data:
            if value not in values:
                errorValue = value
                break

        if errorValue is not "":
            raise ValidationError('{0} is not an acceptable value', errorValue)
        
    def validate_phone(form, field):
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1"+field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

     
    name = StringField(
        'name', validators=[DataRequired(), Length(-1,120)]
    )
    city = StringField(
        'city', validators=[DataRequired(), Length(-1,120)]
    )
    state = SelectField(
        'state', validators=[DataRequired(),  AnyOf( [ choice.value for choice in StatesEnum ] )],
        choices=StatesEnum.choices()
    )
    phone = StringField(
        'phone',
        validators=[Length(-1,120),Optional()]
    )
    image_link = StringField(
        'image_link',
        validators=[Length(-1,500),URL(),Optional()]
    )
    genres = SelectMultipleField(
        'genres', 
        validators=[DataRequired()],
        choices=GenresEnum.choices()
    )
    facebook_link = StringField(
        'facebook_link',
        validators=[Length(-1,120),URL(),Optional()]
    )
    website_link = StringField(
        'website_link',
        validators=[Length(-1,120),URL(),Optional()]
    )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
        'seeking_description',
        validators=[Length(-1,120),Optional()]
    )

