# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    a_wires = list(range(n))
    b_wires = list(range(n, 2 * n))
    
    if kind == 'full':
        cin_wire = 2 * n
        cout_wire = 2 * n + 1
        total_wires = 2 * n + 2
    else:
        cout_wire = 2 * n
        total_wires = 2 * n + 1

    with qml.tape.QuantumTape() as tape:
        if kind == 'full':
            qml.CNOT(wires=[a_wires[0], b_wires[0]])
            qml.CNOT(wires=[a_wires[0], cin_wire])
            qml.Toffoli(wires=[cin_wire, b_wires[0], a_wires[0]])
        else:
            qml.CNOT(wires=[a_wires[0], b_wires[0]])
            
        for i in range(1, n):
            qml.CNOT(wires=[a_wires[i], b_wires[i]])
            qml.CNOT(wires=[a_wires[i], a_wires[i-1]])
            qml.Toffoli(wires=[a_wires[i-1], b_wires[i], a_wires[i]])
            
        qml.CNOT(wires=[a_wires[-1], cout_wire])
        
        for i in range(n - 1, 0, -1):
            qml.Toffoli(wires=[a_wires[i-1], b_wires[i], a_wires[i]])
            qml.CNOT(wires=[a_wires[i], a_wires[i-1]])
            qml.CNOT(wires=[a_wires[i-1], b_wires[i]])
            
        if kind == 'full':
            qml.Toffoli(wires=[cin_wire, b_wires[0], a_wires[0]])
            qml.CNOT(wires=[a_wires[0], cin_wire])
            qml.CNOT(wires=[cin_wire, b_wires[0]])
        else:
            qml.CNOT(wires=[a_wires[0], b_wires[0]])

    return tape
