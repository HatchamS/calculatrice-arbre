white_list = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '^', '(', ')', "."}
mathematic_symbol = ('*', '/', '+', '^', '-')


class Noeud:
    def __init__(self, racine):
        self.gauche = None
        self.droit = None
        self.racine = racine

    def __repr__(self):
        return f'{self.racine}({str(self.gauche)},{str(self.droit)})'

    def change_racine(self, operator):
        new_node = Noeud(operator)
        new_node.gauche = self.gauche
        new_node.droit = self.droit
        self.racine, new_node.racine = new_node.racine, self.racine
        self.gauche = new_node
        self.droit = None

    def add_value_tige_gauche(self, valeur):
        if self is None:
            return 0
        self.gauche = self.gauche.add_value_tige_gauche(valeur) if self.gauche else valeur
        return self

    def add_value_tige_droit(self, valeur):
        if self is None:
            return 0
        self.droit = self.droit.add_value_tige_droit(valeur) if self.droit else valeur
        return self

    def calcul_branches(self):
        if type(self.droit) != Noeud and type(self.gauche) != Noeud:
            return do_operation(self)
        elif type(self.gauche) == Noeud:
            self.gauche = self.gauche.calcul_branches() if self.gauche else 0
        else:
            self.droit = self.droit.calcul_branches() if self.gauche else 0

        return self.calcul_branches()


add = lambda x, y: x + y
mul = lambda x, y: x * y
puissance = lambda x, y: x ** y
soustra = lambda x, y: x - y
division = lambda x, y: x / y

repertory_calcul = {"+": add, "*": mul, "^": puissance, "-": soustra, "/": division}


def modif_graph(graph_calcul: Noeud, number: str, op_caract: str):
    if graph_calcul.racine is None:
        graph_calcul.racine = op_caract
        graph_calcul.add_value_tige_gauche(number)

    elif op_caract in {"*", "/", "^"}:

        if graph_calcul.droit is None or op_caract == "^":
            tmpNode = Noeud(op_caract)
            tmpNode.gauche = number
            graph_calcul.add_value_tige_droit(tmpNode)
        else:
            graph_calcul.add_value_tige_droit(number)
            graph_calcul.droit.change_racine(op_caract)

    elif op_caract in {"+", "-"}:
        graph_calcul.change_racine(op_caract)
        graph_calcul.gauche.add_value_tige_droit(number)

    else:
        graph_calcul.add_value_tige_droit(number)


def parse_expression(calcul_verified: str) -> Noeud:
    graph = Noeud(None)
    temp_number = ""
    max_range = len(calcul_verified) - 1
    for index, caract in enumerate(calcul_verified):
        if caract in mathematic_symbol:
            modif_graph(graph, temp_number, caract)
            temp_number = ""
            temp_op = caract
        elif index == max_range:
            temp_number += caract
            modif_graph(graph, temp_number, "")
        else:
            temp_number += caract

    return graph


def verification_syntax(calcul_brut: str):
    if calcul_brut.count('(') != calcul_brut.count(')'):
        raise Exception("une parentèse n'est pas fermé")

    if not white_list.issuperset(set(calcul_brut)):
        raise Exception("Un caractère non autoriser a été saisie")

    if calcul_brut[0] in mathematic_symbol:
        raise Exception("erreur le calcul ne doit pas commencer par un symbole mathématique")


def do_operation(expresion: Noeud) -> int:
    number = tuple(map(float, (expresion.gauche, expresion.droit)))
    return repertory_calcul.get(expresion.racine)(number[0], number[1])


def main():
    print("entré le calcul :")
    data_input = str(input())

    verification_syntax(data_input)

    graph_calcul = parse_expression(data_input)
    print(graph_calcul)

    final_result = graph_calcul.calcul_branches()
    print(final_result)


main()
