# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    
    if kind == 'full':
        cin = 0
        a = list(range(1, n + 1))
        b = list(range(n + 1, 2 * n + 1))
        cout = 2 * n + 1
    elif kind == 'half':
        cin = 2 * n + 1
        a = list(range(0, n))
        b = list(range(n, 2 * n))
        cout = 2 * n
    elif kind == 'fixed':
        cin = 2 * n
        a = list(range(0, n))
        b = list(range(n, 2 * n))
        cout = None
    else:
        raise ValueError("Invalid kind")

    with qml.tape.QuantumTape() as tape:
        c = cin
        for i in range(n):
            x = a[i]
            y = b[i]
            qml.CNOT(wires=[x, y])
            qml.CNOT(wires=[x, c])
            qml.Toffoli(wires=[c, x, y])
            c = y
            
        if cout is not None:
            qml.CNOT(wires=[b[-1], cout])
            
        for i in reversed(range(n - 1)):
            c = b[i] if i > 0 else cin
            x = a[i + 1]
            y = b[i + 1]
            qml.Toffoli(wires=[c, x, y])
            qml.CNOT(wires=[x, c])
            qml.CNOT(wires=[c, y])
            
        c = cin
        x = a[0]
        y = b[0]
        qml.Toffoli(wires=[c, x, y])
        qml.CNOT(wires=[x, c])
        qml.CNOT(wires=[c, y])

    return tape
