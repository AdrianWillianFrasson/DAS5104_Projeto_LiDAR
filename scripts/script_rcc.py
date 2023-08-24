import os


INPUT_PATH = "..\\assets\\assets.qrc"
OUTPUT_PATH = "..\\src\\interface\\assets_rc.py"


def main():
    input_path = os.path.join(os.path.dirname(__file__), INPUT_PATH)
    output_path = os.path.join(os.path.dirname(__file__), OUTPUT_PATH)

    cmd = f"pyside6-rcc {input_path} -o {output_path}"
    print(f"-> {cmd}")
    os.system(cmd)


if __name__ == '__main__':
    main()
