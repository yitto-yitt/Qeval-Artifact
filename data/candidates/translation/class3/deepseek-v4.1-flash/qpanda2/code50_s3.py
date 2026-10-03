# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)

def remove_gate_in_position(circuit, position):
    if isinstance(circuit, QCircuit):
        prog = QProg()
        prog << circuit
        was_circuit = True
    else:
        prog = circuit
        was_circuit = False
    
    qasm = convert_qprog_to_qasm(prog)
    lines = qasm.split('\n')
    
    header_keywords = ['OPENQASM', 'include', 'qreg', 'creg']
    header_lines = []
    instruction_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('//'):
            continue
        if any(stripped.startswith(kw) for kw in header_keywords):
            header_lines.append(line)
        else:
            instruction_lines.append(line)
    
    if position < 0 or position >= len(instruction_lines):
        raise IndexError("Position out of range")
    del instruction_lines[position]
    
    new_qasm = '\n'.join(header_lines + instruction_lines) + '\n'
    new_prog = convert_qasm_to_qprog(new_qasm, machine)
    
    if was_circuit:
        new_circuit = QCircuit()
        new_circuit << new_prog
        return new_circuit
    else:
        return new_prog

machine.finalize()
