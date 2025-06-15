from nicegui import app, ui
import app.webtool as webtool


############ Functions for login and app page creation ############
def login(username: str, password: str):
    try:
        if username == 'admin' and password == 'password':
            app.storage.user.update({'username': username, 'authenticated': True})
            ui.navigate.to('/app')
            ui.notify('Login Succeed', type='positive')
        else:
            ui.notify('Invalid credentials', type='negative')
    except Exception as e:
        ui.notify(f'An error occurred: {str(e)}', type='negative')

def create_login_page():
    with ui.column().classes('mt-20 mx-auto items-center'):
        ui.label('Webtool Manager').classes('text-2xl mb-4')
        username = ui.input('Username').classes('w-64')
        password = ui.input('Password', password=True, password_toggle_button=True).classes('w-64')
        ui.button('Login', on_click=lambda: login(username.value, password.value)).classes('mt-4')



############ UI Pages ############
@ui.page('/')
def login_page():
    create_login_page()


@ui.page('/app')
def app_page():
    try:
        if app.storage.user.get('authenticated', False):
            ui.notify(f'Hello {app.storage.user["username"]}', type='positive')
            webtool.create_app_page()
        else:
            ui.notify('Please login first', type='warning')
            ui.navigate.to('/')
    except Exception as e:
        ui.notify(f'An error occurred: {str(e)}', type='negative')



############# Main Execution ############
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Webtool Manager', favicon='⚙️', storage_secret='THIS_NEEDS_TO_BE_CHANGED')
