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
        if not statement or statement.startswith(
            ("OPENQASM ", "include ", "qreg ", "creg ")
        ):
            continue

        match = re.fullmatch(r"h\s+q\[(\d+)\]", statement)
        if match:
            circuit << H(int(match.group(1)))
            continue

        match = re.fullmatch(r"cx\s+q\[(\d+)\]\s*,\s*q\[(\d+)\]", statement)
        if match:
            circuit << CNOT(int(match.group(1)), int(match.group(2)))
            continue

        raise ValueError(f"Unsupported QASM statement: {statement}")

    return circuit
