import verilog_to_vhdl as vtv
import os


if __name__ == "__main__":

    multiplieurs = os.listdir('../python_project/Multipliers')
    output_directory = 'vhdl_file'
    try:
        os.mkdir(output_directory)
        print(f"Directory '{output_directory}' created successfully.")
    except FileExistsError:
        print(f"Directory '{output_directory}' already exists.")

    print(multiplieurs)
    for file in multiplieurs:
        input_path = os.path.join('../python_project/Multipliers', file)
        output_path = os.path.join(output_directory, file.split('.')[0] + '.vhdl')

        if file.endswith('.v'):

            vtv.conversion(input_path, output_path)
