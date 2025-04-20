from nicegui import ui
import page1

# Store the authentication state
authenticated = False

def login(username: str, password: str):
    global authenticated
    if username == 'admin' and password == 'password':
        authenticated = True
        ui.navigate.to('/app')
        ui.notify('Login Succeed', type='positive')
    else:
        ui.notify('Invalid credentials', type='negative')

def create_login_page():
    with ui.column().classes('mt-20 mx-auto items-center'):
        ui.label('Login').classes('text-2xl mb-4')
        username = ui.input('Username').classes('w-64')
        password = ui.input('Password', password=True, password_toggle_button=True).classes('w-64')
        ui.button('Login', on_click=lambda: login(username.value, password.value)).classes('mt-4')



@ui.page('/')
def login_page():
    create_login_page()

@ui.page('/app')
def app_page():
    global authenticated
    if authenticated:
        page1.create_app_page()
    else:
        ui.notify('Please login first', type='warning')
        ui.navigate.to('/')

ui.run(title='Iceberg')