# EVAL_META: task_id=61, framework=qpanda2, class=1
import pyqpanda as pq


def create_quantum_circuit_with_one_qubit_and_measure():
    if not hasattr(create_quantum_circuit_with_one_qubit_and_measure, "_machine"):
        create_quantum_circuit_with_one_qubit_and_measure._machine = pq.init_quantum_machine(pq.QMachineType.CPU)

    machine = create_quantum_circuit_with_one_qubit_and_measure._machine
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)

    prog = pq.QProg()
    prog << pq.Measure(q[0], c[0])

    return prog
