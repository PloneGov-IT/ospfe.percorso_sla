# -*- coding: utf-8 -*-
from ospfe.percorso_sla import percorso_slaMessageFactory as _
from Products.CMFCore.utils import getToolByName
from Products.validation.i18n import recursiveTranslate
from Products.validation.interfaces.IValidator import IValidator

class ValidGroupsValidator:
    """
    Check if groups enter by user exist
    """

    __implements__ = (IValidator,)

    name = 'validgroupsvalidator'
    
    def __call__(self, value, instance, *args, **kwargs):
        acl_users = getToolByName(instance, 'acl_users')
        
        invalid_groups = []
        for group in value:
            if not acl_users.getGroupById(group) and not acl_users.getGroupByName(group):
                invalid_groups.append(group)

        if invalid_groups:
            if len(invalid_groups) == 1:
                msg = _('invalid_group_error_msg',
                        default=u"The ${group} group doesn't exist",
                        mapping={'group': invalid_groups[0]})
            else:
                msg = _('invalid_groups_error_msg',
                        default=u"The following groups don't exist: ${groups}",
                        mapping={'groups': ', '.join(invalid_groups)})
            return recursiveTranslate(msg, **kwargs)
        else:
            return True
