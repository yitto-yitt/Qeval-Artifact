# EVAL_META: task_id=5, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)

    circuit = pq.QCircuit()
    circuit << pq.X(qubits[0]) << pq.I(qubits[1])

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)

    if not hasattr(create_state_prep, "_machines"):
        create_state_prep._machines = []
    create_state_prep._machines.append(machine)

    return circuit
