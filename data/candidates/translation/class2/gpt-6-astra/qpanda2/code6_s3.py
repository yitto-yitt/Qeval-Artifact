# EVAL_META: task_id=6, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep(num_qubits):
    if num_qubits < 1:
        raise ValueError("num_qubits must be at least 1")

    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)

    circuit = pq.QCircuit()
    circuit << pq.X(qubits[0])
    for qubit in qubits[1:]:
        circuit << pq.I(qubit)

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)

    if not hasattr(create_state_prep, "_machines"):
        create_state_prep._machines = []
    create_state_prep._machines.append(machine)

    return circuit
