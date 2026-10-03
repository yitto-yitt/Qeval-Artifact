# EVAL_META: task_id=99, framework=qpanda2, class=3
import re
from pyqpanda import *

# Initialize global QVM
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(100)
c = machine.cAlloc_many(100)

def remove_unassigned_parameterized_gates(circuit):
    if isinstance(circuit, QCircuit) or isinstance(circuit, QGate):
        prog = QProg()
        prog.insert(circuit)
    else:
        prog = circuit

    ir_str = transform_qprog_to_originir(prog, machine)
    
    lines = ir_str.split('\n')
    new_lines = []
    
    def is_float(val_str):
        try:
            float(val_str)
            return True
        except ValueError:
            return False

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        # Find parameters in parentheses
        params = re.findall(r'\(([^)]+)\)', line_stripped)
        if params:
            all_floats = True
            for param in params:
                param_clean = param.strip()
                if not is_float(param_clean):
                    all_floats = False
                    break
            if not all_floats:
                continue # Skip this gate
        
        new_lines.append(line)
        
    new_ir_str = '\n'.join(new_lines)
    new_prog = transform_originir_to_qprog(new_ir_str, machine)
    
    return new_prog

# Manual Cleanup
machine.finalize()
