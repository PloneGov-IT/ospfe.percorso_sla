# -*- coding: utf-8 -*-
from ospfe.percorso_sla.adapters.mails.mail_base import PercorsoSLAMailBase

class NotifyDoctor(PercorsoSLAMailBase):
    """
    Classe invio email ai medici. Estende PercorsoSLAMailBase
    """

    def send(self):
        """
        Effettuo l'invio richiamando il metodo della classe base
        """
        if not self.sla_patient:
            return False

        self.sendEmail(self._addresses, self._subject, self._text)
