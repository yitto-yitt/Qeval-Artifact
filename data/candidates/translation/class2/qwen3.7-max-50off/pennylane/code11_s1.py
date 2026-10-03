# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    if isinstance(circuit, qml.QNode):
        @qml.qnode(circuit.device)
        def state_circuit():
            circuit.func()
            return qml.state()
        return state_circuit()
    elif isinstance(circuit, qml.tape.QuantumTape):
        dev = qml.device("default.qubit", wires=circuit.wires)
        return qml.execute([circuit], dev, gradient_fn=None)[0]
    elif type(circuit).__module__.startswith('qiskit'):
        qfunc = qml.from_qiskit(circuit)
        dev = qml.device("default.qubit", wires=circuit.num_qubits)
        @qml.qnode(dev)
        def state_node():
            qfunc()
            return qml.state()
        return state_node()
    else:
        dev = qml.device("default.qubit", wires=circuit.wires)
        @qml.qnode(dev)
        def state_node():
            circuit()
            return qml.state()
        return state_node()
