from nicegui import app, ui

def logout():
    try:
        app.storage.user.clear()
        ui.navigate.to('/')
        ui.notify('Logged out', type='info')
    except Exception as e:
        ui.notify(f'Error logging out: {str(e)}', type='negative')

def setup_ui_elements():
    with ui.row().classes('w-full justify-end'):
        ui.button('Logout', on_click=logout)
    with ui.column().classes('mt-20 mx-auto items-center'):
        ui.label('Exclude SAST and DAST scanning').classes('text-2xl mb-4')
        exclusion_rm_package = ui.input('RM package to exclude').classes('w-96')
        ui.button('Submit', on_click=lambda: submit_exclusion(exclusion_rm_package))

def submit_exclusion(exclusion_rm_package):
    try:
        if exclusion_rm_package.value:
            ui.notify(f'RM package submitted: {exclusion_rm_package.value}', type='positive')
            exclusion_rm_package.value = ''  # Clear the input field after submission
        else:
            ui.notify('Please provide a RM package', type='negative')
    except Exception as e:
        ui.notify(f'Error submitting RM package: {str(e)}', type='negative')

def create_app_page():
    setup_ui_elements()

# Call the create_app_page function to set up the UI
create_app_page()