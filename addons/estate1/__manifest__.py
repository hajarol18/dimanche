{
    'name': "Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Name",
    'category': 'Category',
    'description': """
    Real Estate Advertisement Module
    """,
    'application': True,
   

   'data':[
       'security/ir.model.access.csv',
       'data/ir_model_data.xml',
       'views/estate_property_type_views.xml',
       'views/estate_property_tag_views.xml',
       'views/estate_property_offer_views.xml',
       'views/estate_property_views.xml',
       'views/res_users_views.xml',
       'views/estate_menus.xml',
   ]
}