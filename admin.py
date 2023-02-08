from flask_admin import Admin
from models import MyModelView,User,db,MyAdminModelView,Contact

admin=Admin(index_view=MyAdminModelView(
                    name='Home',
                    template='admin/myhome.html',
                    url='/admin'))

admin.add_view(MyModelView(User,db.session))
admin.add_view(MyModelView(Contact,db.session))