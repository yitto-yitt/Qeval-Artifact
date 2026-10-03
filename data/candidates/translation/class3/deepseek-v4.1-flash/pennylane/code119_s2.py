# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    if kind == 'full':
        num_qubits = 2 * n + 1
        wires = list(range(num_qubits))
        a = wires[:n]
        b = wires[n:2*n]
        c = wires[2*n]
        circuit = qml.QuantumCircuit(wires=wires)
        with circuit:
            qml.CNOT(wires=[c, b[0]])
            for i in range(n):
                qml.CNOT(wires=[a[i], b[i]])
            for i in range(n - 1):
                qml.Toffoli(wires=[b[i], a[i], a[i + 1]])
            qml.Toffoli(wires=[b[n - 1], a[n - 1], c])
            for i in range(n - 1, 0, -1):
                qml.CNOT(wires=[a[i], b[i]])
                qml.Toffoli(wires=[b[i - 1], a[i - 1], a[i]])
            qml.CNOT(wires=[a[0], b[0]])
        return circuit
    elif kind == 'half':
        num_qubits = 2 * n + 1
        wires = list(range(num_qubits))
        a = wires[:n]
        b = wires[n:2*n]
        c = wires[2*n]
        circuit = qml.QuantumCircuit(wires=wires)
        with circuit:
            for i in range(n):
                qml.CNOT(wires=[a[i], b[i]])
            for i in range(n - 1):
                qml.Toffoli(wires=[b[i], a[i], a[i + 1]])
            qml.Toffoli(wires=[b[n - 1], a[n - 1], c])
            for i in range(n - 1, 0, -1):
                qml.CNOT(wires=[a[i], b[i]])
                qml.Toffoli(wires=[b[i - 1], a[i - 1], a[i]])
            qml.CNOT(wires=[a[0], b[0]])
        return circuit
    elif kind == 'fixed':
        num_qubits = 2 * n
        wires = list(range(num_qubits))
        a = wires[:n]
        b = wires[n:2*n]
        circuit = qml.QuantumCircuit(wires=wires)
        with circuit:
            for i in range(n):
                qml.CNOT(wires=[a[i], b[i]])
            for i in range(n - 1):
                qml.Toffoli(wires=[b[i], a[i], a[i + 1]])
            for i in range(n - 1, 0, -1):
                qml.CNOT(wires=[a[i], b[i]])
                qml.Toffoli(wires=[b[i - 1], a[i - 1], a[i]])
            qml.CNOT(wires=[a[0], b[0]])
        return circuit
    else:
        raise ValueError(f"Unknown kind: {kind}")
