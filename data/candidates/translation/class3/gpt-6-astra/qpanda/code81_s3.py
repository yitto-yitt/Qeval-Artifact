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
        if statement.startswith(("OPENQASM", "include", "qreg", "creg")):
            continue

        h_match = re.fullmatch(r"h\s+q\[(\d+)\]", statement)
        cx_match = re.fullmatch(
            r"cx\s+q\[(\d+)\]\s*,\s*q\[(\d+)\]", statement
        )
        if h_match:
            circuit << H(int(h_match.group(1)))
        elif cx_match:
            circuit << CNOT(int(cx_match.group(1)), int(cx_match.group(2)))
        else:
            raise ValueError(f"Unsupported QASM statement: {statement}")

    return circuit
