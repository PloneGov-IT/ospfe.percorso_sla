# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema

from ospfe.percorso_sla import percorso_slaMessageFactory as _


class ISLAPatientSettings(Interface):
    """Settings used in the control panel for set the patient model template
    """

    model_patient = schema.TextLine(
                    title=_("model_patient_label", default=u"Model patient location"),
                    required=True,
                    description=_('model_patient_help',
                        default=u"Insert the path where the model patient is stored.")
            )
