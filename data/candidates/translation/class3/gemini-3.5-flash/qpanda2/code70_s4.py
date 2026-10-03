# EVAL_META: task_id=70, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    circuit = pq.QCircuit()
    circuit << pq.H(q[0]) \
            << pq.CSWAP(q[0], q[1], q[2]) \
            << pq.H(q[1]) \
            << pq.S(q[0]).dagger().control([q[1]])
    return circuit

machine.finalize()
