# EVAL_META: task_id=81, framework=pennylane, class=3
import re
import pennylane as qml

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""

    wire_map = {}
    next_wire = 0
    operations = []

    for raw_statement in qasm_string.split(";"):
        statement = re.sub(r"//.*", "", raw_statement).strip()
        if not statement:
            continue

        lowered = statement.lower()
        if lowered.startswith("openqasm") or lowered.startswith("include") or lowered.startswith("creg"):
            continue

        qreg_match = re.fullmatch(r"qreg\s+([A-Za-z_]\w*)\[(\d+)\]", statement)
        if qreg_match:
            reg_name = qreg_match.group(1)
            reg_size = int(qreg_match.group(2))
            for idx in range(reg_size):
                wire_map[(reg_name, idx)] = next_wire
                next_wire += 1
            continue

        gate_match = re.fullmatch(r"([A-Za-z_]\w*)\s+(.+)", statement)
        if not gate_match:
            continue

        gate_name = gate_match.group(1).lower()
        qubit_tokens = [token.strip() for token in gate_match.group(2).split(",")]
        wires = []
        for token in qubit_tokens:
            wire_match = re.fullmatch(r"([A-Za-z_]\w*)\[(\d+)\]", token)
            if wire_match:
                wires.append(wire_map[(wire_match.group(1), int(wire_match.group(2)))])

        if gate_name == "h":
            operations.append(qml.Hadamard(wires=wires[0]))
        elif gate_name == "cx":
            operations.append(qml.CNOT(wires=wires))

    return qml.tape.QuantumScript(operations, [])
