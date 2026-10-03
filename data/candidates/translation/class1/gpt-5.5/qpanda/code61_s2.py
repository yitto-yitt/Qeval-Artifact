# EVAL_META: task_id=61, framework=qpanda, class=1
import pyqpanda3.core as pq


def create_quantum_circuit_with_one_qubit_and_measure():
    machine = pq.CPUQVM()
    for init_name in ("init_qvm", "init"):
        if hasattr(machine, init_name):
            getattr(machine, init_name)()
            break

    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)

    prog = pq.QProg()
    if hasattr(pq, "measure"):
        meas = pq.measure(q[0], c[0])
    elif hasattr(pq, "Measure"):
        meas = pq.Measure(q[0], c[0])
    else:
        meas = pq.measure_all(q, c)

    inserted = prog << meas
    if inserted is not None:
        prog = inserted

    if not hasattr(create_quantum_circuit_with_one_qubit_and_measure, "_machines"):
        create_quantum_circuit_with_one_qubit_and_measure._machines = []
    create_quantum_circuit_with_one_qubit_and_measure._machines.append(machine)

    return prog
