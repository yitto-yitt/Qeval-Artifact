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
    for statement in qasm_string.split(";"):
        statement = statement.strip()
        if not statement:
            continue
        operation = statement.split()[0]
        if operation in {"OPENQASM", "include", "qreg", "creg"}:
            continue
        qubits = [int(index) for index in re.findall(r"q\[(\d+)\]", statement)]
        if operation == "h":
            circuit << H(qubits[0])
        elif operation == "cx":
            circuit << CNOT(qubits[0], qubits[1])
        else:
            raise ValueError(f"Unsupported QASM statement: {statement}")

    return circuit
