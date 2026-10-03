# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, QProg, X, H

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)
_circuit = None


def create_custom_controlled():
    global _circuit
    if _circuit is None:
        custom = QCircuit()
        custom << X(qubits[1]) << H(qubits[2])

        _circuit = QCircuit()
        _circuit << custom.control([qubits[0], qubits[3]])

        program = QProg()
        program << _circuit
        machine.directly_run(program)

    return _circuit


create_custom_controlled()
machine.finalize()
