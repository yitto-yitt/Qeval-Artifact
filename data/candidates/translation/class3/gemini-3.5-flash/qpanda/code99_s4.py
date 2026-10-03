# EVAL_META: task_id=99, framework=qpanda, class=3
import re
from pyqpanda3.core import CPUQVM, QProg, to_originir, convert_originir_str_to_qprog

def remove_unassigned_parameterized_gates(circuit):
    machine = CPUQVM()
    machine.init_qvm()
    
    prog = QProg()
    prog << circuit
    
    ir_str = to_originir(prog, machine)
    
    lines = ir_str.split('\n')
    new_lines = []
    
    def is_float(val_str):
        val_str = val_str.strip()
        match = re.match(r'^[+-]?[0-9]*\.?[0-9]+([eE][+-]?[0-9]+)?$', val_str)
        return match is not None

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        match = re.search(r'\(([^)]+)\)', line_stripped)
        if match:
            param_str = match.group(1)
            params = param_str.split(',')
            has_unassigned = False
            for p in params:
                if not is_float(p):
                    has_unassigned = True
                    break
            if has_unassigned:
                continue
        
        new_lines.append(line)
        
    new_ir_str = '\n'.join(new_lines)
    
    new_prog = convert_originir_str_to_qprog(new_ir_str, machine)
    return new_prog
