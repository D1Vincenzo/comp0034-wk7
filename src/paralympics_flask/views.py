from flask import current_app as app, render_template

from paralympics_flask import db
from paralympics_flask.models import Event
from paralympics_flask.figures import line_chart

# COMPLETED EXAMPLES OF WEEK 6 ACTIVITIES
# You can delete these once you've compared them to your work
@app.route('/html', methods=['GET'])
def index_html():
    """
    Returns a view using a basic HTML template with no CSS or Jinja.
    """
    return render_template('index_html.html')


@app.route('/css', methods=['GET'])
def index_css():
    """
    Returns a view using a basic HTML template with Bootstrap CSS.
    """
    return render_template('index_css.html')


@app.route('/responsive', methods=['GET'])
def index_responsive():
    """
    Returns a view using Bootstrap CSS and defines the viewport.
    """
    return render_template('templates/index_responsive.html')


@app.route('/jinja', methods=['GET'])
def index_jinja():
    """
    Returns a view using a child Jinja template with Bootstrap CSS.
    """
    return render_template('index_jinja.html')


# STARTER CODE FOR ACTIVITY 7
@app.route('/', methods=['GET'])
def index():
    """
    Returns the home page.

     Use as the starting point for week 7 activities.
    """
    events = db.session.execute(db.select(Event).order_by(Event.year)).scalars()
    return render_template('index.html', events=events)


@app.get('/events/<event_id>')
def get_event(event_id):
    event = db.get_or_404(Event, event_id)
    return render_template('events.html', event=event)

@app.get('/chart')
def display_chart():
    """ Returns a page with a line chart. """
    line_fig_html = line_chart(feature="participants", db=db)
    return render_template('chart.html', fig_html=line_fig_html)