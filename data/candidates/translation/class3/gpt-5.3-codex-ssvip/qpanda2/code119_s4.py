# EVAL_META: task_id=119, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be one of: 'full', 'half', 'fixed'")

    a = machine.qAlloc_many(num_state_qubits)
    b = machine.qAlloc_many(num_state_qubits)

    cin = machine.qAlloc_many(1)[0] if kind == "full" else None
    cout = machine.qAlloc_many(1)[0] if kind in ("full", "half") else None
    anc = machine.qAlloc_many(1)[0] if kind == "fixed" else None

    prog = pq.QProg()

    def majority(c, bq, aq):
        circ = pq.QCircuit()
        circ.insert(pq.CNOT(aq, bq))
        circ.insert(pq.CNOT(aq, c))
        circ.insert(pq.Toffoli(c, bq, aq))
        return circ

    def unmajority(c, bq, aq):
        circ = pq.QCircuit()
        circ.insert(pq.Toffoli(c, bq, aq))
        circ.insert(pq.CNOT(aq, c))
        circ.insert(pq.CNOT(c, bq))
        return circ

    if kind == "full":
        c = cin
    elif kind == "half":
        c = machine.qAlloc_many(1)[0]
    else:
        c = anc

    for i in range(num_state_qubits):
        prog.insert(majority(c, b[i], a[i]))
        c = a[i]

    if kind in ("full", "half"):
        prog.insert(pq.CNOT(a[num_state_qubits - 1], cout))

    for i in reversed(range(num_state_qubits)):
        c_in = cin if (kind == "full" and i == 0) else (anc if (kind == "fixed" and i == 0) else (machine.qAlloc_many(1)[0] if (kind == "half" and i == 0) else a[i - 1]))
        prog.insert(unmajority(c_in, b[i], a[i]))

    if kind == "half":
        machine.qFree(c)

    return prog


machine.finalize()
