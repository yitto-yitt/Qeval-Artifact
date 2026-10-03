# EVAL_META: task_id=6, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QCircuit, QProg, X, I


def create_state_prep(num_qubits):
    if not isinstance(num_qubits, int) or num_qubits < 1:
        raise ValueError("num_qubits must be a positive integer")

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

    if not hasattr(create_state_prep, "_machines"):
        create_state_prep._machines = []
    create_state_prep._machines.append(machine)

    return circuit
