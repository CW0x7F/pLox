# this script file is only used to generate AST with meta programming

import sys

if len(sys.argv) != 2:
    sys.exit(2)

KEY_ELES = {
    'Binary':['left','operator','right'],
    'Literal':['value'],
    'Unary':['operator','right'],
    'Grouping':['expr']

}

with open(sys.argv[1],'w',encoding='utf-8') as f:

    f.write(f"class Expr:\n")
    f.write(f"   pass\n\n")

    for each in KEY_ELES:
        f.write(f"class {each}(Expr):\n")
        f.write(f"   def __init__(self,")        
        for param in KEY_ELES[each]:
            f.write(f" {param},")
        f.write(f"):\n")

        for param in KEY_ELES[each]:
            f.write(f"      self.{param} = {param}\n")

        f.write("\n\n")


