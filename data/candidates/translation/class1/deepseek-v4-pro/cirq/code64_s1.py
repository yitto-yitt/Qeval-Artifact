# EVAL_META: task_id=64, framework=cirq, class=1
import cirq


def simons_algorithm(s):
    n = len(s)
    s_rev = s[::-1]

    reg1_qubits = [cirq.LineQubit(i) for i in range(n)]
    reg2_qubits = [cirq.LineQubit(n + i) for i in range(n)]

    circuit = cirq.Circuit()

    # Apply H to all qubits in the first register
    circuit.append([cirq.H.on(q) for q in reg1_qubits])

    # CNOT from each first-register qubit to the corresponding second-register qubit
    circuit.append([cirq.CNOT(ctrl, targ) for ctrl, targ in zip(reg1_qubits, reg2_qubits)])

    if "1" in s_rev:
        pivot = s_rev.find("1")
        for j in range(n):
            if s_rev[j] == "1":
                circuit.append(cirq.CNOT(reg1_qubits[pivot], reg2_qubits[j]))

    # Apply H again to the first register
    circuit.append([cirq.H.on(q) for q in reg1_qubits])

    # Measure the first register into classical key 'c'
    circuit.append(cirq.measure(*reg1_qubits, key="c"))

    return circuit
