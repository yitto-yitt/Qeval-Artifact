# EVAL_META: task_id=6, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QCircuit, QProg, X, I


def create_state_prep(num_qubits):
    if num_qubits < 1:
        raise ValueError("num_qubits must be at least 1")

    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)

    circuit = QCircuit()
    circuit << X(qubits[0])
    for qubit in qubits[1:]:
        circuit << I(qubit)

    program = QProg()
    program << circuit
    machine.directly_run(program)

    create_state_prep.__dict__.setdefault("_resources", []).append(
        (machine, qubits)
    )
    return circuit
