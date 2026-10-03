# EVAL_META: task_id=81, framework=qpanda, class=3
import re
from pyqpanda3.core import QProg, H, CNOT

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""

    circuit = QProg()
    pattern = r"\b(h|cx)\s+q\[(\d+)\](?:\s*,\s*q\[(\d+)\])?\s*;"
    for instruction in re.finditer(pattern, qasm_string):
        gate, first, second = instruction.groups()
        if gate == "h":
            circuit << H(int(first))
        else:
            circuit << CNOT(int(first), int(second))
    return circuit
