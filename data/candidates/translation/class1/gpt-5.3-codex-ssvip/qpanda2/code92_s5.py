# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq

def calculate_stabilizer_state_info():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    prog << pq.measure_all(q, c)

    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)

    probabilities = {}
    for bitstr, cnt in counts.items():
        probabilities[bitstr] = cnt / shots

    pq.destroy_quantum_machine(machine)
    return probabilities
