from app.blueprints import student_mod
from flask import url_for, request, session, current_app, redirect, g, render_template, request
from sqlalchemy import or_, desc
from app.models.opportunities import Opportunity
from app.models.tag import Tag
from app.core.authentication import require_login, require_role
import logging
import json

LOG = logging.getLogger(__name__)

@student_mod.route('/')
@require_login
@require_role('student')
def index():
    """ Student dashboard """
    if 'id' in session and 'token' in session:
        return redirect(url_for("student.controller.opportunities"))
    return render_template("welcome.html")

@student_mod.route('/update_following/<int:id>/<int:to_change>', methods=['POST'])
@require_login
@require_role('student')
def update_following(id = 0, to_change = 0):
    """ Updates whether a user is following a specific opportunity

    :param id: ID of the opportunity to change
    :type id: int
    :param to_change: 1 if adding, 0 if removing
    :type to_change: int
    :returns: 'Success' if success 'Error' if error
    """

    opportunity = Opportunity.query.filter_by(id = id)

    LOG.debug('%d, %d' % id, to_change)

    if to_change:
        if not opportunity in g.users.opportunities_following:
            g.user.opportunities_following.append(opportunity)
            LOG.debug('Added ' + str(g.user) + ' to the following list of ' + str(opportunity))
            return 'Success'
        else:
            return 'Error'
    else:
        if opportunity in g.users.opportunities_following:
            g.users.opportunities_following.remove(opportunity)
            LOG.debug('Removed ' + str(g.user) + ' from the following list of ' + str(opportunity))
            return 'Success'
        else:
            return 'Error'
    return 'Error'

@student_mod.route('/opportunities')
@student_mod.route('/opportunities/<int:page>')
@require_login
@require_role('student')
def opportunities(page = 1):
    """ Returns all opportunities for a student (paginated) seperated by either tag, but sorted in the recommendation order (see neural net fun times)

    :param page: Page to return
    :type page: int
    """

    if request.method == 'POST':
        if (request.form.getlist('starbox')):
            for i in request.form.getlist('starbox'):
                i.users_following.append(g.user)

        db.session.commit()

    #for i in Opportunity.query.all():
    #    print i.tags

    tags = ["Technology", "Theater", "Volunteering", "Volunteering", "Research"]

    search_field = "" #session['search'] if 'search' in session else ''
    opportunities = Opportunity.query.order_by("name").filter(
        or_(Opportunity.name.like('%' + search_field + '%'),
            Opportunity.description.like('%' + search_field + '%'),
            Opportunity.organization.like('%' + search_field + '%')
        )).paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)

    # Implement the whole suggestion thing
    #opportunities = Opportunity.query.paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)

    return render_template("student/student_opportunities.html", opportunities = opportunities, search_field = search_field, tags = tags)

@student_mod.route('/my_opportunities/<int:page>')
@require_login
@require_role('student')
def my_opportunities(page = 1): ##UNNECESSARY?
    """ Returns all opportunities that a user has suggesterd

    :param page: Page to return
    :type page: int
    """

    # Implement this in the database first

    return 'student.controller.my_opportunities'

@student_mod.route('/starred_opportunities/<int:page>')
@require_login
@require_role('student')
def starred_opportunities(page = 1):
    """ Returns all the opportunities that a user is specifically following

    Two sections:
     - Opportunities that the user specifically followed
     - Opportunities in the tags selected by the user (is this necessary?)

    :param page: Page to return
    :type page: int
    """

    opportunities = Opportunity.query.paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)

    #opportunities = g.opportunities_following.paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)

    return render_template("student/starred_opportunities.html", opportunities = opportunities)

@student_mod.route('/opportunity/<int:op_id>')
@require_login
@require_role('student')
def opportunity(op_id = 0):
    """ Returns a single opportunity to display information

    :param op_id: ID of the opportunity to display information of
    :type op_id: int
    """

    opportunity = Opportunity.query.filter_by(id = op_id).first()
    print "\n" * 10
    print opportunity
    print "\n" * 10
    return render_template("student/student_opportunity.html", opportunity = opportunity)

@student_mod.route('/search')
@student_mod.route('/search/<int:page>')
@require_login
@require_role('student')
def search(page = 1):
    """ Returns a paginated list of opportunities as pursuant to the search parameters given by the GET parameters

    The paramaters should be:
     - search (str) the string to search for
     - tags (str) the tags (as a comma seperated list) to search for

    :param page: Page to return
    :type page: int
    """

    search_field = request.args.get('search') if 'search' in request.args else ''
    tags = request.args.get('tags') if 'tags' in request.args else ''

    LOG.debug('Search Field: ' + search_field)
    LOG.debug('Tags: ' + tags)

    opportunities = Opportunity.query.filter(
        or_(Opportunity.name.like('%' + search_field + '%'),
            Opportunity.description.like('%' + search_field + '%'),
            Opportunity.organization.like('%' + search_field + '%')
        )).paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)

    session['search'] = search_field

    return render_template("student/student_opportunities.html", opportunities = opportunities, search_field = search_field)


@student_mod.route('/sort-opportunities')
@require_login
@require_role('student')
def sort_opportunities(page = 1):
    sort_by = request.args.get("sort_by")
    if sort_by == "alphabetical":
        opportunities = Opportunity.query.order_by("name").paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)
    elif sort_by == "reverse_alphabetical":
        opportunities = Opportunity.query.order_by(desc("name")).paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)
    elif sort_by == "deadline":
        opportunities = Opportunity.query.order_by("deadline").paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)
    elif sort_by == "reverse_deadline":
        opportunities = Opportunity.query.order_by("hours").paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)
    else: #Do alphabetical if sort_by is unrecognized
        opportunities = Opportunity.query.order_by("name").paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)
    return render_template("student/student_opportunities.html", opportunities = opportunities)
