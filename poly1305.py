from block_function import block_function, state_builder, serialize


P1305_MODULUS = (1 << 130) - 5


def le_bytes_to_int(b: bytes) -> int:
    """
    Convertit un tableau d'octets en un entier non signé (little-endian).
    :param b: le tableau d'octets à convertir.
    :return: l'entier représentant le tableau d'octets donné (entier non signé).
    """
    return int.from_bytes(b, 'little')


def int_to_le_bytes(x: int, length: int) -> bytes:
    """
    Convertit un entier non signé en un tableau d'octets de taille donnée (little-endian).
    :param x: l'entier non signé à convertir.
    :param length: la taille en octets du tableau créé.
    :return: le tableau d'octets de taille 'length' (tronque aux 'length' LSB si besoin).
    """
    masque = (1 << (length * 8)) - 1
    return (x & masque).to_bytes(length, 'little')


def clamp_r(r: bytes) -> int:
    """
    Applique le 'clamping' RFC 8439 à la clé secrète r (16-octet little-endian number) :
    r &= 0x0ffffffc0ffffffc0ffffffc0fffffff
    puis la renvoie sous la forme d'un entier non signé (128 bits).
    :param r: la clé secrète.
    :return: la clé secrète r après clamping.
    """
    r_int = le_bytes_to_int(r)
    r_int &= 0x0ffffffc0ffffffc0ffffffc0fffffff
    return r_int


def poly1305_mac(message: bytes, one_time_key: bytes) -> bytes:
    """
    Calcule un code d'authentification (tag) en utilisant l’algorithme Poly1305 (RFC 8439 §2.5).

    Cet algorithme est utilisé pour authentifier des messages avec une clé secrète.
    Poly1305 fonctionne sur des blocs de 16 octets et repose sur des opérations arithmétiques
    modulo p = 2^130 - 5.

    :param message: le message à authentifier (longueur arbitraire).
    :param one_time_key: la clé secrète de départ (32 octets - little-endian).
                         composée de r (16 premiers octets) et de s (16 derniers octets).
    :return: le tag d'authentification généré (16 octets - little-endian).
    """
    r_bytes = one_time_key[:16]
    s_bytes = one_time_key[16:]

    r = clamp_r(r_bytes)
    s = le_bytes_to_int(s_bytes)

    accum = 0
    p = P1305_MODULUS

    for i in range(0, len(message), 16):
        block = message[i:i + 16]

        block_int = le_bytes_to_int(block)

        block_value = block_int + (1 << (len(block) * 8))

        accum += block_value
        accum = (accum * r) % p

    accum += s
    return int_to_le_bytes(accum, 16)


def poly1305_key_gen_chacha20(key: int, nonce: int) -> bytes:
    """
    Génère une clé Poly1305 de 32 octets à partir de la fonction de bloc ChaCha20.

    Cette fonction dérive la clé unique Poly1305 conformément au mécanisme décrit dans ChaCha20-Poly1305 AEAD.
    Elle initialise l’état ChaCha20 avec la clé fournie, un compteur fixé à zéro et le nonce indiqué.
    Les 32 premiers octets (8 mots de 32 bits) produits par le premier bloc ChaCha20 sont extraits,
    convertis en little-endian et renvoyés comme clé Poly1305.

    :param key: la clé ChaCha20 (256 bits).
    :param nonce: le nonce ChaCha20 (96 bits).
    :return: la clé unique (one-time key) Poly1305 (256 premiers bits du bloc ChaCha20, encodés en little-endian).

    Remarques:
    - Le compteur ChaCha20 est toujours fixé à zéro pour la dérivation de la clé.
    - Il est impératif de ne jamais réutiliser une paire (clé, nonce) pour plusieurs messages, sous peine de compromettre la sécurité de Poly1305.
    """
    counter = 0

    state = state_builder(key, counter, nonce)
    block_output = block_function(state)

    block_bytes = serialize(block_output).to_bytes(64, 'big')

    return block_bytes[:32]
