
# creating admin user and group on first run
# TODO: move this to controller
if db(db.auth_user).count() == 0:
    admin = auth.register_bare(first_name='System', last_name='administrator',
                               email='admin@admin.com', username='admin', password='admin')
    auth.add_group(GROUP_ADMIN)
    auth.add_membership(GROUP_ADMIN, admin)

