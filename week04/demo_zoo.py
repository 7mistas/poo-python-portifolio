""" Modulo que importa de animal.py a Classe Mae e respectivas Filhas. """
from animals import Animal, Cachorro, Gato, Passaro
""" Modulo que importa de zoo.py a lista e seu método. """
from zoo import Zoologico

""" Inicia o código de demontração do Zoológico.  """
def main():
    print("==== Demostração do Zoo ====")
    print("\n=" * 50)
    
    print("==== Instanciando os animais... ====")
    animal_1 = Cachorro("Bob", 7)
    animal_2 = Cachorro("Bibi", 14)
    animal_3 = Gato("Lorde", 21)
    animal_4 = Gato("Pingo", 7)
    animal_5 = Cachorro("Paz", 1)
    animal_6 = Passaro("Lis", 19)
    animal_7 = Cachorro("Craque", 19)

    print("==== Adicionando os animais a lista...====")
    animais_listados = Zoologico()
    animais_listados.zoo.append(animal_1)
    animais_listados.zoo.append(animal_2)
    animais_listados.zoo.append(animal_3)
    animais_listados.zoo.append(animal_4)
    animais_listados.zoo.append(animal_5)
    animais_listados.zoo.append(animal_6)
    animais_listados.zoo.append(animal_7)
    
    print("==== Listando os animais do zoo...====")
    animais_listados.mostrar_animais()

    print("==== Fim da demostração do código zoo ====")

if __name__ == "__main__":
    main()
