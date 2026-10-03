# EVAL_META: task_id=70, framework=qpanda2, class=3
import pyqpanda as pq
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)
def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    circuit = pq.QCircuit()
    circuit << pq.H(q[0])
    circuit << pq.CSWAP(q[0], q[1], q[2])
    circuit << pq.H(q[1])
    sdg_gate = pq.SDAG(q[0])
    csdg_gate = pq.controlled(sdg_gate, [q[1]])
    circuit << csdg_gate
    return circuit
machine.finalize()
