# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    a = list(range(n))
    b = list(range(n, 2 * n))
    
    if kind == "full":
        cin = 2 * n
        cout = 2 * n + 1
    elif kind == "half":
        cout = 2 * n
    elif kind == "fixed":
        pass
    else:
        raise ValueError(f"Unknown kind: {kind}")

    with qml.tape.QuantumTape() as tape:
        if kind == "full":
            qml.CNOT(wires=[cin, b[0]])
            qml.CNOT(wires=[cin, a[0]])
            qml.Toffoli(wires=[a[0], b[0], cin])
            
        for i in range(1, n):
            qml.CNOT(wires=[a[i-1], b[i]])
            qml.CNOT(wires=[a[i-1], a[i]])
            qml.Toffoli(wires=[a[i], b[i], a[i-1]])
            
        if kind in ["full", "half"]:
            qml.CNOT(wires=[a[n-1], cout])
            
        for i in range(n - 1, 0, -1):
            qml.Toffoli(wires=[a[i], b[i], a[i-1]])
            qml.CNOT(wires=[a[i-1], a[i]])
            qml.CNOT(wires=[a[i], b[i]])
            
        if kind == "full":
            qml.Toffoli(wires=[a[0], b[0], cin])
            qml.CNOT(wires=[cin, a[0]])
            qml.CNOT(wires=[a[0], b[0]])
        else:
            qml.CNOT(wires=[a[0], b[0]])
            
    return tape
