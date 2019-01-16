class MyAppConfig(AppConfig):

    name = 'myapp'

    def ready(self):
        """ Load monkey patching. """
        # For multiple apps, it should not matter which one you do this
        try:
            from myproject.local import monkey_patch
            monkey_patch()
        except ImportError:
            pass
