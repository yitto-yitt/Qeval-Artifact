# EVAL_META: task_id=6, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QCircuit, QProg, X


def create_state_prep(num_qubits):
    if num_qubits < 1:
        raise ValueError("num_qubits must be positive")

    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)

    circuit = QCircuit()
    circuit << X(qubits[0])

    program = QProg()
    program << circuit
    machine.directly_run(program)

    if not hasattr(create_state_prep, "_resources"):
        create_state_prep._resources = []
    create_state_prep._resources.append((machine, qubits, program))
    return circuit
