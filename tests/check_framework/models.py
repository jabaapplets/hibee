from hibeecore.checks import register
from hibeedb import models


class SimpleModel(models.Model):
    field = models.IntegerField()
    manager = models.manager.Manager()


@register("tests")
def my_check(app_configs, **kwargs):
    my_check.did_run = True
    return []


my_check.did_run = False
