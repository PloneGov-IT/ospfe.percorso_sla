"""Definition of the SLA Patient content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.Archetypes.atapi import AnnotationStorage
from Products.Archetypes.atapi import LinesWidget, RichWidget
from Products.Archetypes.atapi import LinesField, TextField
from Products.Archetypes.public import DisplayList
from Products.ATContentTypes import ATCTMessageFactory
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from ospfe.percorso_sla.interfaces import ISLAPatient
from ospfe.percorso_sla.config import PROJECTNAME
from ospfe.percorso_sla.validator import ValidGroupsValidator
from ospfe.percorso_sla import percorso_slaMessageFactory as _


SLAPatientSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.DateTimeField('birthday',
          required=False,
          widget=atapi.CalendarWidget(
                    description=_(u'help_birthday',
                                    default=u'Insert the birthday of this patient.'),
                    label=_(u'label_birthday', default=u'Patient birthday'),
                    starting_year=1930,
                    future_years=0,
                    show_hm=False)
    ),

    atapi.StringField('patientGender',
          required=True,
          vocabulary=[("M", "M"), ("F", "F")],
          widget=atapi.SelectionWidget(
                    description=_(u'help_patientgender',
                                    default=u''),
                    label=_(u'label_patientgender', default=u'Patient gender'),
                    )
    ),

    atapi.DateTimeField('diseaseAppearance',
          required=False,
          widget=atapi.CalendarWidget(
                    description=_(u'help_diseaseappearance',
                                    default=u'Insert the year when the disease appears.'),
                    label=_(u'label_diseaseappearance', default=u'Diease appearance'),
                    starting_year=1930,
                    future_years=0,
                    show_hm=False)
    ),

    atapi.DateTimeField('diagnosisYear',
          required=False,
          widget=atapi.CalendarWidget(
                    description=_(u'help_diagnosisyear',
                                    default=u'Insert the year when the disease was diagnosed.'),
                    label=_(u'label_diagnosisyear', default=u'Diagnosis year'),
                    starting_year=1930,
                    future_years=0,
                    show_hm=False)
    ),

    atapi.StringField('appearanceType',
          required=False,
          vocabulary="appearanceTypeVocabulary",
          widget=atapi.SelectionWidget(
                    description=_(u'help_appearancetype',
                                    default=u''),
                    label=_(u'label_appearancetype', default=u'Appearance type'),
                    )
    ),

    LinesField('notification_groups',
          write_permission="Manage portal",
          required=False,
          searchable=False,
          validators=(ValidGroupsValidator()),
          widget=LinesWidget(
                    description=_(u'help_notification_groups',
                                  default=u'Enter a list of groups of doctors who must be notified if the SLA form of patient changes to the "Red" state (one per line). Please verify that the users in the groups have access to the patient.'),
                    label=_(u'label_notification_groups', default=u'Notification Groups'))
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

SLAPatientSchema['title'].storage = atapi.AnnotationStorage()
SLAPatientSchema['description'].storage = atapi.AnnotationStorage()
SLAPatientSchema['title'].widget.label = _(u'label_title', default=u'Name and surname')

schemata.finalizeATCTSchema(
    SLAPatientSchema,
    folderish=True,
    moveDiscussion=False
)


class SLAPatient(folder.ATFolder):
    """Description of the Example Type"""
    implements(ISLAPatient)

    meta_type = "SLAPatient"
    schema = SLAPatientSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    def appearanceTypeVocabulary(self):
        """
        """
        return DisplayList([('', ''),
                            ('bulbare', 'Bulbare'),
                            ('comune', 'Comune'),
                            ('pseudopolinevritico', 'Pseudopolinevritico'),
                            ('piramidale', 'Piramidale')])

atapi.registerType(SLAPatient, PROJECTNAME)
