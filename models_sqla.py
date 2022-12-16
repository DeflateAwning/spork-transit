#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 19:55:04 2021

@author: Hrishikesh Terdalkar
"""

###############################################################################

from sqlalchemy import (Column, Integer, String, Boolean, DateTime, Date, JSON, ForeignKey, Float, Time)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList

from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore, AsaList
from flask_security.forms import LoginForm, RegisterForm, StringField, Required

###############################################################################
# Create database connection object

db = SQLAlchemy()

###############################################################################
# User Database Models

DEFAULT_SETTING = {
	'display_name': '',
	'theme': 'united',
}


class Role(db.Model, RoleMixin):
	id = Column(Integer, primary_key=True)
	name = Column(String(255), unique=True)
	description = Column(String(255))
	level = Column(Integer)
	permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)


class User(db.Model, UserMixin):
	id = Column(Integer, primary_key=True)
	username = Column(String(255), unique=True)
	email = Column(String(255), unique=True)
	password = Column(String(255))
	active = Column(Boolean, default=True)
	fs_uniquifier = Column(String(255), unique=True)
	confirmed_at = Column(DateTime)
	settings = Column(JSON, default=DEFAULT_SETTING)
	last_login_at = Column(DateTime)
	current_login_at = Column(DateTime)
	last_login_ip = Column(String(255))
	current_login_ip = Column(String(255))
	login_count = Column(Integer)
	roles = relationship('Role', secondary='roles_users',
						 backref=backref('users', lazy='dynamic'))


class RolesUsers(db.Model):
	__tablename__ = 'roles_users'
	id = Column(Integer, primary_key=True)
	user_id = Column('user_id', Integer, ForeignKey('user.id'))
	role_id = Column('role_id', Integer, ForeignKey('role.id'))



###############################################################################
# Transit Database Models

# could have considered:
# https://github.com/OpenTransitTools/gtfsdb/blob/master/gtfsdb/model/trip.py
# https://gist.github.com/mdellavo/2159074

class DownloadHashLog(db.Model):
	__tablename__ = 'download_hash_log'
	etag = Column('etag', String(255), primary_key=True)
	url = Column('url', String(255), primary_key=True)
	hash_md5 = Column('hash_md5', String(255), nullable=False)
	content_length = Column('content_length', Integer, nullable=False)
	source_name = Column('source_name', String(255), nullable=False)
	first_time = Column('first_time', DateTime, nullable=False)

class GTFSCalendar(db.Model):
	__tablename__ = 'gtfs_calendar'
	service_id = Column('service_id', String(255), primary_key=True, nullable=False)
	index = Column('index', Integer, nullable=False)
	monday = Column('monday', Boolean, nullable=False)
	tuesday = Column('tuesday', Boolean, nullable=False)
	wednesday = Column('wednesday', Boolean, nullable=False)
	thursday = Column('thursday', Boolean, nullable=False)
	friday = Column('friday', Boolean, nullable=False)
	saturday = Column('saturday', Boolean, nullable=False)
	sunday = Column('sunday', Boolean, nullable=False)
	start_date = Column('start_date', Date, nullable=False)
	end_date = Column('end_date', Date, nullable=False)
	fetch_time = Column('fetch_time', DateTime, nullable=False)

class GTFSCalendarDates(db.Model):
	__tablename__ = 'gtfs_calendar_dates'
	index = Column('index', Integer)
	service_id = Column('service_id', String(255), ForeignKey('gtfs_calendar.service_id'), primary_key=True, nullable=False)
	date = Column('date', Date, nullable=False)
	exception_type = Column('exception_type', Integer, nullable=False) # TODO change this to an enum or something
	fetch_time = Column('fetch_time', DateTime, nullable=False)

class GTFSRoutes(db.Model):
	__tablename__ = 'gtfs_routes'
	route_id = Column('route_id', String(255), primary_key=True, nullable=False)
	index = Column('index', Integer, nullable=False)
	route_short_name = Column('route_short_name', Integer, nullable=False)
	route_long_name = Column('route_long_name', String(255), nullable=False)
	route_desc = Column('route_desc', String(255))
	route_type = Column('route_type', Integer, nullable=False) # TODO change this to an enum or something
	route_url = Column('route_url', String(255))
	route_color = Column('route_color', String(255))
	route_text_color = Column('route_text_color', String(255))
	fetch_time = Column('fetch_time', DateTime, nullable=False)

class GTFSShapes(db.Model):
	__tablename__ = 'gtfs_shapes'
	shape_id = Column('shape_id', Integer, primary_key=True, nullable=False)
	shape_pt_sequence = Column('shape_pt_sequence', Integer, primary_key=True, nullable=False)
	index = Column('index', Integer, nullable=False)
	shape_pt_lat = Column('shape_pt_lat', Float, nullable=False)
	shape_pt_lon = Column('shape_pt_lon', Float, nullable=False)
	shape_dist_traveled = Column('shape_dist_traveled', Float, nullable=False)
	fetch_time = Column('fetch_time', DateTime, nullable=False)


class GTFSStopTimes(db.Model):
	__tablename__ = 'gtfs_stop_times'
	trip_id = Column('trip_id', Integer, ForeignKey('gtfs_trips.trip_id'), primary_key=True, nullable=False)
	stop_id = Column('stop_id', Integer, ForeignKey('gtfs_stops.stop_id'), nullable=False)
	stop_sequence = Column('stop_sequence', Integer, primary_key=True, nullable=False)
	index = Column('index', Integer, nullable=False)
	arrival_time = Column('arrival_time', Time, nullable=False)
	departure_time = Column('departure_time', Time, nullable=False)
	
	pickup_type = Column('pickup_type', Integer, nullable=False) # TODO enum
	drop_off_type = Column('drop_off_type', Integer, nullable=False) # TODO enum
	shape_dist_traveled = Column('shape_dist_traveled', Float, nullable=False)
	timepoint = Column('timepoint', Boolean, nullable=False)
	fetch_time = Column('fetch_time', DateTime, nullable=False)
	
class GTFSStops(db.Model):
	__tablename__ = 'gtfs_stops'
	stop_id = Column('stop_id', Integer, primary_key=True, nullable=False)
	stop_code = Column('stop_code', Integer, nullable=False)
	index = Column('index', Integer, nullable=False)
	stop_name = Column('stop_name', String(255), nullable=False)
	stop_desc = Column('stop_desc', String(255), nullable=True)
	stop_lat = Column('stop_lat', Float, nullable=False)
	stop_lon = Column('stop_lon', Float, nullable=False)
	zone_id = Column('zone_id', Integer)
	stop_url = Column('stop_url', String(255))
	location_type = Column('location_type', Integer, nullable=False)
	fetch_time = Column('fetch_time', DateTime, nullable=False)
	
class GTFSTrips(db.Model):
	__tablename__ = 'gtfs_trips'
	trip_id = Column('trip_id', Integer, primary_key=True, nullable=False)
	route_id = Column('route_id', String(255), ForeignKey('gtfs_routes.route_id'), nullable=False)
	service_id = Column('service_id', String(255), ForeignKey('gtfs_calendar.service_id'), nullable=False)
	trip_headsign = Column('trip_headsign', String(255), nullable=False)
	direction_id = Column('direction_id', Integer, nullable=False)
	block_id = Column('block_id', Integer, nullable=False)
	shape_id = Column('shape_id', Integer, ForeignKey('gtfs_shapes.shape_id'), nullable=False)
	fetch_time = Column('fetch_time', DateTime, nullable=False)
	index = Column('index', Integer, nullable=False)

class GTFSRTAlerts(db.Model):
	__tablename__ = 'gtfsrt_alerts'
	alert_observed_uuid = Column('alert_observed_uuid', String(64), primary_key=True, nullable=False)
	id = Column('id', Integer, nullable=False)
	fetch_time = Column('fetch_time', DateTime, nullable=False)
	period_count = Column('period_count', Integer, nullable=False)
	period_start = Column('period_start', DateTime, nullable=False)
	period_end = Column('period_end', DateTime, nullable=False)
	header_text = Column('header_text', String(255))
	description_text = Column('description_text', String(10000))

class GTFSRTAlertsEntities(db.Model):
	__tablename__ = 'gtfsrt_alerts_entities'
	alert_observed_uuid = Column('alert_observed_uuid', String(64), ForeignKey('gtfsrt_alerts.alert_observed_uuid'), primary_key=True, nullable=False)
	fetch_time = Column('fetch_time', DateTime, nullable=False)
	route_short_name = Column('route_short_name', String(255), ForeignKey('gtfs_routes.route_short_name'), primary_key=True, nullable=False)
	stop_id = Column('stop_id', String(255), ForeignKey('gtfs_stops.stop_id'), primary_key=True, nullable=False)
	
class GTFSRTPositions(db.Model):
	__tablename__ = 'gtfsrt_positions'
	trip_id = Column('trip_id', Integer, ForeignKey('gtfs_trips.trip_id'), primary_key=True, nullable=False)
	vehicle_id = Column('vehicle_id', Integer, primary_key=True, nullable=False)
	fetch_time = Column('fetch_time', DateTime, primary_key=True, nullable=False)
	id = Column('id', Integer, nullable=False)
	timestamp = Column('timestamp', DateTime, nullable=False)
	latitude = Column('latitude', Float, nullable=False)
	longitude = Column('longitude', Float, nullable=False)

class GTFSRTUpdates(db.Model):
	__tablename__ = 'gtfsrt_updates'
	# update is for a specific trip (with a route) at a specific stop; sometimes there are up to 2 updates for a trip-route-stop
	
	id = Column('id', String(64), primary_key=True, nullable=False)
	
	fetch_time = Column('fetch_time', DateTime, nullable=False)
	trip_id = Column('trip_id', Integer, ForeignKey('gtfs_trips.trip_id'), nullable=False)
	route_short_name = Column('route_short_name', Integer, ForeignKey('gtfs_routes.route_short_name'), nullable=False)
	stop_id = Column('stop_id', Integer, ForeignKey('gtfs_stops.stop_id'), nullable=False)
	stop_seq = Column('stop_seq', Integer, nullable=False)

	trip_schedule_rel = Column('trip_schedule_rel', String(255), nullable=False)
	stop_schedule_rel = Column('stop_schedule_rel', String(255), nullable=False)
	
	arrival_time = Column('arrival_time', DateTime)
	departure_time = Column('departure_time', DateTime)


###############################################################################
# Setup Flask-Security

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

###############################################################################


class CustomRegisterForm(RegisterForm):
	username = StringField('Username', [Required()])

	def validate(self):
		if user_datastore.find_user(username=self.username.data):
			self.username.errors = ["Username already taken"]
			return False

		if not super(CustomRegisterForm, self).validate():
			return False

		return True


class CustomLoginForm(LoginForm):
	email = StringField('Username or Email', [Required()])

###############################################################################
