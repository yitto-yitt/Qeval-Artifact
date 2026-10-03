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

    program = QProg()
    registers = {}
    next_qubit = 0

    for statement in qasm_string.split(";"):
        statement = statement.strip()
        if not statement:
            continue

        declaration = re.fullmatch(r"qreg\s+(\w+)\[(\d+)\]", statement)
        if declaration:
            name, size = declaration.groups()
            size = int(size)
            registers[name] = list(range(next_qubit, next_qubit + size))
            next_qubit += size
            continue

        if statement.startswith(("OPENQASM ", "include ", "creg ")):
            continue

        gate, operands = statement.split(None, 1)
        qubits = [
            registers[name][int(index)]
            for name, index in re.findall(r"(\w+)\[(\d+)\]", operands)
        ]

        if gate == "h":
            program.append(H(qubits[0]))
        elif gate == "cx":
            program.append(CNOT(qubits[0], qubits[1]))
        else:
            raise ValueError(f"Unsupported QASM instruction: {statement}")

    return program
