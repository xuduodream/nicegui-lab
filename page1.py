from nicegui import app, ui


def logout():
    app.storage.user.clear()
    ui.navigate.to('/')
    ui.notify('Logged out', type='info')

def create_app_page():
    with ui.row().classes('w-full justify-end'):
        ui.button('Logout', on_click=logout)
    with ui.column().classes('mt-20 mx-auto items-center'):
        ui.label('Exclude SAST and DAST scanning').classes('text-2xl mb-4')
        exclusion_rm_package = ui.input('RM package to exclude').classes('w-96')
        ui.button('Submit', on_click=lambda: submit_exclusion(exclusion_rm_package.value))

def submit_exclusion(rm_package: str):
    if rm_package:
        ui.notify(f'RM package submitted: {rm_package}', type='positive')
    else:
        ui.notify('Please provide a RM package', type='negative')
