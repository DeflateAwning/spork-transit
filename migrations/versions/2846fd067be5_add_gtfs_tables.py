"""Add GTFS tables

Revision ID: 2846fd067be5
Revises: 569934902f9d
Create Date: 2022-11-27 20:58:35.189433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2846fd067be5'
down_revision = '569934902f9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('download_hash_log',
    sa.Column('etag', sa.String(length=255), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('hash_md5', sa.String(length=255), nullable=False),
    sa.Column('content_length', sa.Integer(), nullable=False),
    sa.Column('source_name', sa.String(length=255), nullable=False),
    sa.Column('first_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('etag', 'url')
    )
    op.create_table('gtfs_calendar',
    sa.Column('service_id', sa.String(length=255), nullable=False),
    sa.Column('index', sa.Integer(), nullable=False),
    sa.Column('monday', sa.Boolean(), nullable=False),
    sa.Column('tuesday', sa.Boolean(), nullable=False),
    sa.Column('wednesday', sa.Boolean(), nullable=False),
    sa.Column('thursday', sa.Boolean(), nullable=False),
    sa.Column('friday', sa.Boolean(), nullable=False),
    sa.Column('saturday', sa.Boolean(), nullable=False),
    sa.Column('sunday', sa.Boolean(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('fetch_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('service_id')
    )
    op.create_table('gtfs_routes',
    sa.Column('route_id', sa.String(length=255), nullable=False),
    sa.Column('index', sa.Integer(), nullable=False),
    sa.Column('route_short_name', sa.Integer(), nullable=False),
    sa.Column('route_long_name', sa.String(length=255), nullable=False),
    sa.Column('route_desc', sa.String(length=255), nullable=True),
    sa.Column('route_type', sa.Integer(), nullable=False),
    sa.Column('route_url', sa.String(length=255), nullable=True),
    sa.Column('route_color', sa.String(length=255), nullable=True),
    sa.Column('route_text_color', sa.String(length=255), nullable=True),
    sa.Column('fetch_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('route_id')
    )
    op.create_table('gtfs_shapes',
    sa.Column('shape_id', sa.Integer(), nullable=False),
    sa.Column('shape_pt_sequence', sa.Integer(), nullable=False),
    sa.Column('index', sa.Integer(), nullable=False),
    sa.Column('shape_pt_lat', sa.Float(), nullable=False),
    sa.Column('shape_pt_lon', sa.Float(), nullable=False),
    sa.Column('shape_dist_traveled', sa.Float(), nullable=False),
    sa.Column('fetch_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('shape_id', 'shape_pt_sequence')
    )
    op.create_table('gtfs_stops',
    sa.Column('stop_id', sa.Integer(), nullable=False),
    sa.Column('stop_code', sa.Integer(), nullable=False),
    sa.Column('index', sa.Integer(), nullable=False),
    sa.Column('stop_name', sa.String(length=255), nullable=False),
    sa.Column('stop_desc', sa.String(length=255), nullable=True),
    sa.Column('stop_lat', sa.Float(), nullable=False),
    sa.Column('stop_lon', sa.Float(), nullable=False),
    sa.Column('zone_id', sa.Integer(), nullable=True),
    sa.Column('stop_url', sa.String(length=255), nullable=True),
    sa.Column('location_type', sa.Integer(), nullable=False),
    sa.Column('fetch_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('stop_id')
    )
    op.create_table('gtfsrt_alerts',
    sa.Column('alert_observed_uuid', sa.String(length=64), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fetch_time', sa.DateTime(), nullable=False),
    sa.Column('period_count', sa.Integer(), nullable=False),
    sa.Column('period_start', sa.DateTime(), nullable=False),
    sa.Column('period_end', sa.DateTime(), nullable=False),
    sa.Column('header_text', sa.String(length=255), nullable=True),
    sa.Column('description_text', sa.String(length=10000), nullable=True),
    sa.PrimaryKeyConstraint('alert_observed_uuid')
    )
    op.create_table('gtfs_calendar_dates',
    sa.Column('index', sa.Integer(), nullable=True),
    sa.Column('service_id', sa.String(length=255), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('exception_type', sa.Integer(), nullable=False),
    sa.Column('fetch_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['service_id'], ['gtfs_calendar.service_id'], ),
    sa.PrimaryKeyConstraint('service_id')
    )
    op.create_table('gtfs_trips',
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.Column('route_id', sa.String(length=255), nullable=False),
    sa.Column('service_id', sa.String(length=255), nullable=False),
    sa.Column('trip_headsign', sa.String(length=255), nullable=False),
    sa.Column('direction_id', sa.Integer(), nullable=False),
    sa.Column('block_id', sa.Integer(), nullable=False),
    sa.Column('shape_id', sa.Integer(), nullable=False),
    sa.Column('fetch_time', sa.DateTime(), nullable=False),
    sa.Column('index', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['route_id'], ['gtfs_routes.route_id'], ),
    sa.ForeignKeyConstraint(['service_id'], ['gtfs_calendar.service_id'], ),
    sa.ForeignKeyConstraint(['shape_id'], ['gtfs_shapes.shape_id'], ),
    sa.PrimaryKeyConstraint('trip_id')
    )
    op.create_table('gtfsrt_alerts_entities',
    sa.Column('alert_observed_uuid', sa.String(length=64), nullable=False),
    sa.Column('fetch_time', sa.DateTime(), nullable=False),
    sa.Column('route_short_name', sa.String(length=255), nullable=False),
    sa.Column('stop_id', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['alert_observed_uuid'], ['gtfsrt_alerts.alert_observed_uuid'], ),
    sa.ForeignKeyConstraint(['route_short_name'], ['gtfs_routes.route_short_name'], ),
    sa.ForeignKeyConstraint(['stop_id'], ['gtfs_stops.stop_id'], ),
    sa.PrimaryKeyConstraint('alert_observed_uuid', 'route_short_name', 'stop_id')
    )
    op.create_table('gtfs_stop_times',
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.Column('stop_id', sa.Integer(), nullable=False),
    sa.Column('stop_sequence', sa.Integer(), nullable=False),
    sa.Column('index', sa.Integer(), nullable=False),
    sa.Column('arrival_time', sa.Time(), nullable=False),
    sa.Column('departure_time', sa.Time(), nullable=False),
    sa.Column('pickup_type', sa.Integer(), nullable=False),
    sa.Column('drop_off_type', sa.Integer(), nullable=False),
    sa.Column('shape_dist_traveled', sa.Float(), nullable=False),
    sa.Column('timepoint', sa.Boolean(), nullable=False),
    sa.Column('fetch_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['stop_id'], ['gtfs_stops.stop_id'], ),
    sa.ForeignKeyConstraint(['trip_id'], ['gtfs_trips.trip_id'], ),
    sa.PrimaryKeyConstraint('trip_id', 'stop_sequence')
    )
    op.create_table('gtfsrt_positions',
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.Column('vehicle_id', sa.Integer(), nullable=False),
    sa.Column('fetch_time', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['trip_id'], ['gtfs_trips.trip_id'], ),
    sa.PrimaryKeyConstraint('trip_id', 'vehicle_id', 'fetch_time')
    )
    op.create_table('gtfsrt_updates',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('fetch_time', sa.DateTime(), nullable=False),
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.Column('route_short_name', sa.Integer(), nullable=False),
    sa.Column('stop_id', sa.Integer(), nullable=False),
    sa.Column('stop_seq', sa.Integer(), nullable=False),
    sa.Column('trip_schedule_rel', sa.String(length=255), nullable=False),
    sa.Column('stop_schedule_rel', sa.String(length=255), nullable=False),
    sa.Column('arrival_time', sa.DateTime(), nullable=True),
    sa.Column('departure_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['route_short_name'], ['gtfs_routes.route_short_name'], ),
    sa.ForeignKeyConstraint(['stop_id'], ['gtfs_stops.stop_id'], ),
    sa.ForeignKeyConstraint(['trip_id'], ['gtfs_trips.trip_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('gtfsrt_updates')
    op.drop_table('gtfsrt_positions')
    op.drop_table('gtfs_stop_times')
    op.drop_table('gtfsrt_alerts_entities')
    op.drop_table('gtfs_trips')
    op.drop_table('gtfs_calendar_dates')
    op.drop_table('gtfsrt_alerts')
    op.drop_table('gtfs_stops')
    op.drop_table('gtfs_shapes')
    op.drop_table('gtfs_routes')
    op.drop_table('gtfs_calendar')
    op.drop_table('download_hash_log')
    # ### end Alembic commands ###
