from config import create_app

from models import User,db
from werkzeug.security import generate_password_hash
app=create_app()


# command line authentication 
import click

# @app.cli.command("create-admin")
# @click.argument("name")
# def create_user(name):
#     click.echo(f"name:{name}")
@app.cli.command("create-admin")
@click.option('--username', prompt='Enter username', help='Username for the admin account.')
@click.option('--email', prompt='Enter email',
              help='email for the admin account.')
@click.option('--password', prompt='Enter password',
              help='password for the admin account.')
@click.option('--confirmed_password', prompt='Enter confirmed_password',
              help='confirmed_password for the admin account.')
def create_admin(username, email,password,confirmed_password):
    """Simple program that greets NAME for a total of COUNT times."""
    # print(username)
    with app.app_context():
        if((username!='') and (email!='') and (password!='') and (confirmed_password!='')):
            user=User.query.filter_by(email=email).first()
            if (user==None):
                    if(password ==confirmed_password):
                        
                            user=User(username=username,email=email,password=generate_password_hash(password ),is_admin=True)
                            db.session.add(user)
                            db.session.commit()
                            click.echo('account created successfully.')
                            
                    else:
                        click.echo('password and confirmed password is miss matching.')
                        
                    
            else:
                    click.echo('email address is already signup.')
                    
                    
                    
        else:
            click.echo('please fill all the fields.')
            
        





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
