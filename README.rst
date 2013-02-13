.. contents:: **Indice**

Introduction
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

L'area del paziente contiene un form da compilare, che va configurato a dovere secondo le necessità.

.. figure:: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-03.png/image_preview
   :target: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-03.png

E' possibile inserire altri form all'interno della sezione. La vista principale della sezione dell'utente li
supporterà.

.. figure:: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-04.png/image_preview
   :target: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-04.png

Utilizzo da parte dei medici
----------------------------

Perché i medici siano in grado di compilare i form, devono avere un ruolo di **Contributore** sul form stesso.

.. figure:: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-05.png/image_preview
   :target: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-05.png

A questo punto la compilazione del form permetterà solo di generare delle schede relative al paziente.

.. figure:: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-06.png/image_preview
   :target: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-06.png

Le schede vengono create in uno stato "*Da classificare*".
Il medico creatore della scheda ha poi la possibilità di cambiare questo stato in base alla gravità della situazione.

.. figure:: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-07.png/image_preview
   :target: http://blog.redturtle.it/pypi-images/ospfe.percorso_sla/ospfe.percorso_sla-0.1-07.png

L'utlizzo dello stato "*Rosso*" determina una criticità di livello alto.
In questo caso tutti gli utenti di tutti i gruppi inseriti nella sezione "*Gruppi di notifica*" discussa sopra,
saranno contattati via e-mail.

Credits
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

