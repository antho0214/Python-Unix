def conversion(verilog_file, vhdl_file):
    boolean_counter = 0
    # Traite le fichier Verilog et obtient les informations nécessaires
    module_name, ports, wire, assign = traitement_verilog(verilog_file)

    # Ouvre le fichier VHDL pour l'écriture
    with open(vhdl_file, 'w') as file:
        # Écrit la déclaration de l'entité VHDL
        file.write(f"entity {module_name} is\n")


        # Gestion des ports
        file.write("port (")
        for element in ports:
            downto = element[1].split(":")
            print("aaa",downto[0][1:])
            print("b", downto[1][:1])
            if element[0] == 'input':
                file.write(f"{element[2]} : in std_logic_vector ({downto[0][1:]} downto {downto[1][:1]});\n")
            elif element[0] == 'output':
                file.write(f"{element[2]} : out std_logic_vector ({downto[0][1:]} downto {downto[1][:1]})\n")
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
            vhdl_line = vhdl_line.rstrip(";")
            file.write(f"{vhdl_line};\n")
            boolean_counter += 1
        print(f"{boolean_counter} boolean operators were created")
        file.write(f"end {full_adder_struct};\n")
        testbench_generation('test1')


def traitement_verilog(verilog_file):
    try :
        # Lis le fichier Verilog
        with open(verilog_file, 'r') as file:
            lines = file.readlines()
    except Exception as e:
        print(e)

    # Initialisation des variables
    module_name = None
    global ports
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
            print(parts)
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


def testbench_generation(entity):
    print("aaa",ports)

    vhdl_file = 'test_bench_struct'
    output_file = open(entity, 'w')
    with open(vhdl_file, 'r') as file:
        content = file.readlines()
        #print(content)
        for element in content:
            #print(element)
            output_file.write(element.format(entity = entity))

        for element in ports:
            port = element[2]
            print(port)
            output_file.write(element.format(port_in = port, port_out = port))










