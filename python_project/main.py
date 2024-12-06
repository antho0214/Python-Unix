import os
import verilog_to_vhdl as vtv


def save_results(module_name, error_probability, cost):
    # Créer le dossier vcd si ce n'est pas déjà fait
    output_dir = "vcd"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Définir le chemin du fichier de sortie dans le dossier vcd
    output_path = os.path.join(output_dir, f"{module_name}.vcd")

    # Ouvrir le fichier en mode écriture
    with open(output_path, 'w') as file:
        # Écrire les résultats dans le fichier
        file.write(f"Module: {module_name}\n")
        file.write(f"Error Probability: {error_probability}\n")
        file.write(f"Cost: {cost}\n")

    # Confirmation de la sauvegarde
    print(f"Les résultats ont été sauvegardés dans {output_path}")


if __name__ == "__main__":

    multiplieurs = os.listdir('../python_project/Multipliers')
    output_directory = 'vhdl_file'

    # Créez le dossier vhdl_file s'il n'existe pas
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Directory '{output_directory}' created successfully.")
    else:
        print(f"Directory '{output_directory}' already exists.")

    print(multiplieurs)
    for file in multiplieurs:
        input_path = os.path.join('../python_project/Multipliers', file)
        output_path = os.path.join(output_directory, file.split('.')[0] + '.vhdl')

        if file.endswith('.v'):
            boolean_counter = 10
            module_name = vtv.conversion(input_path, output_path)
            print("Module name: ", module_name)

            # Run the GHDL simulation using the converted VHDL entity
            os.system(f"ghdl -a --ieee=synopsys {output_path}")  # Analyze the VHDL files
            print("1")
            os.system(f"ghdl -e --ieee=synopsys {module_name}")  # Elaborate the top-level entity
            print("2")
            # Générer le fichier VCD dans le dossier vcd
            vcd_path = os.path.join("vcd", f"{module_name}.vcd")
            os.system(f"ghdl -r --ieee=synopsys {module_name} --stop-time=600ns --vcd={vcd_path}")
            print("3")

            # Read the results of the simulation (assuming output in a VCD file)
            result_file = f"{module_name}.vcd"  # Output VCD file from GHDL
            print(f"VCD result file: {result_file}")


            # Assuming you have a cost value (replace with actual logic to compute cost)
            cost = boolean_counter
