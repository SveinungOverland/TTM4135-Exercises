import numpy as np
from sympy import Matrix


def takeInput():
    global what_do, parameters
    what_do = input("What do? (e - encrypt, d - decrypt, k - known attack): ")
    if what_do == "e":
        parameters = [
            input("String to encrypt (TH): ") or "TH",
            input("with key (17 15 24 17): ") or "17 15 24 17",
        ]
    elif what_do == "d":
        parameters = [
            input("String to decrypt (MD): ") or "MD",
            input("with key (17 15 24 17): ") or "17 15 24 17",
        ]
    elif what_do == "k":
        parameters = [
            input("Enter encoded ngrams (MD XC): ") or "MD XC",
            input("enter known ngrams (TH HE): ") or "TH HE",
        ]


def encrypt(string: str, key: str):
    P = np.array([ord(it) - 65 for it in string])
    K = np.array([int(it) for it in key.split(" ")]).reshape((2, 2))
    C = K.dot(P)
    C = np.mod(C, 26)
    print(f"Resulting ciphertext: { ''.join([ chr(it + 65) for it in C ]) }")


def decrypt(string: str, key: str):
    C = np.array([ord(it) - 65 for it in string])
    K = np.array([int(it) for it in key.split(" ")]).reshape((2, 2))
    K_inv = np.array(Matrix(K).inv_mod(26))
    P = K_inv.dot(C)
    P = np.mod(P, 26)
    print(f"Resulting text: { ''.join([ chr(it + 65) for it in P ]) }")


def known_attack(encoded_ngrams: str, known_ngrams: str):
    P = Matrix(
        list(map(lambda x: [ord(it) - 65 for it in x], known_ngrams.split(" ")))
    ).T
    C = np.array(
        list(map(lambda x: [ord(it) - 65 for it in x], encoded_ngrams.split(" ")))
    ).T
    P_inv = np.array(P.inv_mod(26))
    K = np.dot(C, P_inv)
    K = np.mod(K, 26)
    print(f"K: {K}")


def main():
    # while True:
    takeInput()
    if what_do == "e":
        encrypt(parameters[0], parameters[1])
    elif what_do == "d":
        decrypt(parameters[0], parameters[1])
    elif what_do == "k":
        known_attack(parameters[0], parameters[1])


if __name__ == "__main__":
    main()