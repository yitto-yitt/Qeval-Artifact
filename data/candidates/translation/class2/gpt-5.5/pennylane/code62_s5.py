# EVAL_META: task_id=62, framework=pennylane, class=2
import pennylane as qml


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    ops = []
    for i in range(len(basis)):
        if state[i] == 1:
            ops.append(qml.PauliX(wires=i))
        if basis[i] == 1:
            ops.append(qml.Hadamard(wires=i))

    class _BB84SendersCircuit(qml.tape.QuantumScript):
        @property
        def wires(self):
            return qml.wires.Wires(range(num_qubits))

    return _BB84SendersCircuit(ops, [])
