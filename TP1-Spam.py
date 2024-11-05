import csv
from collections import defaultdict

def format_phone_number(num_tel):
    # Retirer tout ce qui n'est pas un chiffre ou le symbole '+'
    num_tel = ''.join([i for i in num_tel if i.isnumeric() or i == '+'])

    # Remplacer +33 ou 0033 par 0
    if num_tel.startswith('+33'):
        num_tel = '0' + num_tel[3:]
    elif num_tel.startswith('0033'):
        num_tel = '0' + num_tel[4:]

    # Vérifier si le numéro commence par 0 et fait 10 chiffres de long
    if not num_tel.startswith('0') or len(num_tel) != 10:
        return False, None

    # Formater le numéro
    formatted_number = '-'.join([num_tel[k:k+2] for k in range(0, 10, 2)])
    return True, formatted_number

def main():
    # Demande un numéro de téléphone à l'utilisateur
    user_input = input("Entrez un numéro de téléphone : ")
    valid, formatted = format_phone_number(user_input)
    if valid:
        print(f"Numéro formaté : {formatted}")
    else:
        print("Numéro invalide.")

    # Analyse d'un fichier complet de numéros
    invalid_names = []
    try:
        with open('liste_numeros.txt', 'r') as f:
            r = csv.reader(f, delimiter=':')
            l = list(r)
    except FileNotFoundError:
        print('Fichier liste_numeros.txt introuvable')
        exit(0)

    names, phone_numbers = zip(*l)

    # Formater les numéros et créer une liste de ceux qui sont valides
    valid_entries = []
    
    for name, phone in zip(names, phone_numbers):
        is_valid, formatted = format_phone_number(phone)
        if is_valid:
            valid_entries.append((name, formatted))
        else:
            invalid_names.append(name)

    # Écriture des numéros formatés dans un nouveau fichier
    with open('output.txt', 'w', newline='') as output_file:
        writer = csv.writer(output_file, delimiter=':', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(valid_entries)

    print(f"{len(valid_entries)} numéros valides ont été écrits dans output.txt.")
    print(f"Noms avec numéros invalides : {', '.join(invalid_names) if invalid_names else 'Aucun'}")

    # Analyse des familles avec des numéros de téléphone identiques
    phone_to_names = defaultdict(list)
    
    for name, phone in valid_entries:
        phone_to_names[phone].append(name)

    families = [names for names in phone_to_names.values() if len(names) > 1]

    print("Familles avec le même numéro de téléphone :")
    for family in families:
        print(", ".join(family))

if __name__ == "__main__":
    main()
