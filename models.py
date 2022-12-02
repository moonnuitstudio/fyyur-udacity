from flask_sqlalchemy import SQLAlchemy
from customenums import GenresEnum, StatesEnum

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.Enum(StatesEnum), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))
    genres = db.Column(db.String(120), nullable=False)
    
    shows = db.relationship('Show', backref='venue', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state.value,
            'address': self.address,
            'phone': self.phone,
            'genres': self.genres.split(','), 
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
        }
    
artist_shows = db.Table(
  'artist_shows',
  db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True),
  db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.Enum(StatesEnum), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))

    shows = db.relationship('Show', secondary=artist_shows, backref=db.backref('artists', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state.value,
            'phone': self.phone,
            'genres': self.genres.split(','), 
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
        }

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True) 
  name = db.Column(db.String)
  image_link = db.Column(db.String(500))
  date = db.Column(db.DateTime, server_default=db.func.now())

  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)