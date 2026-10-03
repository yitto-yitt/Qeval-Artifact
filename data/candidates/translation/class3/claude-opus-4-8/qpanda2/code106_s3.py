# EVAL_META: task_id=106, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def _build_circuit():
    circ = pq.QCircuit()
    circ << pq.CNOT(qubits[0], qubits[1])
    circ << pq.T(qubits[0])
    return circ


def compose_cnot_dihedral():
    composed = pq.QCircuit()

    # First element: cx(0,1), t(0)
    composed << pq.CNOT(qubits[0], qubits[1])
    composed << pq.T(qubits[0])

    # Second element: cx(0,1), t(0), x(1)
    composed << pq.CNOT(qubits[0], qubits[1])
    composed << pq.T(qubits[0])
    composed << pq.X(qubits[1])

    prog = pq.QProg()
    prog << composed

    result = machine.prob_run_dict(prog, qubits, -1)
    return result


if __name__ == "__main__":
    print(compose_cnot_dihedral())
    machine.finalize()
