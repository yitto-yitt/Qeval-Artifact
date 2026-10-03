# EVAL_META: task_id=4, framework=qpanda2, class=3
import pyqpanda

machine = pyqpanda.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_unitary_from_matrix():
    circ = pyqpanda.QCircuit()
    circ << pyqpanda.CNOT(q[1], q[0])
    circ << pyqpanda.X(q[0])
    circ << pyqpanda.X(q[1])
    return circ

machine.finalize()
