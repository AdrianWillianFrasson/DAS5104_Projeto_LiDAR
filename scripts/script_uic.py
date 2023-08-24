import os


INPUT_PATH = "..\\QT\\"
OUTPUT_PATH = "..\\src\\interface\\"


def main():
    input_path = os.path.join(os.path.dirname(__file__), INPUT_PATH)
    output_path = os.path.join(os.path.dirname(__file__), OUTPUT_PATH)

    files = [path for path in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, path))]

    for file in files:

        if file.endswith(".ui"):
            input_file = os.path.join(input_path, file)
            output_file = os.path.join(output_path, f"{file[:-3]}_ui.py")

            cmd = f"pyside6-uic {input_file} -o {output_file} --from-imports --star-imports"
            print(f"-> {file}")
            os.system(cmd)


if __name__ == '__main__':
    main()
