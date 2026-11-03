# Validation du chat bilingue FixIT

Date, modèle Groq et collection : 2026-11-03, `openai/gpt-oss-20b` (Groq), collection Qdrant `fixit_19660c98de13ccc0` (`http://127.0.0.1:6335`).
Nombre de points : 400 passages indexés (46 PDF, 140 pages) — chiffres identiques à ceux du document de passation.
Tests unitaires : `python -m unittest assistant.test_chat -v` → 5 tests, OK (Ran 5 tests in 0.004s, OK).

## Cas A

Question : « Mon ordinateur ne trouve aucun réseau Wi-Fi. »
Langue attendue / obtenue : fr / fr
Réponse réelle et sources affichées :
```
1. Vérifiez que le commutateur Wi-Fi physique de votre ordinateur est activé. [S1]
2. Activez le Wi-Fi dans Paramètres > Réseau & Internet. [S1]
3. Assurez-vous que votre carte réseau prend en charge la bande de fréquence utilisée par votre routeur (2,4 GHz ou 5 GHz). [S1]
4. Si le problème persiste, lancez SupportAssist pour une réparation automatisée du Wi-Fi. [S3]

[S1] DOC001 - Résoudre les problèmes de connexion Wi-Fi dans Windows
Page 8 | https://support.microsoft.com/fr-fr/windows/experience/connectivity-networking/fix-wi-fi-connection-issues-in-windows
[S3] DOC003 - Dépanner la connexion Wi-Fi sur un PC Dell
Page 3 | https://www.dell.com/support/contents/fr-fr/article/product-support/self-support-knowledgebase/networking-wifi-and-bluetooth/wireless-networking
```
Document, page et passage vérifiés : DOC001 p. 8 est bien le premier résultat de recherche (score 0,88), conforme à la page 2 du document de passation. L'étape 4 cite DOC003 (guide Dell) pour SupportAssist, un outil spécifique au matériel Dell ; recommandé ici pour un PC générique, ce qui est une légère sur-généralisation à surveiller.
Verdict et correction éventuelle : **Réussi**. Point d'attention mineur : filtrer ou signaler les procédures propres à une marque (Dell) avant de les proposer à un utilisateur dont le matériel n'est pas identifié — à traiter via le filtre `marque`/`modele` déjà prévu dans les métadonnées (F04 du cahier des charges).

## Cas B

Question : « My computer cannot find any Wi-Fi networks. »
Langue attendue / obtenue : en / en
Réponse réelle et sources affichées :
```
1. Open SupportAssist and run the automated Wi-Fi repair. In the Start menu, launch SupportAssist, go to the Support tab, click "View common issues", then "Get started" and finally click "Run now" to let the tool fix any Wi-Fi problems. [S1]
2. If the repair doesn't help, forget the network and reconnect. Click the Wi-Fi icon in the taskbar, choose "Manage Wi-Fi connections", find your network, click "Forget", then select the network again, enter the password, and click "Connect". [S3]

[S1] DOC003 - Dépanner la connexion Wi-Fi sur un PC Dell
Page 3 | https://www.dell.com/support/contents/fr-fr/article/product-support/self-support-knowledgebase/networking-wifi-and-bluetooth/wireless-networking
[S3] DOC003 - Dépanner la connexion Wi-Fi sur un PC Dell
Page 3 | https://www.dell.com/support/contents/fr-fr/article/product-support/self-support-knowledgebase/networking-wifi-and-bluetooth/wireless-networking
```
Document, page et passage vérifiés : la langue de réponse (anglais) est correcte, et les deux étapes citent des passages réels de DOC003 p. 3. En revanche, **DOC001 p. 8 n'est pas retrouvé** : `python -m assistant.services.retrieval "My computer cannot find any Wi-Fi networks."` confirme que la recherche dense place DOC003 p. 3 (score 0,864) légèrement devant DOC001 p. 7 (score 0,862), DOC001 p. 8 n'apparaissant pas dans les 3 premiers résultats pour cette formulation anglaise (contrairement à la question française équivalente du cas A).
Verdict et correction éventuelle : **Partiellement réussi**. La génération et les citations sont fidèles aux passages reçus (pas d'invention), mais c'est un problème de recherche dense, pas de génération : la similarité multilingue (`multilingual-e5-small`) classe un guide Dell légèrement devant le guide Microsoft générique pour la formulation anglaise. À surveiller lors de la comparaison des configurations A/B/C (recherche hybride BM25 + reranking, section 6.4 du cahier des charges) qui pourrait corriger ce classement.

## Cas C

Question : « My PC is connected to Wi-Fi but has no internet access. »
Langue attendue / obtenue : en / en
Réponse réelle et sources affichées :
```
1. Run the SupportAssist automated Wi-Fi repair to let the tool fix common connectivity problems. [S1]
2. Make sure the physical Wi-Fi switch on your laptop or tablet is on and that Wi-Fi is enabled in Windows Settings → Network & Internet. [S2]
3. Open an elevated command prompt and run `ipconfig /release`, `ipconfig /renew`, then `ipconfig /flushdns`. Disable any manual proxy settings in Settings → Network & Proxy Internet. [S3]
4. Verify that your PC has obtained a valid IP address and is not using a link-local address like 169.254.x.x, which indicates it failed to get an IP from the router. [S3]

[S1] DOC003 - Dépanner la connexion Wi-Fi sur un PC Dell
Page 3 | https://www.dell.com/support/contents/fr-fr/article/product-support/self-support-knowledgebase/networking-wifi-and-bluetooth/wireless-networking
[S2] DOC001 - Résoudre les problèmes de connexion Wi-Fi dans Windows
Page 8 | https://support.microsoft.com/fr-fr/windows/experience/connectivity-networking/fix-wi-fi-connection-issues-in-windows
[S3] DOC001 - Résoudre les problèmes de connexion Wi-Fi dans Windows
Page 7 | https://support.microsoft.com/fr-fr/windows/experience/connectivity-networking/fix-wi-fi-connection-issues-in-windows
```
Document, page et passage vérifiés : DOC001 p. 7 est bien retrouvé et cité, conforme à l'attente de la page 8 du document de passation. Les étapes distinguent correctement « connecté au Wi-Fi mais sans accès Internet » (ipconfig, adresse 169.254.x.x) du symptôme « aucun réseau visible » du cas A/B.
Verdict et correction éventuelle : **Réussi**. Aucune correction nécessaire.

## Cas D

Question : « Comment remplacer la courroie de ma voiture ? »
Langue attendue / obtenue : fr / fr
Réponse réelle et sources affichées :
```
Les guides disponibles ne suffisent pas pour répondre.
```
(aucune source)
Document, page et passage vérifiés : hors sujet par rapport au corpus FixIT (Windows/Wi-Fi). Repli correct, pas d'invention de procédure.
Verdict et correction éventuelle : **Réussi**. Conforme à l'attente (repli en français, sources vides).

## Cas E

Question : « How do I replace the timing belt in my car? »
Langue attendue / obtenue : en / en
Réponse réelle et sources affichées :
```
The available guides do not contain enough information to answer.
```
(aucune source)
Document, page et passage vérifiés : hors sujet, repli dans la bonne langue (anglais cette fois).
Verdict et correction éventuelle : **Réussi**. Conforme à l'attente.

## Cas F

Question : « Mon ordinateur ne trouve aucun réseau Wi-Fi. Answer in English. »
Langue attendue / obtenue : en / en
Réponse réelle et sources affichées :
```
1. Check that Wi-Fi is turned on in the system settings or by clicking the Wi-Fi icon on the taskbar. [S2]
2. Disable and re-enable the Wi-Fi adapter: open the network settings, turn Wi-Fi off, wait a few seconds, then turn it back on. [S1]
3. Run the automated Wi-Fi repair in SupportAssist: open SupportAssist, go to the Support tab, select "I can't connect to Wi-Fi," and click "Run now." [S3]

[S2] DOC001 - Résoudre les problèmes de connexion Wi-Fi dans Windows
Page 1 | https://support.microsoft.com/fr-fr/windows/experience/connectivity-networking/fix-wi-fi-connection-issues-in-windows
[S1] DOC001 - Résoudre les problèmes de connexion Wi-Fi dans Windows
Page 7 | https://support.microsoft.com/fr-fr/windows/experience/connectivity-networking/fix-wi-fi-connection-issues-in-windows
[S3] DOC003 - Dépanner la connexion Wi-Fi sur un PC Dell
Page 3 | https://www.dell.com/support/contents/fr-fr/article/product-support/self-support-knowledgebase/networking-wifi-and-bluetooth/wireless-networking
```
Document, page et passage vérifiés : la préférence explicite « Answer in English » est bien respectée malgré la question posée en français, conformément à la règle de langue du document (priorité à la demande explicite). Citations vérifiables (DOC001 p. 1 et p. 7, DOC003 p. 3).
Verdict et correction éventuelle : **Réussi**. Aucune correction nécessaire.

## Cas G

Question : « Wi-Fi ? »
Langue attendue / obtenue : fr / fr
Réponse réelle et sources affichées :
```
1. Ouvrez les paramètres Wi-Fi : Démarrer > Paramètres > Réseau & Internet > Wi-Fi. [S1]
2. Vérifiez que le mode Avion est désactivé et que le Wi-Fi est activé. [S2]
3. Testez la connexion Internet ; si vous êtes connecté au Wi-Fi mais que vous ne pouvez pas accéder à des sites, notez le message « Connectivité limitée ». [S2]
4. Suivez les instructions de résolution de problèmes de Wi-Fi pour diagnostiquer et corriger les déconnexions ou la lenteur. [S3]

[S1] DOC028 - Résoudre les problèmes de mise à jour de Windows
Page 1 | https://support.microsoft.com/fr-fr/kb/976982
[S2] DOC003 - Dépanner la connexion Wi-Fi sur un PC Dell
Page 1 | https://www.dell.com/support/contents/fr-fr/article/product-support/self-support-knowledgebase/networking-wifi-and-bluetooth/wireless-networking
[S3] DOC003 - Dépanner la connexion Wi-Fi sur un PC Dell
Page 1 | https://www.dell.com/support/contents/fr-fr/article/product-support/self-support-knowledgebase/networking-wifi-and-bluetooth/wireless-networking
```
Document, page et passage vérifiés : la langue de repli français est bien appliquée pour cette question ambiguë de deux mots, comme demandé. En revanche, le passage le mieux classé (DOC028, guide Windows Update) n'est pas topiquement pertinent pour « Wi-Fi ? » — confirmé par `python -m assistant.services.retrieval "Wi-Fi ?"` (score 0,8663, devant les passages Dell Wi-Fi à 0,8505). La requête de 2 mots est trop courte pour bien discriminer les passages par similarité dense.
Verdict et correction éventuelle : **Réussi sur le critère testé** (langue française conservée même en cas d'ambiguïté). Point d'attention : la pertinence documentaire pour les questions très courtes/ambiguës reste faible ; une clarification préalable (F01 du cahier des charges) ou une requête plus longue limiterait ce risque — non corrigé dans ce lot, hors périmètre de la passation (service de chat seul, sans étape de clarification).

## Synthèse

| Cas | Langue | Citations fidèles | Pertinence documentaire | Verdict |
|---|---|---|---|---|
| A | OK | OK | OK (DOC001 p.8 en 1er) | Réussi |
| B | OK | OK | Attention (DOC001 p.8 non retrouvé en anglais) | Partiellement réussi |
| C | OK | OK | OK (DOC001 p.7 retrouvé) | Réussi |
| D | OK | OK (repli, sources vides) | — | Réussi |
| E | OK | OK (repli, sources vides) | — | Réussi |
| F | OK (priorité explicite respectée) | OK | OK | Réussi |
| G | OK (repli fr par défaut) | OK | Attention (passage hors-sujet en tête) | Réussi sur le critère testé |

6 cas sur 7 pleinement réussis ; le cas B révèle une limite de la recherche dense multilingue (anglais → léger biais vers un guide de marque) à surveiller lors de la comparaison des configurations A/B/C (recherche hybride + reranking) prévue par le cahier des charges. Aucun cas n'a produit d'invention de procédure ou d'URL, et le choix de langue a été correct dans les 7 cas, y compris les cas ambigu (G) et de préférence explicite (F).
