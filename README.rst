.. contents:: **Indice**

Introduzione
============

Questo prodotto Plone è stato studiato per aiutare i medici nella raccolta dati e condivisione delle informazioni
relative ai pazienti di `SLA`__

__ http://it.wikipedia.org/wiki/Sclerosi_laterale_amiotrofica

L'utilizzo di questo prodotto genera delle schede di raccolta dati e permette ai medici di discutere dei casi
clinici.

Guida
=====

Il prodotto è basato su due componenti Plone:

* `PloneFormGen`__
* `uwosh.pfg.d2c`__

__ http://plone.org/products/ploneformgen
__ http://pypi.python.org/pypi/uwosh.pfg.d2c

Creazione dell'area paziente
----------------------------

Viene aggiunto un nuovo contenuto Plone, che è il "**Paziente SLA**".

.. figure:: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-01.png/image_preview
   :target: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-01.png

Il contenuto raccoglie una serie di dati del paziente. Una nota particolare solo sul campo "*Gruppi di notifica*"
che sarà discusso in seguito.

.. figure:: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-02.png/image_preview
   :target: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-02.png

L'area del paziente appena creata, contiene una serie di form da compilare, che possono essere configurati a dovere
secondo le necessità.

.. figure:: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-03.png/image_preview
   :target: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-03.png

E' possibile inserire altri form all'interno della sezione. La vista principale della sezione dell'utente li
supporterà.

.. figure:: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-04.png/image_preview
   :target: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-04.png

Utilizzo da parte dei medici
----------------------------

Perché i medici siano in grado di creare pazienti e compilare i form, devono avere un ruolo di **Contributore**.

Della creazione di un paziente si è già parlato precedentemente. La compilazione del form, invece, permetterà solo di
generare delle schede relative al paziente.

.. figure:: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-06.png/image_preview
   :target: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-06.png

Le schede vengono create in uno stato "*Da classificare*".
Il medico creatore della scheda ha poi la possibilità di cambiare questo stato in base alla gravità della situazione.

.. figure:: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-07.png/image_preview
   :target: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-07.png

L'utilizzo dello stato "*Rosso*" determina una criticità di livello alto.

Tutti gli utenti di tutti i gruppi inseriti nella sezione "*Gruppi di notifica*" discussa sopra,
saranno contattati via e-mail ad ogni cambio di stato del documento se la scheda viene portata in uno stato non
ancora utilizzato da altre schede per quel tipo di osservazione.

Modello per i pazienti
======================

Nella configurazione del portale, è presente un pannello di controllo che permette di impostare un Paziente "base"
da utilizzare come modello per i futuri pazienti creati.

.. figure:: http://admin.blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-settings.png/image_mini
   :target: http://admin.blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-settings.png

Il paziente modello non è altro che un semplice contenuto di tipo "Paziente" al cui interno si vanno a creare una
serie di form predefiniti che saranno utilizzati come base di partenza per i successivi pazienti.
Alla creazione di nuovi pazienti, vengono copiati al loro interno i form presenti nel paziente modello, oltre alla lista
dei suoi "*Gruppi di notifica*".

**NBB**: il form generato contiene un *campo nascosto* con id "``title-sla-form``".
Tale campo va mantenuto per poter usufruire della funzionalità di generazione automatica del titolo
(non viene usata la funzionalità di generazione dinamica del titolo nativa di uwosh.pfg.d2c in quanto
`incompatibile con Plone 3`__).

__ https://github.com/collective/uwosh.pfg.d2c/issues/6

Crediti
=======

Sviluppato col supporto dell'`Ospedale S. Anna, Ferrara`__; l'Ospedale S. Anna supporta
`l'iniziativa PloneGov`__.

.. image:: http://www.ospfe.it/ospfe-logo.jpg
   :alt: OspFE logo

__ http://www.ospfe.it/
__ http://www.plonegov.it/

Autori
=======

Questo prodotto è stato sviluppato da RedTurtle Technology.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
