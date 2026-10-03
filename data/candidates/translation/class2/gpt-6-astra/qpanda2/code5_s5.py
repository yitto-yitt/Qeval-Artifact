# EVAL_META: task_id=5, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QCircuit, QProg, X, I


def create_state_prep():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)

    circuit = QCircuit()
    circuit << X(qubits[0]) << I(qubits[1])

    program = QProg()
    program << circuit
    machine.directly_run(program)

    if not hasattr(create_state_prep, "_machines"):
        create_state_prep._machines = []
    create_state_prep._machines.append(machine)

    return circuit
