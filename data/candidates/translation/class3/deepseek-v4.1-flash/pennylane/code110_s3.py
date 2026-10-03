# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    if isinstance(circuit, qml.tape.QuantumTape):
        tape_in = circuit
    elif isinstance(circuit, qml.QNode):
        tape_in = qml.tape.make_qscript(circuit.func)()
    elif callable(circuit):
        tape_in = qml.tape.make_qscript(circuit)()
    else:
        raise ValueError("Unsupported circuit type")
    
    wires = list(tape_in.wires)
    U = qml.matrix(tape_in, wire_order=wires)
    
    qc_list = []
    while len(qc_list) < n:
        with qml.tape.QuantumTape() as tape:
            depth = np.random.randint(1, 10)
            for _ in range(depth):
                gate = np.random.choice(['h', 's', 'cnot'])
                if gate == 'h':
                    w = np.random.choice(wires)
                    qml.Hadamard(wires=w)
                elif gate == 's':
                    w = np.random.choice(wires)
                    qml.S(wires=w)
                elif gate == 'cnot':
                    if len(wires) >= 2:
                        w1, w2 = np.random.choice(wires, size=2, replace=False)
                        qml.CNOT(wires=[w1, w2])
        V = qml.matrix(tape, wire_order=wires)
        overlap = np.vdot(V, U)
        phase = overlap / (V.shape[0])
        if np.allclose(U, phase * V, rtol=0.4, atol=0.4):
            qc_list.append(tape)
    return qc_list
