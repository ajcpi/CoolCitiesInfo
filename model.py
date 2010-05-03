import datetime
from google.appengine.ext import db
from google.appengine.api import users
class City(db.Model):
    name = db.StringProperty(required=True)
    mayor = db.StringProperty(required=False)
    city_contact_name = db.StringProperty(required=False)
    Title = db.StringProperty(required=False)
    phone_email = db.StringProperty(required=False)
    cool_city_contact = db.StringProperty(required=False)
    email = db.StringProperty(required=False)
    ghg_inventory = db.StringProperty(required=False)
    climate_action_plan = db.StringProperty(required=False)
    sustainability_plan = db.StringProperty(required=False)
    green_team = db.StringProperty(required=False)
    web_site = db.StringProperty(required=False)
    environmental_concerns_committee = db.StringProperty(required=False)
    green_ribbon_panel = db.StringProperty(required=False)
    Energy_efficiency = db.StringProperty(required=False, multiline=True)
    green_buildings = db.StringProperty(required=False)
    renewable = db.StringProperty(required=False)
    revolving_loan = db.StringProperty(required=False)
    biking_transportation = db.StringProperty(required=False)
    green_fleets = db.StringProperty(required=False)
    codes_policies_regulations = db.StringProperty(required=False)
    comments = db.StringProperty(required=False)
    more_comments = db.StringProperty(required=False)
    comed_challenge = db.StringProperty(required=False)

atList = [
('name', 'contact_info', 'City'),
('mayor', 'contact_info', 'Mayor'),
('city_contact_name', 'contact_info', 'City Contact'),
('Title', 'contact_info', 'Title'),
('phone_email', 'contact_info', 'Phone/Email'),
('cool_city_contact', 'contact_info', 'Cool Cities Contact'),
('email', 'contact_info', 'Email'),
('web_site', 'plan_info', "City's Green Initiative Website"),
('ghg_inventory', 'plan_info', 'Greenhouse Gas inventory'),
('climate_action_plan', 'plan_info', 'Climate Action Plan'),
('sustainability_plan', 'plan_info', 'Sustainability Plan'),
('green_team', 'plan_info', 'Green team'),
('environmental_concerns_committee', 'plan_info', 'Environmental Concerns Committee'),
('green_ribbon_panel', 'plan_info', 'Green Ribbon Panel'),
('Energy_efficiency', 'action_info', 'Energy Efficiency'),
('green_buildings', 'action_info', 'Green Builings'),
('renewable', 'action_info', 'Renewable'),
('revolving_loan', 'action_info', 'Revolving Loan'),
('biking_transportation', 'action_info', 'Biking/Transportaion'),
('green_fleets', 'action_info', 'Green Fleets'),
('codes_policies_regulations', 'action_info', 'Codes/Policies/Regulations'),
('comments', 'action_info', 'Comments'),
('more_comments', 'action_info', 'Comments'),
('comed_challenge', 'action_info', 'ComEd Challenge'),
]