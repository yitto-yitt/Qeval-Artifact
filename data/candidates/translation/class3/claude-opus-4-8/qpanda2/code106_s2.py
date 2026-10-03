# EVAL_META: task_id=106, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def compose_cnot_dihedral():
    prog = pq.QProg()

    # circ1: cx(0,1), t(0)
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.T(qubits[0])

    # circ2 (composed): same as circ1 plus x(1)
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.T(qubits[0])
    prog << pq.X(qubits[1])

    machine.directly_run(prog)
    result = machine.get_qstate()

    machine.finalize()
    return result


if __name__ == "__main__":
    print(compose_cnot_dihedral())
