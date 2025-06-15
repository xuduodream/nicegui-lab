from nicegui import app, ui


# State management for menu groups
menu_states = {
    "database_tools": True,
    "administration": False
}


def logout():
    try:
        app.storage.user.clear()
        ui.navigate.to('/')
        ui.notify('Logged out', type='info')
    except Exception as e:
        ui.notify(f'Error logging out: {str(e)}', type='negative')


def create_mongodb_restore():
    """Create the MongoDB restore application UI"""
    with ui.column().classes('w-full gap-4'):
        ui.label('MongoDB Archive Restorer').classes('text-2xl font-bold')
        
        # Archive selection
        with ui.row().classes('w-full items-center'):
            ui.label('Select Archive:').classes('w-48')
            archive = ui.input().classes('flex-grow')
            ui.button('Browse...', on_click=lambda: ui.notify('Browse functionality would go here'))
        
        # Destination database
        with ui.row().classes('w-full items-center'):
            ui.label('Destination Database:').classes('w-48')
            db_name = ui.input().classes('flex-grow')
        
        # Collections to restore
        with ui.row().classes('w-full items-start'):
            ui.label('Collections:').classes('w-48')
            collections = ui.textarea(placeholder='Enter collection names, one per line').classes('flex-grow h-40')
        
        # Action buttons
        with ui.row().classes('w-full justify-end gap-4 mt-4'):
            ui.button('Clear', on_click=lambda: [
                archive.set_value(''),
                db_name.set_value(''),
                collections.set_value('')
            ])
            ui.button('Restore', on_click=lambda: ui.notify(f'Restoring {archive.value} to {db_name.value}')).props('color=primary')



def toggle_menu_group(group_name):
    """Toggle the visibility of a menu group"""
    menu_states[group_name] = not menu_states[group_name]
    # Update the icon based on state
    if group_name == "database_tools":
        db_toggle_icon.set_name('expand_less' if menu_states[group_name] else 'expand_more')
    elif group_name == "administration":
        admin_toggle_icon.set_name('expand_less' if menu_states[group_name] else 'expand_more')

def create_menu_button(text, icon, handler):
    """Create a styled menu button"""
    return ui.button(text, icon=icon, on_click=handler) \
        .props('flat') \
        .classes('''
            text-gray-700 hover:text-blue-600 
            hover:bg-blue-50 justify-start w-full
            text-left p-2 transition-colors rounded
            ml-2
        ''')





def create_app_page():
    def change_content(content_func):
        """Change the content area to display different applications"""
        content.clear()
        with content:
            content_func()

    # Custom CSS for menu styling
    ui.add_head_html('''
    <style>
        .menu-group {
            transition: all 0.3s ease;
            overflow: hidden;
        }
        .menu-header {
            cursor: pointer;
            user-select: none;
            padding: 8px 12px;
            border-radius: 6px;
            transition: background-color 0.2s;
        }
        .menu-header:hover {
            background-color: #f3f4f6;
        }
    </style>
    ''')

    with ui.header().classes('justify-between items-center'):
        ui.label('Webtool Manager').style('color: white;').classes('text-xl font-bold text-gray-800')
        ui.button('Logout', icon='logout', on_click=logout).props('flat').style('background-color: white; color: white;').classes('text-gray-600 hover:text-blue-600')

    with ui.row().classes('w-full h-[calc(100vh-130px)]'):
        # Sidebar Menu
        with ui.column().classes('bg-gray-50 w-64 h-full p-4 gap-1 border-r'):
            # Dashboard (top-level menu item)
            create_menu_button('Dashboard', 'dashboard', 
                            lambda: change_content(lambda: ui.label('Dashboard Content').classes('text-xl')))
            
            ui.separator().classes('my-2')
            
            # Database Tools Group  
            with ui.column().classes('w-full'):
                # Group header
                with ui.row().classes('w-full items-center menu-header') \
                    .on('click', lambda: toggle_menu_group('database_tools')):
                    ui.icon('folder').classes('text-blue-500')
                    ui.label('Database Tools').classes('ml-2 font-medium text-gray-700 flex-grow')
                    global db_toggle_icon
                    db_toggle_icon = ui.icon('expand_less' if menu_states['database_tools'] else 'expand_more') \
                        .classes('text-gray-500')
                
                # Group content (collapsible)
                with ui.column().classes('menu-group pl-2 mt-1') \
                    .bind_visibility_from(menu_states, 'database_tools'):
                    create_menu_button('MongoDB Restore', 'restore', 
                                    lambda: change_content(create_mongodb_restore))
                    create_menu_button('Data Migrator', 'sync', 
                                    lambda: change_content(lambda: ui.label('Data Migration Content')))
                    create_menu_button('Backup Manager', 'backup', 
                                    lambda: change_content(lambda: ui.label('Backup Manager Content')))
            
            # # Administration Group (collapsed by default)
            # with ui.column().classes('w-full mt-4'):
            #     # Group header
            #     with ui.row().classes('w-full items-center menu-header') \
            #         .on('click', lambda: toggle_menu_group('administration')):
            #         ui.icon('admin_panel_settings').classes('text-green-500')
            #         ui.label('Administration').classes('ml-2 font-medium text-gray-700 flex-grow')
            #         global admin_toggle_icon
            #         admin_toggle_icon = ui.icon('expand_more' if not menu_states['administration'] else 'expand_less') \
            #             .classes('text-gray-500')
                
            #     # Group content (collapsible)
            #     with ui.column().classes('menu-group pl-2 mt-1') \
            #         .bind_visibility_from(menu_states, 'administration'):
            #         create_menu_button('User Admin', 'people', 
            #                            lambda: change_content(lambda: ui.label('User Admin Content')))
            #         create_menu_button('Audit Logs', 'history', 
            #                            lambda: change_content(lambda: ui.label('Audit Logs Content')))
            #         create_menu_button('Settings', 'settings', 
            #                            lambda: change_content(lambda: ui.label('Settings Content')))
            
            # Additional top-level items
            ui.separator().classes('my-2')
            create_menu_button('Documentation', 'help', 
                            lambda: change_content(lambda: ui.label('Documentation Content')))
            # create_menu_button('Support', 'support_agent', 
            #                    lambda: change_content(lambda: ui.label('Support Content')))
        
        # Content Area
        content = ui.column().classes('flex-grow p-8 bg-white')
        with content:
            ui.label('Welcome to Webtool Manager').classes('text-2xl font-bold text-gray-800')
            ui.markdown('''
                **Select an option from the menu to begin**
                
                - Use **Database Tools** for MongoDB operations
                - Access **Administration** for system settings
            ''').classes('mt-4 text-lg')

    # Footer
    with ui.footer().classes('justify-center py-4 bg-gray-50 border-t'):
        ui.label('2025 Webtool Manager v2.0').classes('text-gray-600')
