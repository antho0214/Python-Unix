import re
def conversion(verilog_file, vhdl_file):
    boolean_counter = 0
    # Traite le fichier Verilog et obtient les informations nécessaires
    module_name, ports, wire, assign = traitement_verilog(verilog_file)

    # Ouvre le fichier VHDL pour l'écriture
    with open(vhdl_file, 'w') as file:
        # Écrit la déclaration de l'entité VHDL
        file.write("Library IEEE;\nuse IEEE.std_logic_1164.all;\nuse std.textio.all;\n")
        file.write(f"entity {module_name} is\n")


        # Gestion des ports
        file.write("port (")
        for element in ports:
            downto = element[1].split(":")

            if element[0] == 'input':
                std1 = f"std_logic_vector({downto[0][1:]} downto {downto[1][:1]});"
                file.write(f"{element[2]} : in {std1}\n")
            elif element[0] == 'output':
                std2 = f"std_logic_vector({downto[0][1:]} downto {downto[1][:1]})"
                file.write(f"{element[2]} : out {std2}\n")
        file.write(");\n")

        file.write(f"end {module_name};\n")

        # Déclaration de l'architecture
        full_adder_struct = module_name + '_struct'
        file.write(f"architecture {full_adder_struct} of {module_name} is\n")

        # Gestion des signaux "wire"
        for element in wire:
            file.write(f"signal {element[1]}: std_logic;\n")

        file.write("begin\n")

        # Traitement des affectations "assign"
        for element in assign:
            vhdl_line = " ".join(element[1:])  # Ignore le mot-clé 'assign'
            vhdl_line = vhdl_line.replace("=", "<=")
            vhdl_line = vhdl_line.replace("^", "xor")
            vhdl_line = vhdl_line.replace("&", "and")
            vhdl_line = vhdl_line.replace("|", "or")
            vhdl_line = vhdl_line.replace("~", "not ")
            vhdl_line = vhdl_line.replace("]", ")")
            vhdl_line = vhdl_line.replace("[", "(")
            # Remplacer les nombres binaires après '0'b et '1'b et les encapsuler entre des apostrophes
            vhdl_line = re.sub(r"(0'b|1'b)([01]+)", r"'\2'", vhdl_line)

            vhdl_line = vhdl_line.rstrip(";")


            file.write(f"{vhdl_line};\n")
            boolean_counter += 1
        print(f"{boolean_counter} boolean operators were created")
        file.write(f"end {full_adder_struct};\n")
        tb_file = vhdl_file.split('.')[0] + '_tb.vhdl'
        print(tb_file)
        testbench_generation(tb_file,module_name)

        return module_name

def traitement_verilog(verilog_file):
    try :
        # Lis le fichier Verilog
        with open(verilog_file, 'r') as file:
            lines = file.readlines()
    except Exception as e:
        print(e)

    # Initialisation des variables
    module_name = None

    ports = []

    wire = []
    assign = []

    # Traite chaque ligne du fichier Verilog
    for line in lines:
        line = line.strip()  # Supprime les espaces inutiles

        # Trouver le nom du module
        if line.startswith("module"):
            parts = line.split()  # Sépare les mots par espace
            module_name = parts[1].split("(")[0]  # Nom du module avant la parenthèse
            continue

        # Chercher les ports (input, output, inout)
        if line.startswith("input") or line.startswith("output"):
            parts = line.replace(";", "").split()

            ports.append(parts)

        # Chercher les déclarations "wire"
        if line.startswith("wire"):
            parts = line.replace(";", "").split()
            wire.append(parts)

        # Récupérer les affectations "assign"
        if line.startswith("assign"):
            parts = line.replace(";", "").split()
            assign.append(parts)

    # Retourne les données extraites
    return module_name, ports, wire, assign


def block(module_name):
    # Créer la liste des lignes de stimuli à ajouter
    stimuli_lines = []

    sB = 0
    for k in range(1, 257):  # Itère de 1 à 256 pour sB
        sA = 0
        for i in range(1, 150):  # Itère de 1 à 149 pour sA
            # Formatage des stimuli pour sA et sB
            stimulus = f'sA <= "{format(sA, "08b")}";\n'
            stimulus += f'sB <= "{format(sB, "08b")}";\n'
            stimulus += 'wait for 10 ns;\n'

            # Comparaison de la sortie sO avec la multiplication de sA et sB
            stimulus += f'if (sO = "{format(sA * sB, "016b")}") then\n'
            stimulus += '\tcorrect_outp := correct_outp +1;\n'
            stimulus += 'end if;\n'

            # Écriture dans le fichier de résultats
            stimulus += 'write(file_line, correct_outp);\n'
            stimulus += 'writeline(fptr, file_line);\n'

            # Ajouter chaque stimulus à la liste
            stimuli_lines.append(stimulus)

            sA += 1  # Incrémente sA pour chaque itération
        sB += 1  # Incrémente sB après chaque boucle de sA

    # Retourner les lignes de stimuli générées sous forme de texte
    return "\n".join(stimuli_lines)

def testbench_generation(entity, module_name):
    # Ouvre le fichier de structure du testbench
    vhdl_file = 'test_bench_struct'
    output_file = open(entity, 'w')

    with open(vhdl_file, 'r') as file:
        content = file.readlines()

        # Crée un testbench en remplaçant les placeholders dans le modèle
        for element in content:
            # Remplace le placeholder {stimuli_block} par les stimuli générés par block()
            if "{stimuli_block}" in element:
                stimuli = block(module_name)  # Génère les stimuli
                output_file.write(element.replace("{stimuli_block}", stimuli))
            else:
                # Remplace les autres clés comme {entity} dans le testbench
                output_file.write(element.format(port_in="A, B", port_out="O", entity=module_name))
