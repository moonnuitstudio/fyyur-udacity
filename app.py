#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys
import json

from flask import (
  Flask, 
  render_template, 
  request, 
  Response, 
  flash, 
  redirect, 
  url_for, 
  session
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_wtf.csrf import CSRFProtect
from forms import *
from datetime import datetime

from models import db, Venue, Artist, Show
from helpers import format_datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app_context = app.app_context()
csrf = CSRFProtect()

db.init_app(app)
csrf.init_app(app)

migrate = Migrate(app, db)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues = Venue.query.order_by(Venue.city, Venue.state).all()
  
  #values = db.session.query(Show).join(Artist, Artist.id == Show.artist_id).join(Venue, Venue.id == Show.venue_id).filter(Artist.name.ilike(search_artist_term), Venue.name.ilike(search_venue_term)).all()
  
  venues_length = len( venues )
  
  areas = []
  _venues = []
  
  def save_area(city, state,):
    areas.append({
      'city': city,
      'state': state,
      'venues': _venues
    })
  
  for index in range(venues_length):
    venue = venues[index]
    
    num_upcoming_shows = len( list( filter( lambda x: x.start_time > datetime.today(), venue.shows ) ) )
    
    _venues.append({
      'id': venue.id,
      'name': venue.name,
      'num_upcoming_shows': num_upcoming_shows
    })
    
    if index < venues_length - 1:
      next_venue = venues[index + 1]
      
      if venue.city != next_venue.city or venue.state.value != next_venue.state.value:
        save_area(venue.city, venue.state.value)
        _venues = []
    else:
      save_area(venue.city, venue.state.value)
    
  return render_template('pages/venues.html', areas=areas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  search = "%{}%".format(search_term)
  venues = Venue.query.filter(Venue.name.ilike(search)).all()

  data = []

  for venue in venues:
    _venue = {
      'id': venue.id,
      'name': venue.name,
      'num_upcoming_shows': len( list( filter( lambda x: x.start_time > datetime.today(), venue.shows ) ) )
    }
      
    data.append(_venue) 
    
  response={
    "count": len(list(venues)),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  
  if venue is None:
    return render_template('errors/500.html')
  
  upcoming_shows = list( filter( lambda x: x.start_time > datetime.today(), venue.shows ) )
  past_shows = list( filter( lambda x: x.start_time < datetime.today(), venue.shows ) )
  
  upcoming_shows = list( map( lambda x: x.from_venue_page(), upcoming_shows) )
  past_shows = list( map( lambda x: x.from_venue_page(), past_shows) )
  
  data = venue.to_dict()
  data['upcoming_shows'] = upcoming_shows
  data['past_shows'] = past_shows
  data['upcoming_shows_count'] = len(upcoming_shows)
  data['past_shows_count'] = len(past_shows)
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    form = VenueForm(request.form)
    
    if form.validate():
      venue = Venue(
        name = form.name.data,
        city = form.city.data,
        state = form.state.data,
        genres = ','.join( request.form.getlist('genres') ),
        phone = form.phone.data,
        image_link = form.image_link.data,
        facebook_link = form.facebook_link.data,
        website_link = form.website_link.data,
        seeking_talent = 'seeking_talent' in request.form,
        seeking_description = form.seeking_description.data,
      )
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + venue.name + ' was successfully listed!')
    else:
      return render_template('forms/new_venue.html', form=form, erros=form.errors)
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form["name"] + ' could not be listed.')
  finally:
    db.session.close()
  
  return render_template('pages/home.html')
  

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  
  deleted_state = True
  
  try:
    vanue = Venue.query.get(venue_id)
    name = vanue.name
    
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Venue ' + name + ' was successfully deleted!')
  except:
    db.session.rollback()
    print( sys.exc_info() )
    deleted_state = False
  finally:
    db.session.close()
  print("state", deleted_state)
  return { "state": deleted_state }

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.all()
  data = []
  
  for artist in artists:
    data.append({
      'id': artist.id,
      'name': artist.name,
      'num_upcoming_shows': len( list( filter( lambda x: x.start_time > datetime.today(), artist.shows ) ) )
    })
    
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  search = "%{}%".format(search_term)
  
  artists = Artist.query.filter(Artist.name.ilike(search)).all()
  data = []
  
  for artist in artists:
    data.append({
      'id': artist.id,
      'name': artist.name,
      'num_upcoming_shows': len( list( filter( lambda x: x.start_time > datetime.today(), artist.shows ) ) )
    })
  
  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  
  artist = Artist.query.get(artist_id)
  
  if artist is None:
    return render_template('errors/500.html')
  
  upcoming_shows = list( filter( lambda x: x.start_time > datetime.today(), artist.shows ) )
  past_shows = list( filter( lambda x: x.start_time < datetime.today(), artist.shows ) )
  
  upcoming_shows = list( map( lambda x: x.from_artist_page(), upcoming_shows) )
  past_shows = list( map( lambda x: x.from_artist_page(), past_shows) )
  
  data = artist.to_dict()
  data['upcoming_shows'] = upcoming_shows
  data['past_shows'] = past_shows
  data['upcoming_shows_count'] = len(upcoming_shows)
  data['past_shows_count'] = len(past_shows)
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  artist = Artist.query.get(artist_id)
  
  if artist is None:
    return render_template('errors/500.html')
  
  form = ArtistForm(
    name = artist.name,
    city = artist.city,
    state = artist.state.value,
    genres = artist.genres,
    phone = artist.phone,
    image_link = artist.image_link,
    facebook_link = artist.facebook_link,
    website_link = artist.website_link,
    seeking_venue = "Y" if artist.seeking_venue else "",
    seeking_description = artist.seeking_description,
  )
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  has_error = False
  has_form_error = False
  
  form = ArtistForm(request.form)
  
  try:
    if form.validate():
      artist = Artist.query.get(artist_id)
  
      if artist is None:
        raise Exception('Error artist not found')
      
      print("artist", artist)
      
      artist.name = form.name.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.genres = ','.join( request.form.getlist('genres') )
      artist.phone = form.phone.data
      artist.image_link = form.image_link.data
      artist.facebook_link = form.facebook_link.data
      artist.website_link = form.website_link.data
      artist.seeking_venue = 'seeking_venue' in request.form
      artist.seeking_description = form.seeking_description.data
      
      db.session.commit()
    else:
      has_form_error = True
  except:
    db.session.rollback()
    print( sys.exc_info() )
    has_error = True
  finally:
    db.session.close()
  
  if has_form_error:
    return render_template('forms/edit_artist.html', form=form, erros=form.errors)
  elif has_error:
    flash('An error occurred. Artist ' + request.form["name"] + ' could not be updated.')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  
  if venue is None:
    return render_template('errors/500.html')
  
  form = VenueForm(
    name=venue.name,
    city = venue.city,
    state = venue.state.value,
    address = venue.address,
    genres = venue.genres,
    phone = venue.phone,
    image_link = venue.image_link,
    facebook_link = venue.facebook_link,
    website_link = venue.website_link,
    seeking_talent = "Y" if venue.seeking_talent else "",
    seeking_description = venue.seeking_description,
  )
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  has_error = False
  has_form_error = False
  
  form = VenueForm(request.form)
  
  try:
    if form.validate():
      venue = Venue.query.get(venue_id)
  
      if venue is None:
        raise Exception('Error venue not found')
      
      venue.name = request.form["name"]
      venue.city = request.form["city"]
      venue.state = request.form["state"]
      venue.address = request.form["address"]
      venue.genres = ','.join( request.form.getlist('genres') )
      venue.phone = request.form["phone"]
      venue.image_link = request.form["image_link"]
      venue.facebook_link = request.form["facebook_link"]
      venue.website_link = request.form["website_link"]
      venue.seeking_talent = 'seeking_talent' in request.form
      venue.seeking_description = request.form["seeking_description"]
      
      db.session.commit()
    else:
      has_form_error = True
  except:
    db.session.rollback()
    print( sys.exc_info() )
    has_error = True
  finally:
    db.session.close()
  
  if has_form_error:
    return render_template('forms/edit_venue.html', form=form, erros=form.errors)
  elif has_error:
    flash('An error occurred. Venue ' + request.form["name"] + ' could not be listed.')
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    form = ArtistForm(request.form)
    has_error = False
    has_error_form = False
    
    if form.validate():
      artist = Artist(
        name = form.name.data,
        city = form.city.data,
        state = form.state.data,
        genres = ','.join( request.form.getlist('genres') ),
        phone = form.phone.data,
        image_link = form.image_link.data,
        facebook_link = form.facebook_link.data,
        website_link = form.website_link.data,
        seeking_venue = 'seeking_venue' in request.form,
        seeking_description = form.seeking_description.data,
      )
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + artist.name + ' was successfully listed!')
    else:
      has_error_form = True
  except:
    db.session.rollback()
    has_error = True
  finally:
    db.session.close()
  
  if has_error:
    flash('An error occurred. Artist ' + request.form["name"] + ' could not be listed.')
  elif has_error_form:
    return render_template('forms/new_venue.html', form=form, erros=form.errors)
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows/search', methods=['POST'])
def search_shows():
  artist_term = request.form.get('artist_term', '')
  venue_term = request.form.get('venue_term', '')
  
  search_artist_term = "%{}%".format(artist_term)
  search_venue_term = "%{}%".format(venue_term)
  
  #shows = Show.query.filter().all()
  shows = db.session.query(Show).join(Artist, Artist.id == Show.artist_id).join(Venue, Venue.id == Show.venue_id).filter(Artist.name.ilike(search_artist_term), Venue.name.ilike(search_venue_term)).all()

  
  data = []
  
  for show in shows:
    venue = show.venue
    artist = show.artist
    
    data.append({
      "venue_id": venue.id,
      "venue_name": venue.name,
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M')
    })

  return render_template('pages/shows.html', shows=data, artist_term=artist_term, venue_term=venue_term)

@app.route('/shows')
def shows():
  shows = Show.query.all()
  data = []
  
  for show in shows:
    venue = show.venue
    artist = show.artist
    
    data.append({
      "venue_id": venue.id,
      "venue_name": venue.name,
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M')
    })
  
  return render_template('pages/shows.html', shows=data)
# OK------
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  has_error = False
  has_form_error = False
  
  form = ShowForm(request.form, meta={"csrf": False})
  
  try:
    if form.validate():
      venue_id = form.venue_id.data
      artist_id = form.artist_id.data
      
      venue = Venue.query.get(venue_id)
  
      if venue is None:
        raise Exception('Error venue not found')
      
      artist = Artist.query.get(artist_id)
      
      if artist is None:
        raise Exception('Error artist not found')
      
      show = Show(
        venue_id = venue_id,
        artist_id = artist_id,
        start_time = form.start_time.data
      )
      
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
    else:
      has_form_error = True
  except:
    db.session.rollback()
    print( sys.exc_info() )
    has_error = True
  finally:
    db.session.close()
  
  if has_form_error:
    return render_template('forms/new_show.html', form=form, erros=form.errors)
  elif has_error:
    flash('An error occurred. The show could not be listed.')
  
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
