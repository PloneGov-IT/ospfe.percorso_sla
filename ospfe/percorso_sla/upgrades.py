# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from ospfe.percorso_sla import logger

default_profile = 'profile-ospfe.percorso_sla:default'


def upgrade(upgrade_product, version):
    """ Decorator for updating the QuickInstaller of a upgrade """
    def wrap_func(fn):
        def wrap_func_args(context, *args):
            p = getToolByName(context, 'portal_quickinstaller').get(upgrade_product)
            setattr(p, 'installedversion', version)
            return fn(context, *args)
        return wrap_func_args
    return wrap_func


@upgrade('ospfe.percorso_sla', '0.4')
def to_1100(context):
    """
    """
    logger.info('Upgrading ospfe.percorso_sla to version 0.4')
    context.runAllImportStepsFromProfile(default_profile)
    logger.info('End of upgrade step')
