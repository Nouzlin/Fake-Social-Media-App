__author__ = 'Linus'

import routes, database

if __name__ == '__main__':
    app = routes.app

    '''
    Add a group namned "test" -> O.K.
    Add an existing member to test -> O.K.
    '''
    database.create_new_group(app, "test", "none")
    database.add_group_members(app, "test", [0])

    '''
    Try add a group namned "illegal name" -> Syntax Error
    '''
    database.create_new_group(app, "illegal name", "vip")

    '''
    Try add a group namned "test" -> Integrity Error
    '''
    database.create_new_group(app, "test", "none")

    '''
    Add a group namned "test2" -> O.K.
    Add a non-existing member to test2 -> Error
    '''
    database.create_new_group(app, "test2", "none")
    database.add_group_members(app, "test2", [5])
