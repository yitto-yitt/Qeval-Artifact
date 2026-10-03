# EVAL_META: task_id=112, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = _global_qubits[:n]
    prog = pq.QProg()

    for pauli_string, t in zip(pauli_strings, times):
        for _ in range(reps):
            for i, p in enumerate(pauli_string):
                if p == 'I':
                    continue
                if p == 'X':
                    prog.insert(pq.RX(qubits[i], 2.0 * t / reps))
                elif p == 'Y':
                    prog.insert(pq.RY(qubits[i], 2.0 * t / reps))
                elif p == 'Z':
                    prog.insert(pq.RZ(qubits[i], 2.0 * t / reps))
                else:
                    raise ValueError("Invalid Pauli character: {}".format(p))
    return prog

machine.finalize()
