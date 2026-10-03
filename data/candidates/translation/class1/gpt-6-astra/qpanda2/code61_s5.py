# EVAL_META: task_id=61, framework=qpanda2, class=1
import pyqpanda as pq


def create_quantum_circuit_with_one_qubit_and_measure():
    machine = pq.CPUQVM()
    machine.init_qvm()

    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)
    program = pq.QProg()
    program << pq.Measure(q[0], c[0])

    machine.run_with_configuration(program, c, 1)

    if not hasattr(create_quantum_circuit_with_one_qubit_and_measure, "_machines"):
        create_quantum_circuit_with_one_qubit_and_measure._machines = []
    create_quantum_circuit_with_one_qubit_and_measure._machines.append(machine)

    return program
