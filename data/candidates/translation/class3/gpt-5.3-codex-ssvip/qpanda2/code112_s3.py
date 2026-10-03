# EVAL_META: task_id=112, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    q = _global_qubits[:n]
    prog = pq.QProg()

    for pauli_string, t in zip(pauli_strings, times):
        for _ in range(reps):
            for i, p in enumerate(pauli_string):
                if p == 'I':
                    continue
                elif p == 'X':
                    prog << pq.RX(q[i], 2.0 * t / reps)
                elif p == 'Y':
                    prog << pq.RY(q[i], 2.0 * t / reps)
                elif p == 'Z':
                    prog << pq.RZ(q[i], 2.0 * t / reps)
                else:
                    raise ValueError("Invalid Pauli character: {}".format(p))
    machine.finalize()
    return prog
