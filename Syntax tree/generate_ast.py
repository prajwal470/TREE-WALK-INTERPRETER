import os

def define_ast(output_dir, base_name, types):
    path = os.path.join(output_dir, f"{base_name.lower()}.py")
    with open(path, "w") as f:
        f.write("from abc import ABC, abstractmethod\n")
        f.write("from dataclasses import dataclass\n")
        f.write("from typing import Any, Protocol\n")
        f.write("from token import Token\n\n\n")  # ✅ Import Token properly

        # Base AST class
        f.write(f"class {base_name}(ABC):\n")
        f.write("    def accept(self, visitor):\n")
        f.write("        raise NotImplementedError()\n\n\n")

        # Visitor interface
        f.write(f"class {base_name}Visitor(Protocol):\n")
        for class_def in types:
            class_name = class_def.split(":")[0].strip()
            f.write(f"    def visit_{class_name.lower()}_{base_name.lower()}(self, "
                    f"{base_name.lower()}: '{class_name}') -> Any:\n")
            f.write("        ...\n")
        f.write("\n")

        # Subclasses
        for class_def in types:
            class_name, fields = map(str.strip, class_def.split(":"))
            define_type(f, base_name, class_name, fields)

def define_type(f, base_name, class_name, field_list):
    f.write(f"@dataclass\n")
    f.write(f"class {class_name}({base_name}):\n")
    fields = [field.strip() for field in field_list.split(",")]
    for field in fields:
        name, type_ = map(str.strip, field.split(" "))
        f.write(f"    {name}: {type_}\n")
    f.write("\n")
    f.write(f"    def accept(self, visitor: {base_name}Visitor):\n")
    f.write(f"        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n\n")

def main():
    output_dir = "."
    define_ast(output_dir, "Expr", [
        "Binary   : left Expr, operator Token, right Expr",
        "Grouping : expression Expr",
        "Literal  : value Any",
        "Unary    : operator Token, right Expr",
    ])

if __name__ == "__main__":
    main()