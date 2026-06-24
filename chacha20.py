from block_function import state_builder, block_function, serialize, next_state


def chacha20_encrypt(key: int, counter: int, nonce: int, plaintext: bytes) -> bytes:
    """
    Chiffre un message avec l’algorithme ChaCha20.

    ChaCha20 génère un flot de clés de 64 octets (512 bits) par appel à la fonction de bloc,
    puis applique un XOR entre ce flot et le texte clair.

    :param key: la clé (256 bits).
    :param counter: le compteur de blocs initial (32 bits).
        Note : Cette valeur peut être définie comme étant n'importe quel nombre, mais sera généralement zéro ou un.
               Il est logique d'utiliser un si le bloc zéro est utilisé pour autre chose, comme générer une clé
               d'authentification à usage unique (dans le cadre d'un )algorithme AEAD).
    :param nonce: le nonce (96 bits).
    :param plaintext: le texte clair à chiffrer.
    :return: le texte chiffré (même longueur que `plaintext`).
    """
    state = state_builder(key, counter, nonce)

    encrypted_message = bytearray()

    for i in range(0, len(plaintext), 64):
        key_stream_block = block_function(state)

        key_stream_int = serialize(key_stream_block)
        key_stream_bytes = key_stream_int.to_bytes(64, 'big')

        chunk_text = plaintext[i:i + 64]

        for j in range(len(chunk_text)):
            encrypted_byte = chunk_text[j] ^ key_stream_bytes[j]
            encrypted_message.append(encrypted_byte)
        state = next_state(state)

    return bytes(encrypted_message)
