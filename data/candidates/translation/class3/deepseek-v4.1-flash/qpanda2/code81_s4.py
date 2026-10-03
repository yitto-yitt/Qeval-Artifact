# EVAL_META: task_id=81, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
atexit.register(machine.finalize)

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""
    circuit = QCircuit()
    for line in qasm_string.split('\n'):
        line = line.strip()
        if not line or line.startswith('OPENQASM') or line.startswith('include') or line.startswith('qreg') or line.startswith('creg'):
            continue
        if line.startswith('h '):
            qubit_str = line[2:].strip(' ;')
            idx = int(qubit_str[2])
            circuit << H(qubits[idx])
        elif line.startswith('cx '):
            parts = line[3:].strip(' ;').split(',')
            q0 = int(parts[0].strip()[2])
            q1 = int(parts[1].strip()[2])
            circuit << CNOT(qubits[q0], qubits[q1])
    return circuit
