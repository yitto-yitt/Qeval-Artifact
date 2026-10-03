# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""
    circuit = QCircuit()
    qregs = {}
    cregs = {}
    gate_lines = []
    for line in qasm_string.replace(';', ';\n').split('\n'):
        line = line.strip().rstrip(';')
        if not line or line.startswith('//') or line.startswith('OPENQASM') or line.startswith('include'):
            continue
        if line.startswith('qreg'):
            parts = line.split()
            reg_ref = parts[1]
            name = reg_ref.split('[')[0]
            size = int(reg_ref.split('[')[1].split(']')[0])
            qregs[name] = size
        elif line.startswith('creg'):
            parts = line.split()
            reg_ref = parts[1]
            name = reg_ref.split('[')[0]
            size = int(reg_ref.split('[')[1].split(']')[0])
            cregs[name] = size
        else:
            gate_lines.append(line)
    
    qubit_regs = {}
    for name, size in qregs.items():
        qubit_regs[name] = circuit.qAlloc_many(size)
    cbit_regs = {}
    for name, size in cregs.items():
        cbit_regs[name] = circuit.cAlloc_many(size)
    
    for line in gate_lines:
        if line.startswith('h '):
            parts = line.split()
            qubit_ref = parts[1]
            reg_name = qubit_ref.split('[')[0]
            index = int(qubit_ref.split('[')[1].split(']')[0])
            circuit << H(qubit_regs[reg_name][index])
        elif line.startswith('cx '):
            parts = line.split()
            targets = parts[1].split(',')
            control_ref = targets[0]
            target_ref = targets[1]
            c_reg = control_ref.split('[')[0]
            c_idx = int(control_ref.split('[')[1].split(']')[0])
            t_reg = target_ref.split('[')[0]
            t_idx = int(target_ref.split('[')[1].split(']')[0])
            circuit << CNOT(qubit_regs[c_reg][c_idx], qubit_regs[t_reg][t_idx])
    
    return circuit
