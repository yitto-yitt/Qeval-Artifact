# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, X, H, qAlloc_many

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(4)


def create_custom_controlled():
    controls = [qubits[0], qubits[3]]

    x_gate = X(qubits[1])
    x_gate.set_control(controls)

    h_gate = H(qubits[2])
    h_gate.set_control(controls)

    circuit = QCircuit()
    circuit << x_gate
    circuit << h_gate

    return circuit


create_custom_controlled()
machine.finalize()
