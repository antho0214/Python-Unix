file = open("reverse_polish_notation", "r")

for element in file:
    new_calcul = []
    element = element.split()
    resultat = []
    for n in element:

        match n:

            case '+':

                a = new_calcul[-2]
                b = new_calcul[-1]
                result = a + b
                print(new_calcul[:-2])
                # Mettre à jour la pile
                new_calcul = new_calcul[:-2] + [result]

            case '-':
                a = new_calcul[-2]
                b = new_calcul[-1]
                result = a - b
                new_calcul = new_calcul[:-2] + [result]


            case '*':
                a = new_calcul[-2]
                b = new_calcul[-1]
                result = a * b
                new_calcul = new_calcul[:-2] + [result]

            case '/':
                a = new_calcul[-2]
                b = new_calcul[-1]
                result = a / b
                new_calcul = new_calcul[:-2] + [result]


            case _:
                new_calcul.append(int(n))



    print("res", new_calcul[0])

