class MovementRouter:
    """
    Router to direct database operations for the Movement model to the 'movement_files' database.
    """
    def db_for_read(self, model, **hints):
        if model.__name__ == 'Movement':
            return 'movement_files'
        return None


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'Movement':
            return db == 'movement_files'
        return None