# 🔒 ChaCha20-Poly1305 AEAD & Image Encryption

Ce projet pédagogique en Python implémente l'algorithme de chiffrement authentifié **ChaCha20-Poly1305 AEAD**, tel que défini dans les standards cryptographiques officiels ([RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539) et [RFC 8439](https://datatracker.ietf.org/doc/html/rfc8439)). 

Réalisé dans le cadre d'un cours de mathématiques appliquées, il applique cette cryptographie au chiffrement et déchiffrement d'images locales.

---

## 🎯 Objectifs du projet

- **Comprendre la cryptographie moderne** : Plonger dans le fonctionnement interne de ChaCha20 (quarter rounds, opérations sur colonnes/diagonales, gestion d'états).
- **Garantir l'intégrité** : Implémenter l'authentification de message avec Poly1305.
- **Construction AEAD** *(Authenticated Encryption with Associated Data)* : Combiner confidentialité et authenticité des données.
- **Application pratique** : Utiliser l'algorithme pour chiffrer et déchiffrer des fichiers images réels via un menu interactif.

---

## ✨ Fonctionnalités

- **ChaCha20** : Génération d'un *keystream* et chiffrement par flot (XOR).
- **Poly1305** : Calcul du tag d'authentification à partir d'une clé dérivée.
- **AEAD** : Intégration complète avec gestion des Données Additionnelles Authentifiées (AAD).
- **Application Images** : Chiffrement de fichiers images avec extraction des matrices de pixels via `NumPy` et `Pillow`.
- **Interface CLI** : Menu interactif simple pour chiffrer, déchiffrer et nettoyer l'espace de travail.

---

## 🛠️ Architecture du Code

Le projet est modulaire, chaque fichier traitant une étape spécifique de l'algorithme :

| Fichier | Rôle |
|---------|------|
| `quarter_round.py` | Opérations arithmétiques de base (mod 2^32, XOR, décalages circulaires). |
| `block_function.py`| Construction de l'état (16 mots de 32 bits) et exécution des 20 rounds. |
| `chacha20.py` | Logique de chiffrement par flot (génération et application du keystream). |
| `poly1305.py` | Algorithme de calcul du code d'authentification (MAC) modulo 2^130 - 5. |
| `aead_chacha20_poly1305.py`| Orchestration de l'AEAD (Chiffrement + Padding + MAC). |
| `picture.py` | Conversion des images en bytes, génération des nonces/clés et interfaçage. |
| `main.py` | Point d'entrée de l'application et menu interactif. |

---

## 🚀 Installation et Configuration

### 1. Prérequis
Assurez-vous d'avoir **Python 3.8 ou une version supérieure** installé sur votre machine.

### 2. Installation des dépendances
Ce projet utilise `Pillow` pour charger et sauvegarder les fichiers images, et `NumPy` pour manipuler efficacement les matrices de pixels sous forme de tableaux d'octets bruts :
```bash
pip install Pillow numpy

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/KMS44444/projet-chacha20-poly1305.git
   cd projet-chacha20-poly1305

## 📁 Structure des répertoires requis

Pour éviter toute erreur d'exécution, vous devez vous assurer de la présence d'un dossier `resources` à la racine du projet, structuré ainsi :

```text
📁 resources/
├── 📁 Images/       <-- Placez ici vos images d'origine (ex: photo.png, paysage.jpg)
├── 📁 Encrypted/    <-- Accueillera automatiquement les images chiffrées
└── 📁 Decrypted/    <-- Accueillera les images déchiffrées après validation
```

## 💻 Guide d'Utilisation
L'ensemble de l'application se pilote de manière interactive directement depuis votre terminal.

Lancement de l'application
Exécutez le script principal à la racine du projet :

```bash
python main.py
```
Le menu interactif suivant s'affiche alors sur votre console :
```text
==================================================
Menu :
==================================================
1. Effacer les fichiers
2. Chiffrer une image
3. Déchiffrer une image
q. Quitter
==================================================
```
## 🔐 Chiffrer une image (Option 2)
‎ 1. Entrez 2 et appuyez sur Entrée.

‎ 2. L'application scanne le dossier resources/Images/ et affiche la liste des images disponibles. Tapez le numéro de l'image choisie.

‎ 3. Le programme vous demande de saisir les Données Additionnelles Authentifiées (AAD) :

```text
AAD (données additionnelles authentifiées non chiffrées) : MonSecretMathematique123
```

(L'AAD est une chaîne de caractères textuelle qui ne sera pas chiffrée mais qui sera liée mathématiquement au tag de sécurité pour empêcher toute modification ultérieure du contexte).

L'algorithme génère automatiquement une clé de 256 bits et un nonce de 96 bits de manière aléatoire.

⚠️ ATTENTION : L'application affiche des informations de sécurité vitales sur votre console :

```text
IMPORTANT - Conservez ces informations : elles sont indispensables pour déchiffrer l'image :
Clé générée : a1b2c3d4... (64 caractères hexadécimaux)
Nonce: e1f2a3b4... (24 caractères hexadécimaux)
Aad: MonSecretMathematique123
Tag: 9f8e7d6c... (32 caractères hexadécimaux)
```

Copiez et sauvegardez immédiatement ces 4 éléments (Clé, Nonce, Aad, Tag) dans un bloc-notes (resources/data.txt est prévu à cet effet). Sans eux, le déchiffrement sera impossible.

L'image chiffrée est créée et stockée dans resources/Encrypted/.

## 🔓 Déchiffrer une image (Option 3)
‎ 1. Dans le menu principal, entrez 3 et appuyez sur Entrée.

‎ 2. Sélectionnez le numéro correspondant à l'image chiffrée présente dans resources/Encrypted/.

‎ 3. Saisissez scrupuleusement et l'une après l'autre les informations demandées que vous avez mises de côté :

- La clé (en hexadécimal)

- Le nonce (en hexadécimal)

- Le tag (en hexadécimal)

- L'AAD (votre texte d'origine)

Vérification d'intégrité (Poly1305) :
Si les informations sont correctes : Le message ```Le contrôle du TAG a réussi.```s'affiche. L'image est fidèlement reconstruite et sauvegardée dans le dossier ```resources/Decrypted/```.

Si une information est fausse ou si l'image chiffrée a été modifiée : Une erreur ```ValueError est levée```, bloquant immédiatement le processus afin de signaler la corruption ou l'attaque.

## 🗑️ Nettoyer l'espace de travail (Option 1)
Pour vider vos dossiers de résultats entre deux tests cryptographiques, choisissez l'option ```1```. Après confirmation (```o```), tous les fichiers générés dans les dossiers ```resources/Encrypted/``` et ```resources/Decrypted/``` seront définitivement supprimés.
