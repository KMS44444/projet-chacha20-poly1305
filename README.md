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
