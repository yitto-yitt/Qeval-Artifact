# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    if hasattr(circuit, 'wires'):
        wires = list(circuit.wires)
        num_qubits = len(wires)
        wire_order = wires
    else:
        num_qubits = 2
        wire_order = list(range(num_qubits))
    op_or = qml.matrix(circuit, wire_order=wire_order)
    qc_list = []
    counter = 0
    while counter < n:
        with qml.tape.QuantumTape() as qc:
            for _ in range(np.random.randint(num_qubits * 2, num_qubits * 5)):
                g = np.random.choice(['H', 'S', 'CX'])
                if g == 'H':
                    w = np.random.randint(0, num_qubits)
                    qml.Hadamard(wires=w)
                elif g == 'S':
                    w = np.random.randint(0, num_qubits)
                    qml.S(wires=w)
                else:
                    ws = np.random.choice(num_qubits, 2, replace=False)
                    qml.CNOT(wires=ws.tolist())
        op_qc = qml.matrix(qc, wire_order=wire_order)
        equiv = False
        for phase in [1, -1, 1j, -1j]:
            if np.allclose(op_qc, phase * op_or, rtol=0.4, atol=0.4):
                equiv = True
                break
        if equiv:
            counter += 1
            qc_list.append(qc)
    return qc_list
