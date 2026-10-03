# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import init_quantum_machine, destroy_quantum_machine, QVM, QProg, QMachineType, Measure

def init_random_3qubit(desired_vector):
    init_quantum_machine(QMachineType.CPU)
    qvm = QVM()
    qvm.set_random_seed(42)

    # allocate qubits in reverse order: q[0] (q2), q[1] (q1), q[2] (q0)
    q = [qvm.qAlloc() for _ in range(3)]
    c = [qvm.cAlloc() for _ in range(3)]

    # set the initial statevector (same little‑endian ordering: q0 LSB, q2 MSB)
    qvm.init_qvm_state(desired_vector)

    prog = QProg()
    for i in range(3):
        prog << Measure(q[i], c[i])

    shots = 1024
    counts = qvm.run_with_configuration(prog, c, shots)

    total = sum(counts.values())
    prob_dist = {key: value / total for key, value in counts.items()}

    destroy_quantum_machine()
    return prob_dist
