from nicegui import app, ui
import page1


def login(username: str, password: str):
    if username == 'admin' and password == 'password':
        app.storage.user.update({'username': username, 'authenticated': True})
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
    # Check if the user is authenticated   
    if app.storage.user.get('authenticated', True):
        ui.notify(f'Hello {app.storage.user["username"]}', type='positive')
        page1.create_app_page()
    else:
        ui.notify('Please login first', type='warning')
        ui.navigate.to('/')

ui.run(title='Iceberg',storage_secret='THIS_NEEDS_TO_BE_CHANGED')
