# Aide à la notation des réponses FixIT

Fichier à noter : `evaluation/results/generation_20261119_153419.csv` (colonne `note_0_1_2`, et `commentaire` pour chaque 0 ou 1).

## Comment juger sans être experte : 3 questions simples

Pour chaque réponse, pose-toi ces trois questions.

1. **La réponse parle-t-elle du problème posé ?** Compare le sujet de la question avec celui des étapes. Une question sur le démarrage lent avec des étapes sur le Microsoft Store, c'est à côté du sujet.
2. **Chaque étape est-elle dans le texte du guide ?** Sous la réponse, tu as les extraits que FixIT a lus. Cherche la même idée dans l'extrait cité entre crochets : `[S1]` renvoie à l'extrait S1. Si l'étape n'y est pas, elle est inventée ou mal sourcée.
3. **La réponse est-elle utile à quelqu'un qui a ce problème ?** Un conseil précis (où cliquer, quoi vérifier) est utile. Une phrase vague, ou un conseil sans rapport, ne l'est pas.

**Règle pratique pour la note :**

- **2** : tu réponds oui aux trois questions, et il n'y a pas d'étape hors sujet.
- **1** : le sujet est bon, mais une étape est hors sujet ou absente du guide, ou la réponse est incomplète.
- **0** : la réponse parle d'autre chose, invente, ou répond « les guides ne suffisent pas » alors que la question est couverte.

Les signalements « ⚠ » sont des contrôles automatiques, pas des notes. Un guide « non cité » ne veut pas dire que la réponse est fausse : le modèle a peut-être trouvé une autre source qui convient.


## Les 40 questions à noter

### 1/40 — F001 (PC01, fr)

**Question :** Windows met très longtemps à démarrer le matin.

**Guides attendus :** DOC005 (Configurer les applications de démarrage dans Windows); DOC004 (Améliorer les performances du PC sous Windows)

**⚠ aucun guide attendu n'est cité**

**Réponse de FixIT :**

> Windows met trop de temps à démarrer le matin.
> 1. Videz le cache du Microsoft Store en ouvrant Exécuter (Win + R) et en tapant wsreset.exe. La fenêtre de commande s’ouvre puis se ferme, et le Store s’ouvre automatiquement. [S1]
> 2. Réinitialisez Windows Update en exécutant le dépanneur « Résoudre les problèmes » : Démarrer > Paramètres > Système > Résoudre les problèmes > Autres utilitaires de résolution des problèmes, puis sélectionnez « Exécuter » à côté de Windows Update. [S1]
> 3. Libérez de l’espace disque si votre PC est plein. Suivez les techniques décrites dans l’article « Libérer de l’espace disque dans Windows ». [S2]
> 4. Videz le cache de Windows Update : ouvrez Services (Win + R > services.msc), arrêtez le service Windows Update, supprimez tout le contenu de C:\Windows\SoftwareDistribution, puis redémarrez le service. Après cela, lancez à nouveau Windows Update via Paramètres > Windows Update > Rechercher les mises à jour et redémarrez votre ordinateur. [S3]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC008 — Libérer de l'espace disque dans Windows (page 1) : « >Résoudre >les problèmes Autres utilitaires de résolution des problèmes, puis à côté des Applications du Windows Store, sélectionnez Exécuter. 2. Pour vider le cache du Microsoft Store, appuyez sur la touche + du logo WindowsR pour ouvrir la boîte de dialogue Exécuter, puis tapez wsreset.exe et sélectionnez OK. Une fenêtre d’invite de commandes vide s’ouvre et après environ 10 secondes, la fenêtre se ferme et le Store s’ouvre automatiquement. 3. Pour réinitialiser Windows Update, sélectionnez Démarrer >Paramètres >Système >Résoudre >les problèmes Autres utilitaires de résolution des problèmes, puis en regard de Windows Update , sélectionnez […] »
- **[S2]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 3) : « Si votre PC dispose d’un faible espace disque, essayez d’adopter les techniques présentées dans l’article Libérer de l’espace disque dans Windows. Étape 9. Exécutez de nouveau Windows Update. Même si vous avez téléchargé des mises à jour, d’autres peuvent être disponibles. Après avoir essayé les étapes précédentes, exécutez à nouveau Windows Update en sélectionnant>Paramètres>de démarrage Windows Update>Rechercher les mises à jour. Téléchargez et installez les nouvelles mises à jour. Étape 10. Redémarrez pour appliquer les mises à jour installées De nombreuses mises à jour nécessiteront le redémarrage de votre appareil. Enregistrez votre […] »
- **[S3]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 4) : « - Suivez les instructions à l’écran pour terminer le processus. Videz le cache de Windows Update : - Appuyez sur Win + R, tapez services.msc, puis appuyez sur Entrée. - Recherchez le service Windows Update , cliquez dessus avec le bouton droit de la souris, puis sélectionnez Arrêter. - Accédez à C :\Windows\SoftwareDistribution. - Supprimez tous les fichiers et dossiers à l’intérieur de ce répertoire. - Revenez à la fenêtre Services, cliquez avec le bouton droit sur Windows Update et sélectionnez Démarrer. 0x800705b4 : L’installation de la mise à jour a pris trop de temps ou a été interrompue Vérifiez votre connexion Internet : - […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 2/40 — F002 (PC01, en)

**Question :** My PC takes forever to boot up.

**Guides attendus :** DOC005 (Configurer les applications de démarrage dans Windows); DOC004 (Améliorer les performances du PC sous Windows)

**⚠ aucun guide attendu n'est cité**

**Réponse de FixIT :**

> Your PC is experiencing very slow boot times.
> 1. Clear the Windows Update cache by stopping the Windows Update service, deleting all files in C:\Windows\SoftwareDistribution, and restarting the service. [S1]
> 2. Check your internet connection by going to Settings > Network & Internet > Wi‑Fi and ensuring you are connected. [S1]
> 3. Temporarily disable any antivirus or firewall that might block updates. [S1]
> If the problem persists after these checks, you can open a ticket so that a technician can take over.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 4) : « - Suivez les instructions à l’écran pour terminer le processus. Videz le cache de Windows Update : - Appuyez sur Win + R, tapez services.msc, puis appuyez sur Entrée. - Recherchez le service Windows Update , cliquez dessus avec le bouton droit de la souris, puis sélectionnez Arrêter. - Accédez à C :\Windows\SoftwareDistribution. - Supprimez tous les fichiers et dossiers à l’intérieur de ce répertoire. - Revenez à la fenêtre Services, cliquez avec le bouton droit sur Windows Update et sélectionnez Démarrer. 0x800705b4 : L’installation de la mise à jour a pris trop de temps ou a été interrompue Vérifiez votre connexion Internet : - […] »
- **[S2]** DOC044 — Codes d'erreur dans le Gestionnaire de périphériques de Windows (page 6) : « Cette erreur signifie que Windows est en train de supprimer le périphérique. Toutefois, le périphérique n'a pas encore été totalement supprimé. Ce code d'erreur est temporaire et ne s'affiche que pendant les tentatives d'interrogation et de suppression d'un périphérique. Résolutions recommandées Vous pouvez attendre que Windows ait terminé de supprimer le périphérique ou vous pouvez redémarrer l'ordinateur. - Attendez quelques secondes, puis appuyez sur la touche F5 pour mettre à jour l'affichage du Gestionnaire de périphériques. - Si le problème n'est pas résolu, redémarrez votre ordinateur. Cliquez sur Démarrer, sur Arrêter, puis […] »
- **[S3]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « 2. Sous l’onglet Support, sous View common issues, cliquez sur Get started. 3. Développez I want to troubleshoot my PC, puis I’m having connectivity issues et cliquez sur I can’t connect to WiFi. 4. Cliquez sur le bouton Run now pour laisser SupportAssist exécuter une réparation automatisée du Wi-Fi. Si la réparation automatisée SupportAssist n’a pas résolu le problème Wi-Fi, passez à l’étape suivante. »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 3/40 — F003 (PC01, fr)

**Question :** Le processeur de mon PC est constamment à 100 %.

**Guides attendus :** DOC035 (Processeur : utilisation élevée (proche de 100 %)); DOC004 (Améliorer les performances du PC sous Windows)

**Réponse de FixIT :**

> Le processeur de votre PC reste à 100 % de charge.
> 1. Ouvrez le Gestionnaire des tâches (Ctrl + Maj + Échap) et repérez le processus qui consomme le CPU. Fermez les applications ou onglets inutiles, puis redémarrez le PC si nécessaire. [S3]
> 2. Exécutez une analyse rapide de Windows Security pour détecter d’éventuels programmes malveillants qui pourraient saturer le processeur. [S1]
> 3. Vérifiez qu’il reste au moins 10 % d’espace libre sur le disque principal et assurez‑vous que Windows 11 est à jour (Démarrer > Paramètres > Windows Update). [S2]
> 4. Désactivez les programmes inutiles au démarrage (Paramètres > Applications > Démarrage) et surveillez la température du CPU pour éviter la surchauffe. [S3]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC004 — Améliorer les performances du PC sous Windows (page 2) : « Remarque L’appareil peut redémarrer si nécessaire pour terminer le processus d’installation. Solution 2. Exécutez une analyse des programmes malveillants pour détecter et éliminer les menaces qui ralentissent les performances du PC Les programmes malveillants peuvent consommer des ressources UC et disque, ce qui peut réduire les performances du système. L’exécution d’une analyse des programmes malveillants peut vous aider à détecter et à supprimer les menaces. 1. SélectionnezParamètres>de>confidentialité & de sécurité>Sécurité Windows> protection contre les virus & les menaces. 2. Sélectionnez Analyse rapide. Remarque L’appareil peut […] »
- **[S2]** DOC031 — Résolution des erreurs de code d'arrêt et de redémarrage inattendu (page 2) : « - Vérifiez que le disque dur dispose de suffisamment d’espace. Le système d’exploitation et certaines applications ont besoin d’un espace libre suffisant pour créer des fichiers d’échange et exécuter d’autres fonctions. Les exigences exactes varient en fonction de la configuration du système, mais il est judicieux d’avoir 10 à 15 % de l’espace libre disponible. - Installez les dernières mises à jour de Windows 11. Pour rechercher des mises à jour, sélectionnez Démarrer>Paramètres>Windows Update , puis sélectionnez Rechercher des mises à jour. - Restaurer Windows 11. Si aucune de ces étapes ne vous aide, essayez de restaurer Windows 11 à […] »
- **[S3]** DOC036 — Gel et lenteurs du système (page 1) : « Reconnaître la situation Le PC se fige quelques secondes ou totalement (curseur bloqué), ou l'ensemble devient lent. Distinguer un gel ponctuel d'un gel qui revient régulièrement. Vérifications rapides  Patienter quelques instants : un pic de disque ou de processeur peut se résorber seul.  Ouvrir le Gestionnaire des tâches (Ctrl + Maj + Échap) et repérer un processus qui sature le processeur, la mémoire ou le disque (colonne Disque à 100 %).  Fermer les applications et onglets inutiles, puis redémarrer. Causes à examiner  Mémoire (RAM) saturée : réduire le nombre d'applications et d'onglets ouverts.  Disque à 100 % : désactiver des […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 4/40 — F004 (PC01, en)

**Question :** My laptop is sluggish and programs take ages to open.

**Guides attendus :** DOC004 (Améliorer les performances du PC sous Windows); DOC036 (Gel et lenteurs du système)

**⚠ aucun guide attendu n'est cité**

**Réponse de FixIT :**

> Your laptop is running slowly and applications take a long time to open.
> 1. Open Task Manager (Ctrl+Alt+Del) to view current memory usage and identify any applications consuming excessive resources. [S3]
> 2. Close unnecessary applications to free up memory, which can improve overall system responsiveness. [S3]
> 3. Check and adjust virtual memory settings via System Properties to ensure adequate paging file size for your workload. [S3]
> If the problem persists after these checks, you can open a ticket so that a technician can take over.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC027 — Options de récupération dans Windows (page 4) : « - Réinstallez Windows à l’aide de Windows Update : vos fichiers personnels, vos applications et vos paramètres sont conservés. - Restauration dans le temps : votre PC est restauré à un point antérieur dans le temps. Les modifications apportées après ce point de restauration sont perdues. Files stockés dans OneDrive ou un autre service cloud ne sont pas affectés. - Restauration du système : vos fichiers personnels sont conservés, mais les modifications apportées au système après le point de restauration sont annulées. Cela peut affecter les applications, pilotes, mises à jour ou paramètres récemment installés. - Réinitialiser ce PC : vous […] »
- **[S2]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « 2. Sous l’onglet Support, sous View common issues, cliquez sur Get started. 3. Développez I want to troubleshoot my PC, puis I’m having connectivity issues et cliquez sur I can’t connect to WiFi. 4. Cliquez sur le bouton Run now pour laisser SupportAssist exécuter une réparation automatisée du Wi-Fi. Si la réparation automatisée SupportAssist n’a pas résolu le problème Wi-Fi, passez à l’étape suivante. »
- **[S3]** DOC044 — Codes d'erreur dans le Gestionnaire de périphériques de Windows (page 2) : « « Le pilote de ce périphérique est peut-être endommagé, ou le niveau de la mémoire disponible ou d'autres ressources sur votre ordinateur est trop bas. (Code 3) » Cause Le pilote du périphérique est peut-être endommagé ou la mémoire est insuffisante. Le niveau de la mémoire disponible sur le système est faible et vous devez libérer ou ajouter de la mémoire. Résolutions recommandées Fermez certaines applications Si l'ordinateur ne possède pas suffisamment de mémoire pour exécuter le périphérique, vous pouvez fermer certaines applications pour que la mémoire soit disponible. Vous pouvez également vérifier les ressources mémoire et système, […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 5/40 — F005 (PC02, fr)

**Question :** Word ne répond plus et je n'arrive pas à le fermer.

**Guides attendus :** DOC029 (Forcer la fermeture d'une application qui ne répond pas); DOC006 (Réparer les applications et programmes dans Windows)

**Réponse de FixIT :**

> Word ne répond plus et ne se ferme pas.
> 1. Sélectionner la fenêtre bloquée puis appuyer sur Alt + F4 pour demander sa fermeture immédiate. [S2]
> 2. Ouvrir le Gestionnaire des tâches avec Ctrl + Maj + Échap, sélectionner Word dans l’onglet Processus, puis cliquer sur Fin de tâche pour forcer sa fermeture. [S2]
> 3. Si la fermeture n’est toujours pas possible, ouvrir une invite de commandes en mode administrateur et exécuter taskkill /IM WINWORD.EXE /F pour terminer le processus. [S2]

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « 2. Sous l’onglet Support, sous View common issues, cliquez sur Get started. 3. Développez I want to troubleshoot my PC, puis I’m having connectivity issues et cliquez sur I can’t connect to WiFi. 4. Cliquez sur le bouton Run now pour laisser SupportAssist exécuter une réparation automatisée du Wi-Fi. Si la réparation automatisée SupportAssist n’a pas résolu le problème Wi-Fi, passez à l’étape suivante. »
- **[S2]** DOC029 — Forcer la fermeture d'une application qui ne répond pas (page 1) : « Reconnaître la situation Une application est figée (« Ne répond pas »), la fenêtre reste blanche ou le clic sur la croix de fermeture ne produit aucun effet. Forcer la fermeture interrompt directement le processus : c'est une mesure de dernier recours, qui fait perdre les données non enregistrées. Méthode 1 - Raccourci Alt + F4 Sélectionner la fenêtre bloquée puis appuyer sur Alt + F4 pour demander sa fermeture immédiate. Méthode 2 - Gestionnaire des tâches (recommandée)  Ouvrir le Gestionnaire des tâches avec Ctrl + Maj + Échap.  Dans l'onglet Processus, sélectionner l'application qui ne répond pas.  Cliquer sur Fin de tâche pour forcer […] »
- **[S3]** DOC026 — Résoudre les problèmes de connexion d'un moniteur externe (page 3) : « Vous avez encore des problèmes ? Si vous avez essayé les procédures décrites dans cet article ou que vous ne savez pas comment résoudre le problème, utilisez le Hub de commentaires Windows pou entrer un bogue. Incluez des détails sur ce que vous faisiez ou les mesures spécifiques que vous preniez lors de la survenue du problème. Connectez-vous au hub de commentaires et suivez les instructions pour résumer et décrire votre problème. Ensuite, sélectionnez votre catégorie, puis ajouter suffisamment d’informations supplémentaires pour recréer le problème. Vos informations permettent à Microsoft de déterminer la cause principale de ce problème. »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 6/40 — F006 (PC02, en)

**Question :** A Windows app won't launch at all.

**Guides attendus :** DOC006 (Réparer les applications et programmes dans Windows); DOC007 (Dépanner les applications du Microsoft Store)

**Réponse de FixIT :**

> The user reports that a Windows application fails to launch.
> 1. Close the application if it is stuck, then reopen it. [S1]
> 2. Check for Windows updates and install any available updates. [S1]
> 3. Verify that the application is compatible with Windows 11. [S1]
> 4. Update Microsoft Store and try launching the app again. [S1]
> If the problem persists after these checks, you can open a ticket so that a technician can take over.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC007 — Dépanner les applications du Microsoft Store (page 1) : « Si vous utilisez Windows 11 et que vous rencontrez des problèmes avec une application du Microsoft Store, tenez compte de ces mises à jour et correctifs. Tout d’abord, connectez-vous à votre compte Microsoft. Ensuite, passez en revue ces solutions possibles dans l’ordre indiqué. 1. Fermez, puis rouvrez l’application. Sélectionnez le bouton Fermer (X) dans le coin supérieur droit de la fenêtre de l’application pour la fermer. Ensuite, rouvrez l’application. 2. Vérifiez que Windows est à jour. SélectionnezParamètres>de démarrage>(phrasefix)Windows UpdateVérifier>les mises à jour. Si une mise à jour est disponible, sélectionnez Installer […] »
- **[S2]** DOC005 — Configurer les applications de démarrage dans Windows (page 2) : « 1. Faites un clic droit sur Démarrer et sélectionnez Gestionnaire des tâches. 2. Sélectionnez l’onglet Applications au démarrage . 3. Sélectionnez l’application que vous souhaitez configurer : Sélectionnez Activer pour démarrer l’application automatiquement lorsque vous vous connectez. Sélectionnez Désactiver pour empêcher le démarrage automatique de l’application. Le Gestionnaire des tâches montre l’impact de chacune des applications sur votre expérience de démarrage : Aucun : application au démarrage désactivée Non mesuré : aucune donnée disponible pour mesurer l’application de démarrage, l’application de démarrage est activée Impact […] »
- **[S3]** DOC035 — Processeur : utilisation élevée (proche de 100 %) (page 1) : «  Désactiver au démarrage les applications non essentielles (Gestionnaire des tâches > Applications au démarrage). Causes fréquentes à examiner  Programme malveillant : lancer une analyse avec Sécurité Windows.  Pilote obsolète ou défectueux : mettre à jour via Windows Update ou le site du fabricant.  Surchauffe entraînant une limitation (throttling) : vérifier la ventilation et le dépoussiérage.  Processus système emballé : le redémarrer depuis l'application Services. Quand aller plus loin Si l'utilisation reste élevée sans application identifiable, suivre la procédure du constructeur et envisager un contrôle matériel. Source officielle […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 7/40 — F007 (PC02, fr)

**Question :** Une application plante dès que je l'ouvre.

**Guides attendus :** DOC006 (Réparer les applications et programmes dans Windows); DOC007 (Dépanner les applications du Microsoft Store)

**⚠ aucun guide attendu n'est cité ; réponse de type repli alors que la question est répondable**

**Réponse de FixIT :**

> Les guides disponibles ne suffisent pas pour répondre.
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC005 — Configurer les applications de démarrage dans Windows (page 2) : « 1. Faites un clic droit sur Démarrer et sélectionnez Gestionnaire des tâches. 2. Sélectionnez l’onglet Applications au démarrage . 3. Sélectionnez l’application que vous souhaitez configurer : Sélectionnez Activer pour démarrer l’application automatiquement lorsque vous vous connectez. Sélectionnez Désactiver pour empêcher le démarrage automatique de l’application. Le Gestionnaire des tâches montre l’impact de chacune des applications sur votre expérience de démarrage : Aucun : application au démarrage désactivée Non mesuré : aucune donnée disponible pour mesurer l’application de démarrage, l’application de démarrage est activée Impact […] »
- **[S2]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 8) : « télécharger l’outil de nouvelle installation. Veillez à lire attentivement les notes sur la page de téléchargement de logiciels avant d’utiliser l’outil. Articles connexes Comment utiliser l’application Contrôle d’intégrité du PC Créer un compte d’administrateur ou d’utilisateur local dans Windows »
- **[S3]** DOC045 — Utiliser votre appareil Windows comme point d'accès mobile (page 1) : « les propriétés par défaut, ou la dernière utilisation dans Paramètres. - Lorsqu’elle est activée, l’action rapide affiche le nombre d’appareils connectés à votre point d’accès mobile. »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 8/40 — F008 (PC02, en)

**Question :** How do I force quit a frozen program on Windows?

**Guides attendus :** DOC029 (Forcer la fermeture d'une application qui ne répond pas)

**Réponse de FixIT :**

> Force quit a frozen program on Windows
> 1. Press Alt+F4 while the frozen window is active to request immediate closure. [S2]
> 2. Open Task Manager with Ctrl+Shift+Esc, select the unresponsive application in the Processes tab, and click End Task. [S2]
> 3. Right‑click the application's icon in the taskbar (Windows 11) and choose End task after enabling the option in Settings > System > Developer options. [S2]
> 4. Use the command line: open Command Prompt, run tasklist to find the program, then taskkill /IM program.exe /F (or PowerShell Stop‑Process -Name "program" -Force). [S1]

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC029 — Forcer la fermeture d'une application qui ne répond pas (page 1) : « suffit de faire un clic droit sur l'icône de l'application dans la barre des tâches, puis de choisir Terminer la tâche. Méthode 4 - Ligne de commande  Invite de commandes : taper tasklist pour repérer le programme, puis taskkill /IM nom_du_programme.exe /F.  PowerShell : Stop-Process -Name "nom_du_programme" -Force. Après la fermeture forcée Si l'application se bloque souvent, la mettre à jour ou la réparer (Paramètres > Applications), vérifier la mémoire et le disque dans le Gestionnaire des tâches, et redémarrer le PC si le système reste instable. Source officielle et article complet : […] »
- **[S2]** DOC029 — Forcer la fermeture d'une application qui ne répond pas (page 1) : « Reconnaître la situation Une application est figée (« Ne répond pas »), la fenêtre reste blanche ou le clic sur la croix de fermeture ne produit aucun effet. Forcer la fermeture interrompt directement le processus : c'est une mesure de dernier recours, qui fait perdre les données non enregistrées. Méthode 1 - Raccourci Alt + F4 Sélectionner la fenêtre bloquée puis appuyer sur Alt + F4 pour demander sa fermeture immédiate. Méthode 2 - Gestionnaire des tâches (recommandée)  Ouvrir le Gestionnaire des tâches avec Ctrl + Maj + Échap.  Dans l'onglet Processus, sélectionner l'application qui ne répond pas.  Cliquer sur Fin de tâche pour forcer […] »
- **[S3]** DOC004 — Améliorer les performances du PC sous Windows (page 3) : « 2. Recherchez les applications à supprimer, sélectionnez Autres options (...), puis sélectionnez Désinstaller. Solution 5. Désactivez le démarrage d’applications pour réduire l’activité en arrière-plan Les applications exécutées au démarrage peuvent ralentir le temps de démarrage et augmenter l’utilisation en arrière-plan. Désactivez les applications dont vous n’avez pas besoin de démarrer automatiquement. 1. Appuyez sur Ctrl + Maj + Échap pour ouvrir le Gestionnaire des tâches. 2. Sélectionnez Applications au démarrage dans le menu de gauche. 3. Cliquez avec le bouton droit sur les applications que vous souhaitez désactiver, puis […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 9/40 — F009 (PC03, fr)

**Question :** Windows affiche que mon disque est presque plein.

**Guides attendus :** DOC008 (Libérer de l'espace disque dans Windows); DOC009 (Gérer l'espace disque avec l'Assistant Stockage)

**Réponse de FixIT :**

> Windows indique que le disque est presque plein.
> 1. Ouvrez Ce PC, sélectionnez un dossier (Vidéos, Musique, Images, Téléchargements) et affichez les fichiers par taille pour identifier les fichiers volumineux. [S1]
> 2. Supprimez ou déplacez les fichiers inutiles vers un support externe, puis videz la Corbeille pour libérer l’espace. [S1]
> 3. Consultez l’article « Libérer de l’espace disque dans Windows » pour appliquer d’autres techniques de nettoyage. [S3]

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC008 — Libérer de l'espace disque dans Windows (page 3) : « 2. Sous Ce PC , dans le menu de gauche, sélectionnez un dossier pour voir quels fichiers y sont enregistrés. Les dossiers Vidéos, Musique, Images et Téléchargements contiennent généralement les fichiers les plus volumineux enregistrés sur votre appareil. 3. Pour afficher la taille des fichiers dans un dossier, sélectionnez Afficher dans la barre des tâches, puis Détails. Cliquez avec le bouton droit dans l’espace ouvert (ou sélectionnez et maintenez appuyé), puis sélectionnez Trier par>taille pour afficher les fichiers les plus volumineux en haut de la liste. 4. Si des fichiers dont vous n’avez plus besoin sont présents sur votre appareil, […] »
- **[S2]** DOC044 — Codes d'erreur dans le Gestionnaire de périphériques de Windows (page 6) : « Cette erreur signifie que Windows est en train de supprimer le périphérique. Toutefois, le périphérique n'a pas encore été totalement supprimé. Ce code d'erreur est temporaire et ne s'affiche que pendant les tentatives d'interrogation et de suppression d'un périphérique. Résolutions recommandées Vous pouvez attendre que Windows ait terminé de supprimer le périphérique ou vous pouvez redémarrer l'ordinateur. - Attendez quelques secondes, puis appuyez sur la touche F5 pour mettre à jour l'affichage du Gestionnaire de périphériques. - Si le problème n'est pas résolu, redémarrez votre ordinateur. Cliquez sur Démarrer, sur Arrêter, puis […] »
- **[S3]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 3) : « Si votre PC dispose d’un faible espace disque, essayez d’adopter les techniques présentées dans l’article Libérer de l’espace disque dans Windows. Étape 9. Exécutez de nouveau Windows Update. Même si vous avez téléchargé des mises à jour, d’autres peuvent être disponibles. Après avoir essayé les étapes précédentes, exécutez à nouveau Windows Update en sélectionnant>Paramètres>de démarrage Windows Update>Rechercher les mises à jour. Téléchargez et installez les nouvelles mises à jour. Étape 10. Redémarrez pour appliquer les mises à jour installées De nombreuses mises à jour nécessiteront le redémarrage de votre appareil. Enregistrez votre […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 10/40 — F010 (PC03, en)

**Question :** How do I clean up temporary files to free space?

**Guides attendus :** DOC008 (Libérer de l'espace disque dans Windows); DOC009 (Gérer l'espace disque avec l'Assistant Stockage)

**⚠ aucun guide attendu n'est cité**

**Réponse de FixIT :**

> User wants to free disk space by removing temporary files on Windows 11.
> 1. Open Settings → Storage → Storage Sense → Run Storage Sense now to automatically delete temporary files and other unused items. [S2]
> 2. Open Settings → Storage → Temporary files, check all the boxes for files you want to delete, then click Delete files. [S2]
> 3. Search for “Disk Cleanup” in the Start menu, select the drive you want to clean, choose the file types to delete (including temporary files), and click OK. [S2]

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC008 — Libérer de l'espace disque dans Windows (page 2) : « Libérer de l’espace avec l’Assistant Stockage L’Assistant Stockage peut automatiquement libérer de l’espace à votre place en éliminant les fichiers inutiles, comme les fichiers temporaires et les éléments contenus dans votre Corbeille. Pour obtenir plus d’informations, consultez Gérer l’espace disque avec l’Assistant Stockage. Libérer de l’espace avec les recommandations de nettoyage Si vous ne souhaitez pas utiliser l’Assistant Stockage, les recommandations de nettoyage peuvent vous aider à identifier et nettoyer les fichiers temporaires et les fichiers système de votre appareil. 1. Sélectionnez Démarrer >les paramètres >Recommandations de […] »
- **[S2]** DOC004 — Améliorer les performances du PC sous Windows (page 2) : « Utilisez l’Assistant Stockage et les outils de nettoyage pour supprimer les fichiers temporaires. Exécutez l’Assistant Stockage pour supprimer automatiquement les fichiers temporaires : 1. Sélectionnez Démarrer>Paramètres>Stockagesystème>. 2. Sélectionnez Assistant Stockage. 3. Sélectionnez l’Assistant Exécuter le stockage maintenant. Effacer manuellement les fichiers temporaires : 1. Sélectionnez Démarrer>Paramètres>Stockagesystème>. 2. Sélectionnez Fichiers temporaires, activez la case activée de tous les fichiers que vous souhaitez supprimer, puis sélectionnez Supprimer les fichiers. Utiliser le Nettoyage de disque : 1. Sélectionnez […] »
- **[S3]** DOC008 — Libérer de l'espace disque dans Windows (page 1) : « de mise à jour de Windows en raison du manque d’espace disque, la réinitialisation ou la réinstallation de Windows peut aider. Pour plus d’informations, consultez Réinstaller Windows. Si une erreur d’espace disque faible s’affiche en raison de la saturation du dossier Temp Si vous avez utilisé les recommandations de nettoyage pour libérer de l’espace sur votre appareil, puis que vous voyez une erreur d’espace disque faible, il est possible que votre dossier Temp se remplisse rapidement avec les fichiers d’application (.appx) utilisés par Microsoft Store. Pour résoudre ce problème, vous devrez réinitialiser le Store, vider le cache du Store […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 11/40 — F011 (PC03, fr)

**Question :** Comment activer le nettoyage automatique du disque ?

**Guides attendus :** DOC009 (Gérer l'espace disque avec l'Assistant Stockage); DOC008 (Libérer de l'espace disque dans Windows)

**⚠ aucun guide attendu n'est cité**

**Réponse de FixIT :**

> Activer l’Assistant Stockage (Storage Sense) pour qu’il libère automatiquement les fichiers temporaires et autres fichiers inutiles.
> 1. Ouvrez Paramètres > Système > Stockage. [S1]
> 2. Sélectionnez « Assistant Stockage » (ou « Storage Sense ») et activez‑le. [S1]
> 3. Configurez la fréquence d’exécution (ex. « Quand l’espace disque est insuffisant ») et choisissez les types de fichiers à supprimer. [S1]
> 4. Enregistrez les paramètres et laissez l’Assistant Stockage gérer automatiquement le nettoyage. [S1]

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC004 — Améliorer les performances du PC sous Windows (page 2) : « Utilisez l’Assistant Stockage et les outils de nettoyage pour supprimer les fichiers temporaires. Exécutez l’Assistant Stockage pour supprimer automatiquement les fichiers temporaires : 1. Sélectionnez Démarrer>Paramètres>Stockagesystème>. 2. Sélectionnez Assistant Stockage. 3. Sélectionnez l’Assistant Exécuter le stockage maintenant. Effacer manuellement les fichiers temporaires : 1. Sélectionnez Démarrer>Paramètres>Stockagesystème>. 2. Sélectionnez Fichiers temporaires, activez la case activée de tous les fichiers que vous souhaitez supprimer, puis sélectionnez Supprimer les fichiers. Utiliser le Nettoyage de disque : 1. Sélectionnez […] »
- **[S2]** DOC009 — Gérer l'espace disque avec l'Assistant Stockage (page 1) : « L’Assistant Stockage peut automatiquement libérer de l’espace à votre place en éliminant les fichiers inutiles, comme les fichiers temporaires et les éléments contenus dans votre Corbeille. Voici plus d’informations sur son fonctionnement et sa configuration pour répondre à vos besoins. Si l’Assistant Stockage est activé avec les paramètres par défaut, il s’exécute lorsque l’espace disque de votre appareil est insuffisant et propre fichiers temporaires inutiles. Le contenu de la Corbeille sera supprimé par défaut après un certain temps, mais les éléments de votre dossier Téléchargements et de OneDrive (ou de tout autre fournisseur de cloud) […] »
- **[S3]** DOC008 — Libérer de l'espace disque dans Windows (page 2) : « Libérer de l’espace avec l’Assistant Stockage L’Assistant Stockage peut automatiquement libérer de l’espace à votre place en éliminant les fichiers inutiles, comme les fichiers temporaires et les éléments contenus dans votre Corbeille. Pour obtenir plus d’informations, consultez Gérer l’espace disque avec l’Assistant Stockage. Libérer de l’espace avec les recommandations de nettoyage Si vous ne souhaitez pas utiliser l’Assistant Stockage, les recommandations de nettoyage peuvent vous aider à identifier et nettoyer les fichiers temporaires et les fichiers système de votre appareil. 1. Sélectionnez Démarrer >les paramètres >Recommandations de […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 12/40 — F012 (PC03, en)

**Question :** My laptop warns there is not enough storage to update.

**Guides attendus :** DOC008 (Libérer de l'espace disque dans Windows); DOC009 (Gérer l'espace disque avec l'Assistant Stockage)

**⚠ aucun guide attendu n'est cité**

**Réponse de FixIT :**

> Your laptop reports insufficient storage to perform a Windows update.
> 1. Check that your laptop has at least 16 GB free for a 32‑bit OS update or 20 GB for a 64‑bit OS update. [S1]
> 2. Free up space by using Disk Cleanup or uninstalling unused applications. [S1]
> 3. If the internal drive is too small, insert a USB drive and use it to perform the update. [S1]
> 4. Run the Windows Update troubleshooter: Settings > System > Troubleshoot > Other troubleshooters > Windows Update > Run. [S1]

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 6) : « - Mettez à jour votre logiciel antivirus. 0x80070002 : Échec de l’installation de la mise à jour Redémarrez votre PC : Redémarrez votre PC pour vous assurer qu’aucune autre application ne bloque le processus de mise à jour. Exécutez l’utilitaire de résolution des problèmes de Windows Update : - Sélectionnez Démarrer> lesystèmede paramètres>. - Sélectionnez Dépanner et choisissez Autres utilitaires de résolution des problèmes. - Localisez Windows Update et sélectionnez Exécuter. - Suivez les instructions à l’écran pour terminer le processus. Vérifiez l’espace disque : Vérifiez que votre appareil dispose d’un espace disque suffisant. Votre […] »
- **[S2]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 5) : « Si votre appareil est équipé d’un petit disque dur, vous devrez peut-être insérer un lecteur USB pour le mettre à jour. Si votre PC dispose d’un faible espace disque, essayez d’adopter les techniques présentées dans l’article Libérer de l’espace disque dans Windows. Désactiver le VPN : Si vous utilisez un VPN, désactivez-le et réessayez. 0x80070057 ou 0x80080005 : Fichiers endommagés ou configurations système incorrectes Exécution du Vérificateur des fichiers système : Ouvrez l’invite de commandes en tant qu’administrateur et tapez sfc/scannow , puis exécutez. Exécutez l’utilitaire de résolution des problèmes de Windows Update : - […] »
- **[S3]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 3) : « Si votre PC dispose d’un faible espace disque, essayez d’adopter les techniques présentées dans l’article Libérer de l’espace disque dans Windows. Étape 9. Exécutez de nouveau Windows Update. Même si vous avez téléchargé des mises à jour, d’autres peuvent être disponibles. Après avoir essayé les étapes précédentes, exécutez à nouveau Windows Update en sélectionnant>Paramètres>de démarrage Windows Update>Rechercher les mises à jour. Téléchargez et installez les nouvelles mises à jour. Étape 10. Redémarrez pour appliquer les mises à jour installées De nombreuses mises à jour nécessiteront le redémarrage de votre appareil. Enregistrez votre […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 13/40 — F013 (PER01, fr)

**Question :** Le son de mon casque ne marche pas sur Windows.

**Guides attendus :** DOC010 (Résoudre les problèmes de son ou audio dans Windows); DOC020 (Périphérique de sortie audio non détecté dans Windows)

**Réponse de FixIT :**

> Le casque audio n’est pas reconnu ou ne produit pas de son sur Windows.
> 1. Vérifiez que le casque apparaît dans le Gestionnaire de périphériques (Contrôleurs audio, vidéo et jeu). [S2]
> 2. Si le périphérique est désactivé, activez‑le (clic droit → Activer l’appareil). [S2]
> 3. Mettez à jour le pilote audio via le Gestionnaire de périphériques (Mettre à jour le pilote → Rechercher automatiquement). [S3]
> 4. Si aucune mise à jour n’est trouvée, désinstallez puis réinstallez le pilote audio (Gestionnaire de périphériques → Désinstaller l’appareil, puis redémarrer). [S1]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC011 — Résoudre les problèmes de microphone dans Windows (page 2) : « Sélectionnez Arrêter le test et choisissez Lire sous Exemple enregistré pour entendre à quoi il ressemble. 4. Exécutez l’utilitaire de résolution des problèmes d’enregistrement audio. Sélectionnez Paramètres>du son système>. Faites défiler vers le bas jusqu’à Avancé et choisissez Périphériques de sortie ou Périphériques d’entrée sous Résoudre les problèmes de son courants. Sélectionnez Tous les périphériques audio sous Avancé pour des options supplémentaires. Windows ne détecte pas le casque, l’appareil photo ou le microphone Si les étapes précédentes de résolution des problèmes ne résolvent pas le problème et que Windows ne détecte même pas […] »
- **[S2]** DOC020 — Périphérique de sortie audio non détecté dans Windows (page 1) : « Solution 1 : Vérifier les périphériques audio dans le Gestionnaire de périphériques Assurez-vous que le périphérique audio est activé et détecté. 1. Sélectionnez Démarrer, tapez Gestionnaire de périphériques, puis sélectionnez-le dans les résultats. 2. Développez Contrôleurs audio, vidéo et jeu. 3. Si votre périphérique audio s’affiche : Appuyez longuement (ou cliquez avec le bouton droit) sur l’appareil, puis sélectionnez Activer l’appareil s’il est disponible. 4. Si vous ne voyez pas le périphérique audio : Sélectionnez Afficher>Afficher les périphériques cachés. Sélectionnez l’analyse d’action>pour les modifications matérielles. Solution […] »
- **[S3]** DOC010 — Résoudre les problèmes de son ou audio dans Windows (page 5) : « 1. Dans la zone de recherche de la barre des tâches, tapez gestionnaire de périphériques, puis sélectionnez celui-ci dans les résultats. 2. Sélectionnez la flèche en regard de Contrôleurs audio, vidéo et jeu pour développer cette section. 3. Sélectionnez et maintenez enfoncée (ou cliquez avec le bouton droit) la liste de votre carte audio ou périphérique audio, par exemple un casque ou des haut-parleurs, sélectionnez Mettre à jour le pilote, puis sélectionnez Rechercher automatiquement les pilotes. Suivez les instructions qui s’affichent à l’écran pour effectuer la mise à jour. Si Windows ne trouve pas de nouveau pilote, recherchez-en un sur […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 14/40 — F014 (PER01, en)

**Question :** No audio from my laptop after the last update.

**Guides attendus :** DOC010 (Résoudre les problèmes de son ou audio dans Windows); DOC012 (Mettre à jour les pilotes audio dans Windows)

**Réponse de FixIT :**

> Laptop has no audio after the latest Windows update.
> 1. Open Device Manager, expand "Audio, video and game controllers". If the audio device is listed, right‑click it and choose "Enable device". If it’s not visible, go to View > Show hidden devices and then enable it. [S1]
> 2. Right‑click the audio device and select "Update driver" → "Search automatically for drivers". Follow the prompts and restart the PC when finished. [S2]
> 3. If audio still doesn’t work, uninstall the audio driver from Device Manager, then download and install the latest driver from the laptop or audio‑card manufacturer’s website and restart the PC. [S3]
> If the problem persists after these checks, you can open a ticket so that a technician can take over.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC020 — Périphérique de sortie audio non détecté dans Windows (page 1) : « Solution 1 : Vérifier les périphériques audio dans le Gestionnaire de périphériques Assurez-vous que le périphérique audio est activé et détecté. 1. Sélectionnez Démarrer, tapez Gestionnaire de périphériques, puis sélectionnez-le dans les résultats. 2. Développez Contrôleurs audio, vidéo et jeu. 3. Si votre périphérique audio s’affiche : Appuyez longuement (ou cliquez avec le bouton droit) sur l’appareil, puis sélectionnez Activer l’appareil s’il est disponible. 4. Si vous ne voyez pas le périphérique audio : Sélectionnez Afficher>Afficher les périphériques cachés. Sélectionnez l’analyse d’action>pour les modifications matérielles. Solution […] »
- **[S2]** DOC012 — Mettre à jour les pilotes audio dans Windows (page 1) : « Mettre à jour les pilotes audio à l’aide du Gestionnaire de périphériques Si Windows Update n’installe pas de pilote audio plus récent, vous pouvez case activée manuellement. 1. Sélectionnez Démarrer, tapez Gestionnaire de périphériques, puis sélectionnez Gestionnaire de périphériques. 2. Développez Contrôleurs audio, vidéo et jeu. 3. Cliquez avec le bouton droit sur votre périphérique audio, puis sélectionnez Mettre à jour le pilote. 4. Sélectionnez Rechercher automatiquement les pilotes. 5. Suivez les instructions à l’écran. 6. Redémarrez votre PC une fois la mise à jour terminée. Si Windows signale que le meilleur pilote est déjà […] »
- **[S3]** DOC012 — Mettre à jour les pilotes audio dans Windows (page 2) : « 3. Téléchargez le dernier pilote audio pour Windows 11. 4. Installez le pilote en suivant les instructions du fabricant. 5. Redémarrez votre PC. Si les problèmes de son persistent après la mise à jour de vos pilotes audio, essayez les étapes de dépannage supplémentaires dans Résoudre les problèmes de son ou audio dans Windows. »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 15/40 — F015 (PER01, fr)

**Question :** Windows ne détecte plus mes haut-parleurs.

**Guides attendus :** DOC020 (Périphérique de sortie audio non détecté dans Windows); DOC010 (Résoudre les problèmes de son ou audio dans Windows)

**Réponse de FixIT :**

> Windows ne détecte plus les haut-parleurs connectés à l’ordinateur.
> 1. Vérifiez que les haut-parleurs ne sont pas en mode muet et qu’ils sont sélectionnés comme sortie audio dans les paramètres de son (icône haut-parleurs → liste des périphériques audio). [S1]
> 2. Ouvrez le Gestionnaire de périphériques, développez « Contrôleurs audio, vidéo et jeu » et assurez‑vous que le contrôleur audio est activé et visible. Si le périphérique est désactivé, activez‑le. [S3]
> 3. Si le périphérique audio n’apparaît pas, désinstallez le pilote actuel via le Gestionnaire de périphériques, puis téléchargez et installez le dernier pilote audio depuis le site du fabricant. Redémarrez l’ordinateur après l’installation. [S3]
> 4. Exécutez l’utilitaire de résolution des problèmes audio (Paramètres > Son > Résoudre les problèmes) pour détecter et corriger automatiquement les problèmes de son. [S2]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC010 — Résoudre les problèmes de son ou audio dans Windows (page 3) : « Étape 5. Vérifier les paramètres de son Vérifiez que vos périphériques audio ne sont pas en mode muet et qu’ils n’ont pas été désactivés. 1. Sélectionnez et maintenez enfoncée (ou cliquez avec le bouton droit) l’icône Haut-parleurs dans la barre des tâches. 2. Ensuite, sélectionnez la flèche à droite du curseur de volume du haut-parleur pour ouvrir la liste des périphériques audio connectés à votre ordinateur. L’info-bulle doit s’afficher sous la forme Sélectionnez une sortie audio lorsque vous pointez sur la flèche. Remarque Si vous ne voyez pas les haut-parleurs affichés, il se trouve peut-être dans la zone de dépassement. Sélectionnez […] »
- **[S2]** DOC011 — Résoudre les problèmes de microphone dans Windows (page 2) : « Sélectionnez Arrêter le test et choisissez Lire sous Exemple enregistré pour entendre à quoi il ressemble. 4. Exécutez l’utilitaire de résolution des problèmes d’enregistrement audio. Sélectionnez Paramètres>du son système>. Faites défiler vers le bas jusqu’à Avancé et choisissez Périphériques de sortie ou Périphériques d’entrée sous Résoudre les problèmes de son courants. Sélectionnez Tous les périphériques audio sous Avancé pour des options supplémentaires. Windows ne détecte pas le casque, l’appareil photo ou le microphone Si les étapes précédentes de résolution des problèmes ne résolvent pas le problème et que Windows ne détecte même pas […] »
- **[S3]** DOC020 — Périphérique de sortie audio non détecté dans Windows (page 1) : « Solution 1 : Vérifier les périphériques audio dans le Gestionnaire de périphériques Assurez-vous que le périphérique audio est activé et détecté. 1. Sélectionnez Démarrer, tapez Gestionnaire de périphériques, puis sélectionnez-le dans les résultats. 2. Développez Contrôleurs audio, vidéo et jeu. 3. Si votre périphérique audio s’affiche : Appuyez longuement (ou cliquez avec le bouton droit) sur l’appareil, puis sélectionnez Activer l’appareil s’il est disponible. 4. Si vous ne voyez pas le périphérique audio : Sélectionnez Afficher>Afficher les périphériques cachés. Sélectionnez l’analyse d’action>pour les modifications matérielles. Solution […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 16/40 — F016 (PER01, en)

**Question :** How do I reinstall my audio driver on Windows?

**Guides attendus :** DOC012 (Mettre à jour les pilotes audio dans Windows); DOC010 (Résoudre les problèmes de son ou audio dans Windows)

**Réponse de FixIT :**

> User wants to reinstall the audio driver on Windows.
> 1. Open Device Manager by pressing Win+X and selecting Device Manager or by typing "Device Manager" in the Start menu. [S2]
> 2. Expand the "Audio, video and game controllers" section. [S2]
> 3. Right‑click the audio device, choose "Uninstall device", check the box to delete the driver software if available, and confirm the uninstallation. [S1]
> 4. Restart the computer; Windows will automatically reinstall the audio driver. If it does not, open Device Manager again, right‑click the section header, and select "Scan for hardware changes". [S1]

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC011 — Résoudre les problèmes de microphone dans Windows (page 2) : « 2. Élargir la section Contrôleurs audio, vidéo et de jeu . 3. Recherchez des périphériques ou des pilotes audio. Cliquez avec le bouton droit sur le périphérique audio et sélectionnez Désinstaller le périphérique. Veillez à cocher la case indiquant Tentative de suppression du pilote pour ce périphérique , puis sélectionnez Désinstaller. Répétez cette procédure pour tous les autres périphériques audio. 4. Redémarrez l’ordinateur. Windows tentera de réinstaller automatiquement vos périphériques audio et vos pilotes. Si ce n’est pas le cas, cliquez avec le bouton droit sur le bouton Démarrer et sélectionnez Gestionnaire de périphériques. […] »
- **[S2]** DOC012 — Mettre à jour les pilotes audio dans Windows (page 2) : « 1. Sélectionnez Démarrer, tapez Gestionnaire de périphériques, puis sélectionnez-le dans les résultats. 2. Développez Contrôleurs audio, vidéo et jeu. 3. Cliquez avec le bouton droit sur votre périphérique audio, puis sélectionnez Désinstaller le périphérique. 4. Si vous y êtes invité, confirmez la désinstallation. 5. Redémarrez votre PC. Une fois que votre PC a redémarré, Windows réinstalle automatiquement le pilote audio. Obtenir le dernier pilote audio auprès du fabricant de l’appareil Certains pilotes audio sont fournis directement par le fabricant du PC ou du périphérique audio. Cette option est utile si les problèmes audio sont apparus […] »
- **[S3]** DOC012 — Mettre à jour les pilotes audio dans Windows (page 2) : « 3. Téléchargez le dernier pilote audio pour Windows 11. 4. Installez le pilote en suivant les instructions du fabricant. 5. Redémarrez votre PC. Si les problèmes de son persistent après la mise à jour de vos pilotes audio, essayez les étapes de dépannage supplémentaires dans Résoudre les problèmes de son ou audio dans Windows. »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 17/40 — F017 (PER02, fr)

**Question :** Personne ne m'entend pendant mes réunions en ligne.

**Guides attendus :** DOC011 (Résoudre les problèmes de microphone dans Windows)

**⚠ aucun guide attendu n'est cité ; réponse de type clarification alors que la question est répondable**

**Réponse de FixIT :**

> Quel logiciel utilisez-vous pour les réunions?

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « 2. Sous l’onglet Support, sous View common issues, cliquez sur Get started. 3. Développez I want to troubleshoot my PC, puis I’m having connectivity issues et cliquez sur I can’t connect to WiFi. 4. Cliquez sur le bouton Run now pour laisser SupportAssist exécuter une réparation automatisée du Wi-Fi. Si la réparation automatisée SupportAssist n’a pas résolu le problème Wi-Fi, passez à l’étape suivante. »
- **[S2]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 2) : « - Vérifiez l’état de votre réseau. Si vous êtes déconnecté, reconnectez-vous à votre réseau Wi-Fi ou Ethernet. Pour plus d’informations, voir Résoudre Wi-Fi problèmes de connexion dans Windows. Étape 3. Vérifiez que vous disposez d’un accès administrateur Certaines mises à jour nécessitent un accès administrateur. Si votre compte ne dispose pas d’un accès administrateur, consultez la section Créer un compte utilisateur local ou un compte administrateur dans Windows. Vous pouvez également demander à une personne de votre famille, ou de votre entreprise, qui possède un compte administrateur d’installer les mises à jour. Étape 4. Déconnecter le […] »
- **[S3]** DOC026 — Résoudre les problèmes de connexion d'un moniteur externe (page 3) : « Vous avez encore des problèmes ? Si vous avez essayé les procédures décrites dans cet article ou que vous ne savez pas comment résoudre le problème, utilisez le Hub de commentaires Windows pou entrer un bogue. Incluez des détails sur ce que vous faisiez ou les mesures spécifiques que vous preniez lors de la survenue du problème. Connectez-vous au hub de commentaires et suivez les instructions pour résumer et décrire votre problème. Ensuite, sélectionnez votre catégorie, puis ajouter suffisamment d’informations supplémentaires pour recréer le problème. Vos informations permettent à Microsoft de déterminer la cause principale de ce problème. »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 18/40 — F018 (PER02, en)

**Question :** My headset mic is not picked up by Windows.

**Guides attendus :** DOC011 (Résoudre les problèmes de microphone dans Windows)

**Réponse de FixIT :**

> Le microphone du casque n’est pas détecté par Windows.
> 1. Vérifiez que les applications ont accès au microphone : Démarrer > Paramètres > Confidentialité & sécurité > Microphone, assurez‑vous que l’accès est activé et que les applications sont autorisées. [S2]
> 2. Ouvrez le Gestionnaire de périphériques, développez Contrôleurs audio, vidéo et jeu, vérifiez que le périphérique audio est activé. Si non, faites un clic droit et choisissez Activer l’appareil. [S3]
> 3. Exécutez l’utilitaire de résolution des problèmes d’enregistrement audio : Paramètres > Son > Résoudre les problèmes de son courants, sélectionnez Tous les périphériques audio. [S1]
> 4. Réinstallez les pilotes audio : Gestionnaire de périphériques > Contrôleurs audio, vidéo et jeu, faites un clic droit sur le périphérique, choisissez Désinstaller, puis redémarrez et laissez Windows réinstaller le pilote. [S1]

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC011 — Résoudre les problèmes de microphone dans Windows (page 2) : « Sélectionnez Arrêter le test et choisissez Lire sous Exemple enregistré pour entendre à quoi il ressemble. 4. Exécutez l’utilitaire de résolution des problèmes d’enregistrement audio. Sélectionnez Paramètres>du son système>. Faites défiler vers le bas jusqu’à Avancé et choisissez Périphériques de sortie ou Périphériques d’entrée sous Résoudre les problèmes de son courants. Sélectionnez Tous les périphériques audio sous Avancé pour des options supplémentaires. Windows ne détecte pas le casque, l’appareil photo ou le microphone Si les étapes précédentes de résolution des problèmes ne résolvent pas le problème et que Windows ne détecte même pas […] »
- **[S2]** DOC011 — Résoudre les problèmes de microphone dans Windows (page 1) : « Si vous rencontrez des problèmes avec les fonctions de votre microphone ou avec le microphone de votre casque ou de votre webcam, les informations suivantes peuvent vous aider à résoudre des problèmes. Vérifier que les applications ont accès au microphone Si votre microphone n’est pas détecté après la mise à jour de Windows 11, vous devrez peut-être accorder à vos applications l’autorisation de l’utiliser. Voici comment procéder : 1. Sélectionnez Démarrer>Paramètres>Confidentialité & sécurité>Microphone et assurez-vous que l’accès au microphone est activé. 2. Assurez-vous que l’option Autoriser les applications à accéder à votre microphone […] »
- **[S3]** DOC020 — Périphérique de sortie audio non détecté dans Windows (page 1) : « Solution 1 : Vérifier les périphériques audio dans le Gestionnaire de périphériques Assurez-vous que le périphérique audio est activé et détecté. 1. Sélectionnez Démarrer, tapez Gestionnaire de périphériques, puis sélectionnez-le dans les résultats. 2. Développez Contrôleurs audio, vidéo et jeu. 3. Si votre périphérique audio s’affiche : Appuyez longuement (ou cliquez avec le bouton droit) sur l’appareil, puis sélectionnez Activer l’appareil s’il est disponible. 4. Si vous ne voyez pas le périphérique audio : Sélectionnez Afficher>Afficher les périphériques cachés. Sélectionnez l’analyse d’action>pour les modifications matérielles. Solution […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 19/40 — F019 (PER02, fr)

**Question :** Comment autoriser le microphone pour une application ?

**Guides attendus :** DOC011 (Résoudre les problèmes de microphone dans Windows)

**Réponse de FixIT :**

> Vous souhaitez autoriser l'accès au microphone pour une application sur Windows 11.
> 1. Ouvrez Paramètres > Confidentialité & sécurité > Microphone et assurez‑vous que l’accès au microphone est activé. [S1]
> 2. Activez l’option « Autoriser les applications à accéder à votre microphone » et activez le bouton bascule à côté de l’application concernée. [S2]
> 3. Pour les applications de bureau, activez « Autoriser les applications de bureau à accéder à votre microphone » dans la même section. [S1]
> 4. Si votre microphone est intégré à une caméra, vérifiez également que la caméra est activée dans Paramètres > Confidentialité & sécurité > Caméra. [S3]

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC011 — Résoudre les problèmes de microphone dans Windows (page 1) : « Si vous rencontrez des problèmes avec les fonctions de votre microphone ou avec le microphone de votre casque ou de votre webcam, les informations suivantes peuvent vous aider à résoudre des problèmes. Vérifier que les applications ont accès au microphone Si votre microphone n’est pas détecté après la mise à jour de Windows 11, vous devrez peut-être accorder à vos applications l’autorisation de l’utiliser. Voici comment procéder : 1. Sélectionnez Démarrer>Paramètres>Confidentialité & sécurité>Microphone et assurez-vous que l’accès au microphone est activé. 2. Assurez-vous que l’option Autoriser les applications à accéder à votre microphone […] »
- **[S2]** DOC010 — Résoudre les problèmes de son ou audio dans Windows (page 7) : « 3. Assurez-vous que les bascules Accès au microphone et Permettre aux applications d’accéder à votre microphone sont activées. 4. Si vous rencontrez ce problème avec une application spécifique, faites défiler vers le bas sous Autoriser les applications à accéder à votre microphone et assurez-vous que le bouton bascule en regard de cette application spécifique est également activé . »
- **[S3]** DOC011 — Résoudre les problèmes de microphone dans Windows (page 1) : « applications de bureau à accéder à votre microphone est activée. Vous ne pouvez pas désactiver l’accès au microphone pour les applications individuelles. Si votre caméra contient un microphone, vous devrez peut-être également autoriser vos applications à utiliser cette caméra. Si c’est le cas, sélectionnez Démarrer>Paramètres>Confidentialité & sécurité>Caméra et assurez-vous que la Caméra est activée. Les autres ne m’entendent pas Essayez les solutions suivantes : 1. Si votre casque est équipé d’un bouton de désactivation du son, vérifiez qu’il n’est pas activé. 2. Assurez-vous que votre microphone ou votre casque est correctement connecté à […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 20/40 — F020 (PER02, en)

**Question :** Windows does not detect my microphone at all.

**Guides attendus :** DOC011 (Résoudre les problèmes de microphone dans Windows)

**Réponse de FixIT :**

> The user reports that Windows 11 does not detect their microphone.
> 1. Open Settings → Privacy & Security → Microphone and ensure microphone access is turned on, and that the option to allow desktop apps to access the microphone is enabled. [S1]
> 2. Run the built‑in audio troubleshooter: Settings → System → Sound → Advanced → Troubleshoot audio problems, and follow the prompts. [S2]
> 3. Set the microphone as the default input device: Settings → System → Sound → Input, choose the microphone, then click "Set as default". [S3]
> 4. If the microphone still isn’t detected, reinstall the audio drivers: right‑click Start → Device Manager, expand Audio, video and game controllers, right‑click the audio device, and choose Uninstall device, then restart the PC to let Windows reinstall the driver. [S2]
> If the problem persists after these checks, you can open a ticket so that a technician can take over.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC011 — Résoudre les problèmes de microphone dans Windows (page 1) : « Si vous rencontrez des problèmes avec les fonctions de votre microphone ou avec le microphone de votre casque ou de votre webcam, les informations suivantes peuvent vous aider à résoudre des problèmes. Vérifier que les applications ont accès au microphone Si votre microphone n’est pas détecté après la mise à jour de Windows 11, vous devrez peut-être accorder à vos applications l’autorisation de l’utiliser. Voici comment procéder : 1. Sélectionnez Démarrer>Paramètres>Confidentialité & sécurité>Microphone et assurez-vous que l’accès au microphone est activé. 2. Assurez-vous que l’option Autoriser les applications à accéder à votre microphone […] »
- **[S2]** DOC011 — Résoudre les problèmes de microphone dans Windows (page 2) : « Sélectionnez Arrêter le test et choisissez Lire sous Exemple enregistré pour entendre à quoi il ressemble. 4. Exécutez l’utilitaire de résolution des problèmes d’enregistrement audio. Sélectionnez Paramètres>du son système>. Faites défiler vers le bas jusqu’à Avancé et choisissez Périphériques de sortie ou Périphériques d’entrée sous Résoudre les problèmes de son courants. Sélectionnez Tous les périphériques audio sous Avancé pour des options supplémentaires. Windows ne détecte pas le casque, l’appareil photo ou le microphone Si les étapes précédentes de résolution des problèmes ne résolvent pas le problème et que Windows ne détecte même pas […] »
- **[S3]** DOC011 — Résoudre les problèmes de microphone dans Windows (page 1) : « 3. Vérifiez que votre microphone ou votre casque est configuré comme périphérique d’enregistrement par défaut pour le système. Voici comment faire dans Windows 11 : Sélectionnez Démarrer>Paramètres>du son système>. Dans Entrée, accédez à Choisir un appareil pour parler ou enregistrer , puis sélectionnez l’appareil à utiliser. Pour tester votre microphone, sélectionnez > à droite de l’appareil. Dans la page des propriétés, sélectionnez Démarrer le test sous Test du microphone et parlez dans le microphone. »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 21/40 — F021 (PER03, fr)

**Question :** Mon clavier externe ne répond plus après la mise en veille.

**Guides attendus :** DOC013 (Résoudre les problèmes de clavier et de souris dans Windows)

**Réponse de FixIT :**

> Clavier externe ne répond plus après mise en veille
> 1. Connectez le clavier à un autre ordinateur pour vérifier s’il fonctionne. Si le clavier ne fonctionne pas sur l’autre PC, il est probablement défectueux. [S1]
> 2. Assurez-vous que le pilote du clavier est correctement installé. Si le pilote est absent ou obsolète, installez le pilote approprié. [S1]
> 3. Mettez à jour le pilote via Windows Update : recherchez les mises à jour dans la barre des tâches, puis sélectionnez « Rechercher les mises à jour ». [S1]

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC013 — Résoudre les problèmes de clavier et de souris dans Windows (page 2) : « Vérifier si la souris et le clavier fonctionnent Si le périphérique ne semble pas marcher du tout (aucun voyant ne s’allume sur le périphérique quand il est connecté ou le curseur reste immobile ou n’apparaît pas à l’écran), connectez le périphérique à un autre PC pour vérifier s’il fonctionne sur ce PC. Si le périphérique ne fonctionne pas sur l’autre PC, vous devrez peut-être le remplacer. Remarque Certains périphériques ont besoin qu’un pilote soit installé pour fonctionner. Quand vous testez le périphérique sur un autre PC, assurez-vous que le pilote correct est installé pour le périphérique. Mettre à jour un pilote de périphérique à […] »
- **[S2]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « 2. Sous l’onglet Support, sous View common issues, cliquez sur Get started. 3. Développez I want to troubleshoot my PC, puis I’m having connectivity issues et cliquez sur I can’t connect to WiFi. 4. Cliquez sur le bouton Run now pour laisser SupportAssist exécuter une réparation automatisée du Wi-Fi. Si la réparation automatisée SupportAssist n’a pas résolu le problème Wi-Fi, passez à l’étape suivante. »
- **[S3]** DOC026 — Résoudre les problèmes de connexion d'un moniteur externe (page 2) : « Si votre installation fonctionnait bien, puis s’est soudainement arrêtée, voici quelques solutions que vous pouvez essayer. Essayez une séquence de touches Windows Dans certains cas, appuyez sur Touche de logo Windows + Ctrl + Maj + B pour réinitialiser votre pilote graphique peut résoudre votre problème. Si cela ne fonctionne pas, consultez la rubrique redémarrage vous aide. Redémarrer votre appareil Pour redémarrer votre appareil, sélectionnez Démarrer, puisRedémarraged’alimentation>. Si cela ne fonctionne pas, sélectionnez Démarrer, puis sélectionnezArrêtd’alimentation>. Ensuite, rallumez votre appareil. Restaurer votre pilote vidéo Si […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 22/40 — F022 (PER03, en)

**Question :** My touchpad stopped working on my laptop.

**Guides attendus :** DOC016 (Résoudre les problèmes de pavé tactile dans Windows); DOC013 (Résoudre les problèmes de clavier et de souris dans Windows)

**⚠ aucun guide attendu n'est cité ; réponse de type repli alors que la question est répondable**

**Réponse de FixIT :**

> The available guides do not contain enough information to answer.
> If the problem persists after these checks, you can open a ticket so that a technician can take over.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC026 — Résoudre les problèmes de connexion d'un moniteur externe (page 2) : « Si votre installation fonctionnait bien, puis s’est soudainement arrêtée, voici quelques solutions que vous pouvez essayer. Essayez une séquence de touches Windows Dans certains cas, appuyez sur Touche de logo Windows + Ctrl + Maj + B pour réinitialiser votre pilote graphique peut résoudre votre problème. Si cela ne fonctionne pas, consultez la rubrique redémarrage vous aide. Redémarrer votre appareil Pour redémarrer votre appareil, sélectionnez Démarrer, puisRedémarraged’alimentation>. Si cela ne fonctionne pas, sélectionnez Démarrer, puis sélectionnezArrêtd’alimentation>. Ensuite, rallumez votre appareil. Restaurer votre pilote vidéo Si […] »
- **[S2]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « 2. Sous l’onglet Support, sous View common issues, cliquez sur Get started. 3. Développez I want to troubleshoot my PC, puis I’m having connectivity issues et cliquez sur I can’t connect to WiFi. 4. Cliquez sur le bouton Run now pour laisser SupportAssist exécuter une réparation automatisée du Wi-Fi. Si la réparation automatisée SupportAssist n’a pas résolu le problème Wi-Fi, passez à l’étape suivante. »
- **[S3]** DOC026 — Résoudre les problèmes de connexion d'un moniteur externe (page 2) : « développer la section Cartes graphiques . - Cliquez avec le bouton droit sur votre carte graphique, puis sélectionnez Désinstaller le périphérique et Tenter de supprimer le pilote de ce périphérique, puis sélectionnez Désinstaller. »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 23/40 — F023 (PER03, fr)

**Question :** Ma souris Bluetooth n'est pas reconnue par Windows.

**Guides attendus :** DOC024 (Résoudre les problèmes Bluetooth dans Windows); DOC013 (Résoudre les problèmes de clavier et de souris dans Windows)

**Réponse de FixIT :**

> La souris Bluetooth n'est pas reconnue par Windows.
> 1. Redémarrez votre PC pour réinitialiser le matériel Bluetooth. [S1]
> 2. Désactivez puis réactivez le Bluetooth via Paramètres > Bluetooth & appareils. [S3]
> 3. Supprimez la souris Bluetooth dans Paramètres > Bluetooth & appareils > Appareils, puis coupler à nouveau. [S3]
> 4. Exécutez l’utilitaire de résolution des problèmes Bluetooth et mettez à jour les pilotes Bluetooth. [S3]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC018 — Corriger la disparition du Bluetooth (page 1) : « Si l’icône ou la bascule Bluetooth est manquante ou grisée dans les paramètres ou les paramètres rapides, le matériel Bluetooth de votre PC a peut-être rencontré une erreur. Dans ce cas, vous ne pourrez pas activer ou désactiver le Bluetooth, et les périphériques Bluetooth tels que les claviers, les souris et les casques ne pourront pas se connecter à votre PC. Remarque Les erreurs de matériel Bluetooth sont généralement dues à des problèmes liés aux pilotes ou au microprogramme fournis par le fabricant de votre PC. Microsoft vous recommande de contacter le fabricant de votre PC, car il peut avoir des étapes de dépannage spécifiques à votre […] »
- **[S2]** DOC019 — Bluetooth connecté mais sans son (page 1) : « Si votre appareil Bluetooth se connecte à Windows mais que vous n’entendez aucun son, que vous rencontrez une qualité audio médiocre ou que vous faites face à des déconnexions fréquentes, cela peut perturber votre expérience audio. Ce problème se produit souvent en raison de paramètres incorrects, de pilotes obsolètes ou de limitations de compatibilité. Essayez les étapes de dépannage suivantes pour résoudre le problème : Solution 1 : exécuter l’utilitaire de résolution des problèmes Bluetooth automatisé Si vous utilisez un appareil Windows 11, commencez par exécuter l’utilitaire de résolution des problèmes Bluetooth automatisé dans […] »
- **[S3]** DOC024 — Résoudre les problèmes Bluetooth dans Windows (page 2) : « Désactivez le Bluetooth , patientez quelques secondes, puis réactivez-le. - Supprimez le périphérique Bluetooth, puis ajoutez-le à nouveau : Sélectionnez Démarrer>Paramètres Bluetooth>& appareils>Appareils . Dans Appareils, sélectionnez Plus d’options pour l’appareil Bluetooth auquel vous rencontrez des problèmes de connexion, puis sélectionnez Supprimer l’appareil>Oui. Pour en savoir plus sur le couplage de votre appareil Bluetooth, consultez Coupler un appareil Bluetooth. Étape 6. Exécuter l’utilitaire de résolution des problèmes Bluetooth Sélectionnez Démarrer>Paramètres>Système>Résoudreles problèmes >Autres utilitaires de résolution des […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 24/40 — F024 (PER03, en)

**Question :** Some keys on my keyboard are not working in Windows.

**Guides attendus :** DOC013 (Résoudre les problèmes de clavier et de souris dans Windows)

**Réponse de FixIT :**

> Certain keys on the keyboard are unresponsive in Windows.
> 1. Connect the keyboard to another computer to confirm whether the keys work there. If they do not, the keyboard likely has a hardware issue. [S1]
> 2. Update the keyboard driver using Windows Update: open Settings > Windows Update > Check for updates. Install any available driver updates for the keyboard. [S1]
> If the problem persists after these checks, you can open a ticket so that a technician can take over.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC013 — Résoudre les problèmes de clavier et de souris dans Windows (page 2) : « Vérifier si la souris et le clavier fonctionnent Si le périphérique ne semble pas marcher du tout (aucun voyant ne s’allume sur le périphérique quand il est connecté ou le curseur reste immobile ou n’apparaît pas à l’écran), connectez le périphérique à un autre PC pour vérifier s’il fonctionne sur ce PC. Si le périphérique ne fonctionne pas sur l’autre PC, vous devrez peut-être le remplacer. Remarque Certains périphériques ont besoin qu’un pilote soit installé pour fonctionner. Quand vous testez le périphérique sur un autre PC, assurez-vous que le pilote correct est installé pour le périphérique. Mettre à jour un pilote de périphérique à […] »
- **[S2]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 5) : « Si votre appareil est équipé d’un petit disque dur, vous devrez peut-être insérer un lecteur USB pour le mettre à jour. Si votre PC dispose d’un faible espace disque, essayez d’adopter les techniques présentées dans l’article Libérer de l’espace disque dans Windows. Désactiver le VPN : Si vous utilisez un VPN, désactivez-le et réessayez. 0x80070057 ou 0x80080005 : Fichiers endommagés ou configurations système incorrectes Exécution du Vérificateur des fichiers système : Ouvrez l’invite de commandes en tant qu’administrateur et tapez sfc/scannow , puis exécutez. Exécutez l’utilitaire de résolution des problèmes de Windows Update : - […] »
- **[S3]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 6) : « - Mettez à jour votre logiciel antivirus. 0x80070002 : Échec de l’installation de la mise à jour Redémarrez votre PC : Redémarrez votre PC pour vous assurer qu’aucune autre application ne bloque le processus de mise à jour. Exécutez l’utilitaire de résolution des problèmes de Windows Update : - Sélectionnez Démarrer> lesystèmede paramètres>. - Sélectionnez Dépanner et choisissez Autres utilitaires de résolution des problèmes. - Localisez Windows Update et sélectionnez Exécuter. - Suivez les instructions à l’écran pour terminer le processus. Vérifiez l’espace disque : Vérifiez que votre appareil dispose d’un espace disque suffisant. Votre […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 25/40 — F025 (NET01, fr)

**Question :** La liste des réseaux Wi-Fi est vide sur mon portable.

**Guides attendus :** DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows); DOC003 (Dépanner la connexion Wi-Fi sur un PC Dell)

**Réponse de FixIT :**

> La liste des réseaux Wi‑Fi apparaît vide sur votre ordinateur portable.
> 1. Vérifiez que le commutateur Wi‑Fi physique (si votre portable en possède un) est activé. [S1]
> 2. Ouvrez Paramètres > Réseau & Internet et assurez‑vous que le Wi‑Fi est activé. [S1]
> 3. Dans le Gestionnaire de périphériques, développez Cartes réseau, faites un clic droit sur votre adaptateur Wi‑Fi et choisissez « Activer le périphérique » si l’option est grisée. [S2]
> 4. Redémarrez le service « Service de réseau local sans fil » : appuyez sur Win+R, tapez services.msc, trouvez le service, cliquez sur Redémarrer. [S2]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 8) : « Votre carte réseau sans fil est reconnue, mais aucun réseau Wi-Fi n’est trouvé et vous n’êtes pas connecté à Wi-Fi Si vous voyez l’icône Pas de connexion Internet alors que vous êtes à portée de réseaux Wi-Fi, cela peut signifier que : Le commutateur Wi-Fi physique sur votre ordinateur portable ou votre tablette est désactivé. Assurez-vous qu’il est activé. Le Wi-Fi est désactivé dans les paramètres Wi-Fi. Ouvrez Paramètres, puis sélectionnez Réseau & Internet. Assurez-vous que le Wi-Fi est activé. Votre adaptateur ne prend pas en charge la fréquence de diffusion de votre réseau. Par exemple, il se peut que votre carte prenne uniquement en […] »
- **[S2]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 6) : « Désactiver les applications en arrière-plan : Ouvrez le Gestionnaire des tâches (Ctrl + ,Maj + ,Échap). Mettre fin aux processus consommant une bande passante réseau élevée. Tester les performances du routeur : Connectez un autre appareil au Wi-Fi. Si le problème persiste, le routeur peut nécessiter une maintenance ou un remplacement. Wi-Fi option manquante Si l’option de basculement Wi-Fi est manquante ou n’est pas visible dans les paramètres, suivez les étapes de dépannage ci-dessous. Vérifier le commutateur matériel : Certains ordinateurs portables ont un commutateur Wi-Fi physique ; Assurez-vous qu’il est activé. Activer Wi-Fi adaptateur […] »
- **[S3]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 7) : « Si l’appareil se connecte au Wi-Fi, mais qu’Internet n’est pas disponible, suivez les étapes de dépannage ci-dessous. Désactivez le Wi-Fi, réactivez-le et reconnectez-vous à votre réseau sans fil. Renouveler la configuration IP Ouvrez une invite de commandes en tant qu’administrateur. Saisissez ipconfig /release et appuyez sur Entrée. Saisissez ipconfig /renew et appuyez sur Entrée. Vider le cache DNS Ouvrez une invite de commandes en tant qu’administrateur. Tapez ipconfig /flushdns et appuyez sur Entrée. Vérifier les paramètres du proxy Accédez à Paramètres>Réseau & Proxy Internet>. Désactivez tous les paramètres de proxy manuels. Vérifiez […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 26/40 — F026 (NET01, en)

**Question :** No Wi-Fi networks show up in the taskbar.

**Guides attendus :** DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows); DOC003 (Dépanner la connexion Wi-Fi sur un PC Dell)

**⚠ langue attendue en, obtenue fr**

**Réponse de FixIT :**

> Les réseaux Wi‑Fi ne s’affichent pas dans la barre des tâches.
> 1. Vérifiez que le commutateur Wi‑Fi physique (s’il existe) est activé. [S1]
> 2. Ouvrez Paramètres > Réseau & Internet et assurez‑vous que le Wi‑Fi est activé. [S1]
> 3. Dans le Gestionnaire de périphériques, développez Cartes réseau, faites un clic droit sur votre adaptateur Wi‑Fi et choisissez « Activer le périphérique » si nécessaire. [S3]
> 4. Redémarrez le service WLAN AutoConfig : appuyez sur Win+R, tapez services.msc, trouvez « WLAN AutoConfig », faites un clic droit et sélectionnez Redémarrer. [S3]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 8) : « Votre carte réseau sans fil est reconnue, mais aucun réseau Wi-Fi n’est trouvé et vous n’êtes pas connecté à Wi-Fi Si vous voyez l’icône Pas de connexion Internet alors que vous êtes à portée de réseaux Wi-Fi, cela peut signifier que : Le commutateur Wi-Fi physique sur votre ordinateur portable ou votre tablette est désactivé. Assurez-vous qu’il est activé. Le Wi-Fi est désactivé dans les paramètres Wi-Fi. Ouvrez Paramètres, puis sélectionnez Réseau & Internet. Assurez-vous que le Wi-Fi est activé. Votre adaptateur ne prend pas en charge la fréquence de diffusion de votre réseau. Par exemple, il se peut que votre carte prenne uniquement en […] »
- **[S2]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 7) : « Si l’appareil se connecte au Wi-Fi, mais qu’Internet n’est pas disponible, suivez les étapes de dépannage ci-dessous. Désactivez le Wi-Fi, réactivez-le et reconnectez-vous à votre réseau sans fil. Renouveler la configuration IP Ouvrez une invite de commandes en tant qu’administrateur. Saisissez ipconfig /release et appuyez sur Entrée. Saisissez ipconfig /renew et appuyez sur Entrée. Vider le cache DNS Ouvrez une invite de commandes en tant qu’administrateur. Tapez ipconfig /flushdns et appuyez sur Entrée. Vérifier les paramètres du proxy Accédez à Paramètres>Réseau & Proxy Internet>. Désactivez tous les paramètres de proxy manuels. Vérifiez […] »
- **[S3]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 6) : « Désactiver les applications en arrière-plan : Ouvrez le Gestionnaire des tâches (Ctrl + ,Maj + ,Échap). Mettre fin aux processus consommant une bande passante réseau élevée. Tester les performances du routeur : Connectez un autre appareil au Wi-Fi. Si le problème persiste, le routeur peut nécessiter une maintenance ou un remplacement. Wi-Fi option manquante Si l’option de basculement Wi-Fi est manquante ou n’est pas visible dans les paramètres, suivez les étapes de dépannage ci-dessous. Vérifier le commutateur matériel : Certains ordinateurs portables ont un commutateur Wi-Fi physique ; Assurez-vous qu’il est activé. Activer Wi-Fi adaptateur […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 27/40 — F027 (NET01, fr)

**Question :** Mon PC ne détecte pas le Wi-Fi alors que mon téléphone le voit.

**Guides attendus :** DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows); DOC003 (Dépanner la connexion Wi-Fi sur un PC Dell)

**Réponse de FixIT :**

> PC ne détecte pas de réseaux Wi‑Fi alors que le téléphone les voit.
> 1. Vérifiez que le commutateur Wi‑Fi physique de votre ordinateur portable est activé. [S1]
> 2. Ouvrez Paramètres > Réseau & Internet et assurez‑vous que le Wi‑Fi est activé. [S1]
> 3. Assurez‑vous que votre carte réseau prend en charge la bande de fréquence de votre routeur (2,4 GHz ou 5 GHz). [S1]
> 4. Exécutez l’assistance automatisée SupportAssist (Support > View common issues > I can’t connect to Wi‑Fi > Run now) pour rechercher et corriger les problèmes de Wi‑Fi. [S2]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 8) : « Votre carte réseau sans fil est reconnue, mais aucun réseau Wi-Fi n’est trouvé et vous n’êtes pas connecté à Wi-Fi Si vous voyez l’icône Pas de connexion Internet alors que vous êtes à portée de réseaux Wi-Fi, cela peut signifier que : Le commutateur Wi-Fi physique sur votre ordinateur portable ou votre tablette est désactivé. Assurez-vous qu’il est activé. Le Wi-Fi est désactivé dans les paramètres Wi-Fi. Ouvrez Paramètres, puis sélectionnez Réseau & Internet. Assurez-vous que le Wi-Fi est activé. Votre adaptateur ne prend pas en charge la fréquence de diffusion de votre réseau. Par exemple, il se peut que votre carte prenne uniquement en […] »
- **[S2]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « 2. Sous l’onglet Support, sous View common issues, cliquez sur Get started. 3. Développez I want to troubleshoot my PC, puis I’m having connectivity issues et cliquez sur I can’t connect to WiFi. 4. Cliquez sur le bouton Run now pour laisser SupportAssist exécuter une réparation automatisée du Wi-Fi. Si la réparation automatisée SupportAssist n’a pas résolu le problème Wi-Fi, passez à l’étape suivante. »
- **[S3]** DOC045 — Utiliser votre appareil Windows comme point d'accès mobile (page 2) : « - Pour vous connecter sur l’autre appareil, accédez aux paramètres Wi-Fi de cet appareil, recherchez le nom de votre réseau, sélectionnez-le, entrez le mot de passe ou scannez le code QR, puis connectez-vous. - Pour afficher ou gérer des paramètres tels que le mot de passe réseau, ou si vous n’avez pas encore configuré votre point d’accès mobile et que vous devez le faire, faites un clic droit (ou appuyez longuement) sur l’action rapide Point d’accès mobile et sélectionnez Accéder aux paramètres. »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 28/40 — F028 (NET01, en)

**Question :** Windows can't see my home wireless network.

**Guides attendus :** DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows); DOC003 (Dépanner la connexion Wi-Fi sur un PC Dell)

**Réponse de FixIT :**

> Windows cannot detect the home wireless network.
> 1. Run the automated Wi‑Fi repair via SupportAssist: open the Support tab, select "I can’t connect to WiFi", then click "Run now". [S1]
> 2. Open an elevated command prompt and run:
> - ipconfig /release
> - ipconfig /renew
> - ipconfig /flushdns
> Then check that the IP address is not in the 169.254.x.x range. [S2]
> 3. Disable any manual proxy settings: Settings > Network & Internet > Proxy, turn off all manual proxy options. [S2]
> 4. Check that the wireless adapter appears in Device Manager. If it is missing, download and install the latest driver from the manufacturer’s website. [S3]
> If the problem persists after these checks, you can open a ticket so that a technician can take over.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « 2. Sous l’onglet Support, sous View common issues, cliquez sur Get started. 3. Développez I want to troubleshoot my PC, puis I’m having connectivity issues et cliquez sur I can’t connect to WiFi. 4. Cliquez sur le bouton Run now pour laisser SupportAssist exécuter une réparation automatisée du Wi-Fi. Si la réparation automatisée SupportAssist n’a pas résolu le problème Wi-Fi, passez à l’étape suivante. »
- **[S2]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 7) : « Si l’appareil se connecte au Wi-Fi, mais qu’Internet n’est pas disponible, suivez les étapes de dépannage ci-dessous. Désactivez le Wi-Fi, réactivez-le et reconnectez-vous à votre réseau sans fil. Renouveler la configuration IP Ouvrez une invite de commandes en tant qu’administrateur. Saisissez ipconfig /release et appuyez sur Entrée. Saisissez ipconfig /renew et appuyez sur Entrée. Vider le cache DNS Ouvrez une invite de commandes en tant qu’administrateur. Tapez ipconfig /flushdns et appuyez sur Entrée. Vérifier les paramètres du proxy Accédez à Paramètres>Réseau & Proxy Internet>. Désactivez tous les paramètres de proxy manuels. Vérifiez […] »
- **[S3]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 9) : « Si votre carte réseau sans fil n’est pas répertoriée dans le Gestionnaire de périphériques, Windows ne la détecte pas. Dans ce cas, vous devrez peut-être installer le pilote manuellement. Visitez le site web du fabricant de votre appareil pour obtenir un pilote qui fonctionne dans Windows. »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 29/40 — F029 (NET02, fr)

**Question :** Windows refuse mon mot de passe Wi-Fi alors qu'il est correct.

**Guides attendus :** DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows); DOC002 (Se connecter à un réseau Wi-Fi dans Windows); DOC003 (Dépanner la connexion Wi-Fi sur un PC Dell)

**Réponse de FixIT :**

> Windows refuse le mot de passe Wi‑Fi même si celui‑ci est correct.
> 1. Lancez l’assistance SupportAssist et exécutez la réparation automatisée du Wi‑Fi (onglet Support → View common issues → Get started → Run now). [S1]
> 2. Oubliez le réseau Wi‑Fi puis reconnectez‑vous en saisissant à nouveau le mot de passe (icône Wi‑Fi → Gérer les connexions → Oublier → reconnecter). [S3]
> 3. Ouvrez une invite de commandes en tant qu’administrateur et exécutez : ipconfig /release, ipconfig /renew, puis ipconfig /flushdns pour renouveler l’adresse IP et vider le cache DNS. [S2]
> 4. Vérifiez que les paramètres de proxy sont désactivés (Paramètres > Réseau & Proxy Internet) et que votre adresse IP n’est pas 169.254.x.x, indiquant un problème DHCP. [S2]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « 2. Sous l’onglet Support, sous View common issues, cliquez sur Get started. 3. Développez I want to troubleshoot my PC, puis I’m having connectivity issues et cliquez sur I can’t connect to WiFi. 4. Cliquez sur le bouton Run now pour laisser SupportAssist exécuter une réparation automatisée du Wi-Fi. Si la réparation automatisée SupportAssist n’a pas résolu le problème Wi-Fi, passez à l’étape suivante. »
- **[S2]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 7) : « Si l’appareil se connecte au Wi-Fi, mais qu’Internet n’est pas disponible, suivez les étapes de dépannage ci-dessous. Désactivez le Wi-Fi, réactivez-le et reconnectez-vous à votre réseau sans fil. Renouveler la configuration IP Ouvrez une invite de commandes en tant qu’administrateur. Saisissez ipconfig /release et appuyez sur Entrée. Saisissez ipconfig /renew et appuyez sur Entrée. Vider le cache DNS Ouvrez une invite de commandes en tant qu’administrateur. Tapez ipconfig /flushdns et appuyez sur Entrée. Vérifier les paramètres du proxy Accédez à Paramètres>Réseau & Proxy Internet>. Désactivez tous les paramètres de proxy manuels. Vérifiez […] »
- **[S3]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « vérifiez. À l’issue de l’optimisation de SupportAssist, vérifiez si le Wi-Fi fonctionne. Dans le cas contraire, passez à l’étape suivante. Option Oublier et reconnexion au Wi-Fi Si l’optimisation n’a pas été utile, rétablissez une nouvelle connexion à votre réseau sans fil. 1. Dans la barre d’état système, cliquez sur l’icône Wi-Fi et sélectionnez Gérer les connexions Wi-Fi (icône >). 2. Sous Wi-Fi, recherchez le nom de votre réseau. 3. Cliquez sur Oublier. 4. Pour vous reconnecter, sélectionnez le réseau, saisissez le mot de passe, puis cliquez sur Connexion. La reconnexion n’a pas permis de résoudre le problème ? Passons à l’étape […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 30/40 — F030 (NET02, en)

**Question :** I select my Wi-Fi network but it won't connect.

**Guides attendus :** DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows); DOC002 (Se connecter à un réseau Wi-Fi dans Windows); DOC003 (Dépanner la connexion Wi-Fi sur un PC Dell)

**Réponse de FixIT :**

> The user selects a Wi‑Fi network but cannot connect.
> 1. Check that the physical Wi‑Fi switch on your laptop or tablet is enabled and that Wi‑Fi is turned on in Settings > Network & Internet > Wi‑Fi. [S2]
> 2. Run the automated Wi‑Fi repair in SupportAssist: open SupportAssist, go to Support > View common issues > Get started, select I want to troubleshoot my PC, choose I’m having connectivity issues, then I can’t connect to Wi‑Fi, and click Run now. [S1]
> 3. Verify that your Wi‑Fi adapter supports the frequency band of your router (2.4 GHz vs 5 GHz). If your adapter only supports 2.4 GHz, switch the router to 2.4 GHz or use a compatible adapter. [S2]
> If the problem persists after these checks, you can open a ticket so that a technician can take over.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « 2. Sous l’onglet Support, sous View common issues, cliquez sur Get started. 3. Développez I want to troubleshoot my PC, puis I’m having connectivity issues et cliquez sur I can’t connect to WiFi. 4. Cliquez sur le bouton Run now pour laisser SupportAssist exécuter une réparation automatisée du Wi-Fi. Si la réparation automatisée SupportAssist n’a pas résolu le problème Wi-Fi, passez à l’étape suivante. »
- **[S2]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 8) : « Votre carte réseau sans fil est reconnue, mais aucun réseau Wi-Fi n’est trouvé et vous n’êtes pas connecté à Wi-Fi Si vous voyez l’icône Pas de connexion Internet alors que vous êtes à portée de réseaux Wi-Fi, cela peut signifier que : Le commutateur Wi-Fi physique sur votre ordinateur portable ou votre tablette est désactivé. Assurez-vous qu’il est activé. Le Wi-Fi est désactivé dans les paramètres Wi-Fi. Ouvrez Paramètres, puis sélectionnez Réseau & Internet. Assurez-vous que le Wi-Fi est activé. Votre adaptateur ne prend pas en charge la fréquence de diffusion de votre réseau. Par exemple, il se peut que votre carte prenne uniquement en […] »
- **[S3]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 1) : « Suivez ces étapes pour garantir la connectivité : - Sélectionnez Démarrer>les paramètres>Réseau & Internet>Wi-Fi. »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 31/40 — F031 (NET02, fr)

**Question :** Comment oublier puis reconnecter un réseau Wi-Fi ?

**Guides attendus :** DOC002 (Se connecter à un réseau Wi-Fi dans Windows); DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows)

**Réponse de FixIT :**

> Vous souhaitez oublier puis reconnecter un réseau Wi‑Fi sur Windows 11.
> 1. Ouvrez Paramètres > Réseau & Internet > Wi‑Fi > Gérer les réseaux connus. Sélectionnez votre réseau et cliquez sur Oublier. [S1]
> 2. Sélectionnez à nouveau le réseau dans la liste des réseaux disponibles et entrez le mot de passe pour vous reconnecter. [S1]
> 3. Si la connexion ne fonctionne toujours pas, redémarrez votre modem et votre routeur en suivant les instructions de l’extrait 2. [S2]

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 2) : « Vérifiez si le nom de votre réseau affiche Connecté au-dessous. S’il affiche une status autre que Connecté, sélectionnez un réseau Wi-Fi que vous reconnaissez dans la liste des réseaux disponibles. Ensuite, cliquez sur le réseau et essayez de vous connecter. Étape 2. Vérifier le mode Avion Accédez à Paramètres>Réseau & Internet>Mode avion. Assurez-vous que le mode Avion est désactivé. Étape 3. Oubliez et reconnectez-vous au réseau Wi-Fi Dans l’ application des paramètres de votre appareil Windows sélectionnez Réseau & Internet>Wi-Fi, puis sélectionnez Gérer les réseaux connus. Sélectionnez votre réseau Wi-Fi et cliquez sur Oublier. […] »
- **[S2]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 2) : « Lorsque vous effectuez cette opération, toutes les personnes connectées à votre réseau Wi-Fi sont temporairement déconnectées. Les étapes à suivre pour redémarrer votre modem et votre routeur peuvent varier, mais voici les étapes générales. Remarque Si vous disposez d'un appareil combiné modem-câble/routeur Wi-Fi, vous ne devez suivre que les étapes relatives à l'appareil unique. Débranchez le câble d’alimentation du routeur de la source d’alimentation. Débranchez le câble d’alimentation du modem de la source d’alimentation. Certains modems sont dotés d’une batterie de secours. Si vous débranchez le modem et que les lumières restent […] »
- **[S3]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 3) : « Étape 5. Ajustez Wi-Fi canal et la fréquence Essayez de vous connecter à un réseau sur une autre bande de fréquence. De nombreux routeurs Wi-Fi grand public diffusent sur deux bandes de fréquence réseau différentes : 2,4 GHz et 5 GHz. Ceux-ci s’affichent en tant que réseaux distincts dans la liste des réseaux Wi-Fi disponibles. Si votre liste de réseaux Wi-Fi disponibles comprend à la fois un réseau 2,4 GHz et un réseau 5 GHz, essayez de vous connecter à l’autre réseau. Pour en savoir plus, consultez la case activée Wi-Fi et l’aménagement de votre maison. Étape 6. Essayez de vous connecter au même réseau sur un autre appareil Sur un autre […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 32/40 — F032 (NET02, en)

**Question :** Connecting to Wi-Fi shows a 'can't connect to this network' error.

**Guides attendus :** DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows); DOC003 (Dépanner la connexion Wi-Fi sur un PC Dell)

**⚠ langue attendue en, obtenue fr**

**Réponse de FixIT :**

> L’utilisateur ne parvient pas à se connecter à un réseau Wi‑Fi et reçoit l’erreur « can't connect to this network ».
> 1. Ouvrez SupportAssist, allez dans l’onglet Support, cliquez sur View common issues, puis Get started. Sous I want to troubleshoot my PC, choisissez I'm having connectivity issues, puis I can’t connect to WiFi, et cliquez sur Run now. [S1]
> 2. Dans la barre d’état système, cliquez sur l’icône Wi‑Fi, sélectionnez Gérer les connexions Wi‑Fi, trouvez votre réseau, cliquez sur Oublier, puis reconnectez en saisissant le mot de passe. [S2]
> 3. Ouvrez une invite de commandes en tant qu’administrateur, exécutez ipconfig /release, puis ipconfig /renew, et ipconfig /flushdns. [S3]
> 4. Accédez à Paramètres > Réseau & Proxy Internet, désactivez les paramètres de proxy manuels, vérifiez votre adresse IP pour vous assurer qu’elle n’est pas 169.254.x.x. [S3]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « 2. Sous l’onglet Support, sous View common issues, cliquez sur Get started. 3. Développez I want to troubleshoot my PC, puis I’m having connectivity issues et cliquez sur I can’t connect to WiFi. 4. Cliquez sur le bouton Run now pour laisser SupportAssist exécuter une réparation automatisée du Wi-Fi. Si la réparation automatisée SupportAssist n’a pas résolu le problème Wi-Fi, passez à l’étape suivante. »
- **[S2]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « vérifiez. À l’issue de l’optimisation de SupportAssist, vérifiez si le Wi-Fi fonctionne. Dans le cas contraire, passez à l’étape suivante. Option Oublier et reconnexion au Wi-Fi Si l’optimisation n’a pas été utile, rétablissez une nouvelle connexion à votre réseau sans fil. 1. Dans la barre d’état système, cliquez sur l’icône Wi-Fi et sélectionnez Gérer les connexions Wi-Fi (icône >). 2. Sous Wi-Fi, recherchez le nom de votre réseau. 3. Cliquez sur Oublier. 4. Pour vous reconnecter, sélectionnez le réseau, saisissez le mot de passe, puis cliquez sur Connexion. La reconnexion n’a pas permis de résoudre le problème ? Passons à l’étape […] »
- **[S3]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 7) : « Si l’appareil se connecte au Wi-Fi, mais qu’Internet n’est pas disponible, suivez les étapes de dépannage ci-dessous. Désactivez le Wi-Fi, réactivez-le et reconnectez-vous à votre réseau sans fil. Renouveler la configuration IP Ouvrez une invite de commandes en tant qu’administrateur. Saisissez ipconfig /release et appuyez sur Entrée. Saisissez ipconfig /renew et appuyez sur Entrée. Vider le cache DNS Ouvrez une invite de commandes en tant qu’administrateur. Tapez ipconfig /flushdns et appuyez sur Entrée. Vérifier les paramètres du proxy Accédez à Paramètres>Réseau & Proxy Internet>. Désactivez tous les paramètres de proxy manuels. Vérifiez […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 33/40 — F033 (NET03, fr)

**Question :** Mon Wi-Fi se déconnecte toutes les cinq minutes.

**Guides attendus :** DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows); DOC003 (Dépanner la connexion Wi-Fi sur un PC Dell)

**Réponse de FixIT :**

> Votre connexion Wi‑Fi se déconnecte toutes les cinq minutes.
> 1. Vérifiez que le commutateur Wi‑Fi physique de votre ordinateur et le paramètre Wi‑Fi dans les paramètres système sont activés. [S1]
> 2. Ouvrez Paramètres > Réseau & Internet > Wi‑Fi pour vous assurer que le Wi‑Fi est bien activé. [S2]
> 3. Essayez de vous connecter à la bande 2,4 GHz au lieu de 5 GHz, ou changez de canal sur votre routeur pour éviter les interférences. [S3]
> 4. Testez la connexion sur un autre appareil ; si le problème ne se produit que sur votre PC, exécutez les commandes réseau pour réinitialiser la pile TCP/IP. [S3]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 8) : « Votre carte réseau sans fil est reconnue, mais aucun réseau Wi-Fi n’est trouvé et vous n’êtes pas connecté à Wi-Fi Si vous voyez l’icône Pas de connexion Internet alors que vous êtes à portée de réseaux Wi-Fi, cela peut signifier que : Le commutateur Wi-Fi physique sur votre ordinateur portable ou votre tablette est désactivé. Assurez-vous qu’il est activé. Le Wi-Fi est désactivé dans les paramètres Wi-Fi. Ouvrez Paramètres, puis sélectionnez Réseau & Internet. Assurez-vous que le Wi-Fi est activé. Votre adaptateur ne prend pas en charge la fréquence de diffusion de votre réseau. Par exemple, il se peut que votre carte prenne uniquement en […] »
- **[S2]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 1) : « Suivez ces étapes pour garantir la connectivité : - Sélectionnez Démarrer>les paramètres>Réseau & Internet>Wi-Fi. »
- **[S3]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 3) : « Étape 5. Ajustez Wi-Fi canal et la fréquence Essayez de vous connecter à un réseau sur une autre bande de fréquence. De nombreux routeurs Wi-Fi grand public diffusent sur deux bandes de fréquence réseau différentes : 2,4 GHz et 5 GHz. Ceux-ci s’affichent en tant que réseaux distincts dans la liste des réseaux Wi-Fi disponibles. Si votre liste de réseaux Wi-Fi disponibles comprend à la fois un réseau 2,4 GHz et un réseau 5 GHz, essayez de vous connecter à l’autre réseau. Pour en savoir plus, consultez la case activée Wi-Fi et l’aménagement de votre maison. Étape 6. Essayez de vous connecter au même réseau sur un autre appareil Sur un autre […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 34/40 — F034 (NET03, en)

**Question :** My Wi-Fi keeps dropping randomly throughout the day.

**Guides attendus :** DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows); DOC003 (Dépanner la connexion Wi-Fi sur un PC Dell)

**Réponse de FixIT :**

> Your Wi‑Fi connection drops intermittently throughout the day.
> 1. Turn Wi‑Fi off, then on again, and reconnect to your network. [S1]
> 2. Open an elevated command prompt and run `ipconfig /release` followed by `ipconfig /renew`, then `ipconfig /flushdns` to refresh your IP and DNS settings. [S1]
> 3. Check that no manual proxy is enabled by going to Settings > Network & Internet > Proxy and disabling any proxy settings. [S1]
> 4. Run the SupportAssist Wi‑Fi repair tool: open SupportAssist, navigate to the Support tab, select "I’m having connectivity issues" → "I can’t connect to Wi‑Fi", then click "Run now" to let it perform an automated fix. [S2]
> If the problem persists after these checks, you can open a ticket so that a technician can take over.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 7) : « Si l’appareil se connecte au Wi-Fi, mais qu’Internet n’est pas disponible, suivez les étapes de dépannage ci-dessous. Désactivez le Wi-Fi, réactivez-le et reconnectez-vous à votre réseau sans fil. Renouveler la configuration IP Ouvrez une invite de commandes en tant qu’administrateur. Saisissez ipconfig /release et appuyez sur Entrée. Saisissez ipconfig /renew et appuyez sur Entrée. Vider le cache DNS Ouvrez une invite de commandes en tant qu’administrateur. Tapez ipconfig /flushdns et appuyez sur Entrée. Vérifier les paramètres du proxy Accédez à Paramètres>Réseau & Proxy Internet>. Désactivez tous les paramètres de proxy manuels. Vérifiez […] »
- **[S2]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « 2. Sous l’onglet Support, sous View common issues, cliquez sur Get started. 3. Développez I want to troubleshoot my PC, puis I’m having connectivity issues et cliquez sur I can’t connect to WiFi. 4. Cliquez sur le bouton Run now pour laisser SupportAssist exécuter une réparation automatisée du Wi-Fi. Si la réparation automatisée SupportAssist n’a pas résolu le problème Wi-Fi, passez à l’étape suivante. »
- **[S3]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 4) : « - Suivez les instructions à l’écran pour terminer le processus. Videz le cache de Windows Update : - Appuyez sur Win + R, tapez services.msc, puis appuyez sur Entrée. - Recherchez le service Windows Update , cliquez dessus avec le bouton droit de la souris, puis sélectionnez Arrêter. - Accédez à C :\Windows\SoftwareDistribution. - Supprimez tous les fichiers et dossiers à l’intérieur de ce répertoire. - Revenez à la fenêtre Services, cliquez avec le bouton droit sur Windows Update et sélectionnez Démarrer. 0x800705b4 : L’installation de la mise à jour a pris trop de temps ou a été interrompue Vérifiez votre connexion Internet : - […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 35/40 — F035 (NET03, fr)

**Question :** La connexion sans fil est instable depuis la dernière mise à jour.

**Guides attendus :** DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows); DOC003 (Dépanner la connexion Wi-Fi sur un PC Dell)

**Réponse de FixIT :**

> Connexion Wi‑Fi instable depuis la mise à jour Windows 11.
> 1. Cliquez sur l’icône Wi‑Fi, choisissez Gérer les connexions Wi‑Fi, oubliez votre réseau, puis reconnectez‑vous en entrant le mot de passe. [S3]
> 2. Ouvrez SupportAssist, allez dans l’onglet Support, cliquez sur Get started pour lancer la réparation automatisée du Wi‑Fi. [S3]
> 3. Allez dans Paramètres > Réseau & Internet > Wi‑Fi, vérifiez que vous êtes bien connecté et que le signal est stable. [S1]
> 4. Si vous utilisez un VPN, désactivez‑le temporairement et testez la connexion Wi‑Fi. [S2]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 4) : « - Suivez les instructions à l’écran pour terminer le processus. Videz le cache de Windows Update : - Appuyez sur Win + R, tapez services.msc, puis appuyez sur Entrée. - Recherchez le service Windows Update , cliquez dessus avec le bouton droit de la souris, puis sélectionnez Arrêter. - Accédez à C :\Windows\SoftwareDistribution. - Supprimez tous les fichiers et dossiers à l’intérieur de ce répertoire. - Revenez à la fenêtre Services, cliquez avec le bouton droit sur Windows Update et sélectionnez Démarrer. 0x800705b4 : L’installation de la mise à jour a pris trop de temps ou a été interrompue Vérifiez votre connexion Internet : - […] »
- **[S2]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 5) : « Si votre appareil est équipé d’un petit disque dur, vous devrez peut-être insérer un lecteur USB pour le mettre à jour. Si votre PC dispose d’un faible espace disque, essayez d’adopter les techniques présentées dans l’article Libérer de l’espace disque dans Windows. Désactiver le VPN : Si vous utilisez un VPN, désactivez-le et réessayez. 0x80070057 ou 0x80080005 : Fichiers endommagés ou configurations système incorrectes Exécution du Vérificateur des fichiers système : Ouvrez l’invite de commandes en tant qu’administrateur et tapez sfc/scannow , puis exécutez. Exécutez l’utilitaire de résolution des problèmes de Windows Update : - […] »
- **[S3]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « vérifiez. À l’issue de l’optimisation de SupportAssist, vérifiez si le Wi-Fi fonctionne. Dans le cas contraire, passez à l’étape suivante. Option Oublier et reconnexion au Wi-Fi Si l’optimisation n’a pas été utile, rétablissez une nouvelle connexion à votre réseau sans fil. 1. Dans la barre d’état système, cliquez sur l’icône Wi-Fi et sélectionnez Gérer les connexions Wi-Fi (icône >). 2. Sous Wi-Fi, recherchez le nom de votre réseau. 3. Cliquez sur Oublier. 4. Pour vous reconnecter, sélectionnez le réseau, saisissez le mot de passe, puis cliquez sur Connexion. La reconnexion n’a pas permis de résoudre le problème ? Passons à l’étape […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 36/40 — F036 (NET03, en)

**Question :** Wi-Fi disconnects whenever my laptop wakes from sleep.

**Guides attendus :** DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows); DOC003 (Dépanner la connexion Wi-Fi sur un PC Dell)

**⚠ langue attendue en, obtenue fr**

**Réponse de FixIT :**

> Le Wi‑Fi se déconnecte à chaque réveil du laptop
> 1. Lancez SupportAssist et exécutez la réparation automatisée du Wi‑Fi (Run now). [S1]
> 2. Vérifiez que le commutateur Wi‑Fi physique et le paramètre Wi‑Fi dans Paramètres > Réseau & Internet sont activés. [S3]
> 3. Assurez‑vous que votre carte réseau prend en charge la bande de fréquence utilisée par votre routeur (2,4 GHz ou 5 GHz). [S3]
> 4. Désactivez le mode Avion et assurez‑vous que le Wi‑Fi n’est pas désactivé dans les paramètres de l’ordinateur. [S2]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « 2. Sous l’onglet Support, sous View common issues, cliquez sur Get started. 3. Développez I want to troubleshoot my PC, puis I’m having connectivity issues et cliquez sur I can’t connect to WiFi. 4. Cliquez sur le bouton Run now pour laisser SupportAssist exécuter une réparation automatisée du Wi-Fi. Si la réparation automatisée SupportAssist n’a pas résolu le problème Wi-Fi, passez à l’étape suivante. »
- **[S2]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 1) : « participer à une visioconférence importante ou simplement de naviguer sur le Web. Problèmes de Wi-Fi courants Connexion Wi-Fi impossible : votre ordinateur ne parvient pas à se connecter aux réseaux sans fil disponibles. Cela est souvent dû au fait que le mode Avion est activé ou que le Wi-Fi est désactivé. Pas de connexion Internet : vous pouvez recevoir un message indiquant que vous êtes connecté au Wi-Fi, mais que vous ne pouvez pas accéder à des sites Web ou à des services en ligne. Connectivité limitée : votre ordinateur se connecte au Wi-Fi, mais ne peut pas accéder à Internet. Dans cette situation, vous obtenez souvent le message […] »
- **[S3]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 8) : « Votre carte réseau sans fil est reconnue, mais aucun réseau Wi-Fi n’est trouvé et vous n’êtes pas connecté à Wi-Fi Si vous voyez l’icône Pas de connexion Internet alors que vous êtes à portée de réseaux Wi-Fi, cela peut signifier que : Le commutateur Wi-Fi physique sur votre ordinateur portable ou votre tablette est désactivé. Assurez-vous qu’il est activé. Le Wi-Fi est désactivé dans les paramètres Wi-Fi. Ouvrez Paramètres, puis sélectionnez Réseau & Internet. Assurez-vous que le Wi-Fi est activé. Votre adaptateur ne prend pas en charge la fréquence de diffusion de votre réseau. Par exemple, il se peut que votre carte prenne uniquement en […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 37/40 — F037 (NET04, fr)

**Question :** Wi-Fi connecté mais aucune page web ne se charge.

**Guides attendus :** DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows); DOC003 (Dépanner la connexion Wi-Fi sur un PC Dell)

**Réponse de FixIT :**

> Wi‑Fi connecté mais aucune page web ne se charge.
> 1. Vérifiez que le commutateur Wi‑Fi physique et le paramètre Wi‑Fi dans les paramètres sont activés. [S1]
> 2. Ouvrez les paramètres réseau : Démarrer > Paramètres > Réseau & Internet > Wi‑Fi. [S2]
> 3. Vérifiez le statut de la connexion : si vous voyez « Connectivité limitée » ou « Pas de connexion Internet », cela indique que le Wi‑Fi est connecté mais qu’Internet n’est pas accessible. [S3]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 8) : « Votre carte réseau sans fil est reconnue, mais aucun réseau Wi-Fi n’est trouvé et vous n’êtes pas connecté à Wi-Fi Si vous voyez l’icône Pas de connexion Internet alors que vous êtes à portée de réseaux Wi-Fi, cela peut signifier que : Le commutateur Wi-Fi physique sur votre ordinateur portable ou votre tablette est désactivé. Assurez-vous qu’il est activé. Le Wi-Fi est désactivé dans les paramètres Wi-Fi. Ouvrez Paramètres, puis sélectionnez Réseau & Internet. Assurez-vous que le Wi-Fi est activé. Votre adaptateur ne prend pas en charge la fréquence de diffusion de votre réseau. Par exemple, il se peut que votre carte prenne uniquement en […] »
- **[S2]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 1) : « Suivez ces étapes pour garantir la connectivité : - Sélectionnez Démarrer>les paramètres>Réseau & Internet>Wi-Fi. »
- **[S3]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 1) : « participer à une visioconférence importante ou simplement de naviguer sur le Web. Problèmes de Wi-Fi courants Connexion Wi-Fi impossible : votre ordinateur ne parvient pas à se connecter aux réseaux sans fil disponibles. Cela est souvent dû au fait que le mode Avion est activé ou que le Wi-Fi est désactivé. Pas de connexion Internet : vous pouvez recevoir un message indiquant que vous êtes connecté au Wi-Fi, mais que vous ne pouvez pas accéder à des sites Web ou à des services en ligne. Connectivité limitée : votre ordinateur se connecte au Wi-Fi, mais ne peut pas accéder à Internet. Dans cette situation, vous obtenez souvent le message […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 38/40 — F038 (NET04, en)

**Question :** Connected to Wi-Fi, no internet, yellow triangle on the icon.

**Guides attendus :** DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows); DOC003 (Dépanner la connexion Wi-Fi sur un PC Dell)

**⚠ langue attendue en, obtenue fr**

**Réponse de FixIT :**

> Vous êtes connecté à un réseau Wi‑Fi mais vous n’avez pas accès à Internet, l’icône du réseau affiche un triangle jaune.
> 1. Vérifiez que le commutateur Wi‑Fi physique de votre appareil est activé et que le paramètre Wi‑Fi dans Paramètres > Réseau & Internet est activé. [S1]
> 2. Assurez‑vous que votre carte réseau prend en charge la bande de fréquence utilisée par votre routeur (2,4 GHz ou 5 GHz). Si nécessaire, changez le canal ou la bande sur le routeur. [S1]
> 3. Exécutez l’assistant de résolution des problèmes réseau de Windows : Paramètres > Réseau & Internet > Statut > Résoudre les problèmes. [S2]
> 4. Vérifiez la connectivité Internet en ouvrant un navigateur ou en pingant un site (ex. `ping www.google.com`). Si le ping échoue, vérifiez les paramètres DNS ou redémarrez le routeur. [S3]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 8) : « Votre carte réseau sans fil est reconnue, mais aucun réseau Wi-Fi n’est trouvé et vous n’êtes pas connecté à Wi-Fi Si vous voyez l’icône Pas de connexion Internet alors que vous êtes à portée de réseaux Wi-Fi, cela peut signifier que : Le commutateur Wi-Fi physique sur votre ordinateur portable ou votre tablette est désactivé. Assurez-vous qu’il est activé. Le Wi-Fi est désactivé dans les paramètres Wi-Fi. Ouvrez Paramètres, puis sélectionnez Réseau & Internet. Assurez-vous que le Wi-Fi est activé. Votre adaptateur ne prend pas en charge la fréquence de diffusion de votre réseau. Par exemple, il se peut que votre carte prenne uniquement en […] »
- **[S2]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 1) : « plus, consultez Se connecter à un VPN dans Windows. Pas d’Internet Votre appareil ne possède pas de connexion Internet. Concernant le Wi-Fi, cette icône peut apparaître pour une ou plusieurs raisons. Résolution des problèmes généraux Veuillez essayer les étapes de dépannage générales suivantes pour résoudre le problème Wi-Fi. Étape 1. Vérifier l’état de votre connexion réseau Sélectionnez les icônes Réseau, Son ou Batterie ( ) sur le côté droit de la barre des tâches. Assurez-vous que Wi-Fi est activé. »
- **[S3]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 6) : « (reportez-vous à son manuel) et modifiez le canal sans fil pour réduire les interférences. Vous êtes connecté au Wi-Fi, mais aucune connexion Internet n’est détectée (c’est ce que l’on qualifie de « connectivité limitée ») Votre PC Windows est connecté à votre réseau local mais n’est pas connecté à Internet. Si vous sélectionnez l’icône Pas de connexion Internet, le message Pas d’Internet s’affiche sous le réseau Wi-Fi auquel vous êtes connecté. Vous pouvez probablement voir d’autres PC et appareils sur votre réseau local, mais vous ne pouvez faire aucune opération nécessitant un accès à Internet, comme surfer sur le web, consulter vos […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 39/40 — F039 (NET04, fr)

**Question :** J'ai le Wi-Fi mais Internet ne fonctionne pas, que faire ?

**Guides attendus :** DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows); DOC003 (Dépanner la connexion Wi-Fi sur un PC Dell)

**Réponse de FixIT :**

> Vous avez un signal Wi‑Fi mais aucune connexion Internet.
> 1. Lancez SupportAssist et exécutez la réparation automatisée du Wi‑Fi (Run now). [S1]
> 2. Vérifiez que le commutateur Wi‑Fi physique est activé et que le Wi‑Fi est activé dans Paramètres > Réseau & Internet. [S3]
> 3. Assurez‑vous que votre carte réseau prend en charge la bande de fréquence utilisée par votre routeur (2,4 GHz ou 5 GHz). [S3]
> 4. Ouvrez Paramètres > Réseau & Internet > Wi‑Fi pour confirmer que le Wi‑Fi est bien activé. [S2]
> Si le problème persiste après ces vérifications, vous pouvez créer un ticket pour qu'un technicien prenne le relais.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « 2. Sous l’onglet Support, sous View common issues, cliquez sur Get started. 3. Développez I want to troubleshoot my PC, puis I’m having connectivity issues et cliquez sur I can’t connect to WiFi. 4. Cliquez sur le bouton Run now pour laisser SupportAssist exécuter une réparation automatisée du Wi-Fi. Si la réparation automatisée SupportAssist n’a pas résolu le problème Wi-Fi, passez à l’étape suivante. »
- **[S2]** DOC028 — Résoudre les problèmes de mise à jour de Windows (page 1) : « Suivez ces étapes pour garantir la connectivité : - Sélectionnez Démarrer>les paramètres>Réseau & Internet>Wi-Fi. »
- **[S3]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 8) : « Votre carte réseau sans fil est reconnue, mais aucun réseau Wi-Fi n’est trouvé et vous n’êtes pas connecté à Wi-Fi Si vous voyez l’icône Pas de connexion Internet alors que vous êtes à portée de réseaux Wi-Fi, cela peut signifier que : Le commutateur Wi-Fi physique sur votre ordinateur portable ou votre tablette est désactivé. Assurez-vous qu’il est activé. Le Wi-Fi est désactivé dans les paramètres Wi-Fi. Ouvrez Paramètres, puis sélectionnez Réseau & Internet. Assurez-vous que le Wi-Fi est activé. Votre adaptateur ne prend pas en charge la fréquence de diffusion de votre réseau. Par exemple, il se peut que votre carte prenne uniquement en […] »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---

### 40/40 — F040 (NET04, en)

**Question :** Wi-Fi shows 'no internet, secured' on Windows.

**Guides attendus :** DOC001 (Résoudre les problèmes de connexion Wi-Fi dans Windows); DOC003 (Dépanner la connexion Wi-Fi sur un PC Dell)

**Réponse de FixIT :**

> Your Windows PC is connected to Wi‑Fi but shows 'No Internet, Secured', indicating limited connectivity.
> 1. Disable Wi‑Fi, re‑enable it, and reconnect to your network. [S1]
> 2. Open an elevated command prompt and run 'ipconfig /release' followed by 'ipconfig /renew' to refresh your IP address. [S1]
> 3. Flush the DNS cache by running 'ipconfig /flushdns' in an elevated command prompt. [S1]
> 4. Check proxy settings: go to Settings > Network & Internet > Proxy and turn off any manual proxy configuration. [S1]
> If the problem persists after these checks, you can open a ticket so that a technician can take over.

**Extraits que FixIT a lus pour répondre (S1, S2, S3) :**

- **[S1]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 7) : « Si l’appareil se connecte au Wi-Fi, mais qu’Internet n’est pas disponible, suivez les étapes de dépannage ci-dessous. Désactivez le Wi-Fi, réactivez-le et reconnectez-vous à votre réseau sans fil. Renouveler la configuration IP Ouvrez une invite de commandes en tant qu’administrateur. Saisissez ipconfig /release et appuyez sur Entrée. Saisissez ipconfig /renew et appuyez sur Entrée. Vider le cache DNS Ouvrez une invite de commandes en tant qu’administrateur. Tapez ipconfig /flushdns et appuyez sur Entrée. Vérifier les paramètres du proxy Accédez à Paramètres>Réseau & Proxy Internet>. Désactivez tous les paramètres de proxy manuels. Vérifiez […] »
- **[S2]** DOC001 — Résoudre les problèmes de connexion Wi-Fi dans Windows (page 6) : « (reportez-vous à son manuel) et modifiez le canal sans fil pour réduire les interférences. Vous êtes connecté au Wi-Fi, mais aucune connexion Internet n’est détectée (c’est ce que l’on qualifie de « connectivité limitée ») Votre PC Windows est connecté à votre réseau local mais n’est pas connecté à Internet. Si vous sélectionnez l’icône Pas de connexion Internet, le message Pas d’Internet s’affiche sous le réseau Wi-Fi auquel vous êtes connecté. Vous pouvez probablement voir d’autres PC et appareils sur votre réseau local, mais vous ne pouvez faire aucune opération nécessitant un accès à Internet, comme surfer sur le web, consulter vos […] »
- **[S3]** DOC003 — Dépanner la connexion Wi-Fi sur un PC Dell (page 3) : « 2. Sous l’onglet Support, sous View common issues, cliquez sur Get started. 3. Développez I want to troubleshoot my PC, puis I’m having connectivity issues et cliquez sur I can’t connect to WiFi. 4. Cliquez sur le bouton Run now pour laisser SupportAssist exécuter une réparation automatisée du Wi-Fi. Si la réparation automatisée SupportAssist n’a pas résolu le problème Wi-Fi, passez à l’étape suivante. »

**Ta note (0, 1 ou 2) :** ____  **Commentaire si 0 ou 1 :** ________________

---


## Les 10 questions hors corpus (jugées automatiquement par `repli_correct`)

| ID | Question | Type obtenu | Sources | repli_correct |
|---|---|---|---|---|
| F041 | Quelle est la capitale du Canada ? | repli | — | oui |
| F042 | What's the best way to learn Spanish? | repli | — | oui |
| F043 | Comment changer un pneu crevé sur ma voiture ? | repli | — | oui |
| F044 | Give me a recipe for chocolate chip cookies. | repli | — | oui |
| F045 | Quels sont les symptômes de la grippe ? | repli | — | oui |
| F046 | How do I invest in the stock market? | repli | — | oui |
| F047 | Quel temps fera-t-il demain à Tunis ? | repli | — | oui |
| F048 | Write a short poem about the ocean. | repli | — | oui |
| F049 | Comment fixer une étagère au mur ? | repli | — | oui |
| F050 | What is the population of Japan? | repli | — | oui |