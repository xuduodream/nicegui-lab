from nicegui import app, ui


def logout():
    try:
        app.storage.user.clear()
        ui.navigate.to('/')
        ui.notify('Logged out', type='info')
    except Exception as e:
        ui.notify(f'Error logging out: {str(e)}', type='negative')

def submit_exclusion(exclusion_rm_package):
    try:
        if exclusion_rm_package.value:
            ui.notify(f'RM package submitted: {exclusion_rm_package.value}', type='positive')
            exclusion_rm_package.value = ''  # Clear the input field after submission
        else:
            ui.notify('Please provide a RM package', type='negative')
    except Exception as e:
        ui.notify(f'Error submitting RM package: {str(e)}', type='negative')


def setup_ui_elements():
    with ui.header().classes(replace='row items-center justify-between') as header:       
        ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
        with ui.tabs() as tabs:
                    ui.tab('A')
                    ui.tab('B')
                    ui.tab('C')
        ui.button('Logout', on_click=logout).classes('mr-2')

    with ui.footer(value=False) as footer:
        ui.label('Footer')

    with ui.left_drawer().classes('bg-blue-100') as left_drawer:
        ui.label('Side menu')
        ui.button('Go to Panel B', on_click=lambda: tabs.set_value('B')).props('flat').classes('text-primary hover:text-primary-focus')
        
    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

    with ui.tab_panels(tabs, value='A').classes('w-full'):
        with ui.tab_panel('A'):
            ui.label('Exclude SAST and DAST scanning').classes('text-2xl mb-4')
            exclusion_rm_package = ui.input('RM package to exclude').classes('w-96')
            ui.button('Submit', on_click=lambda: submit_exclusion(exclusion_rm_package))
        with ui.tab_panel('B'):
            ui.label('Content of B')
        with ui.tab_panel('C'):
            ui.label('Content of C')



def create_app_page():
    setup_ui_elements()

# Call the create_app_page function to set up the UI
create_app_page()