# EVAL_META: task_id=73, framework=qpanda2, class=3
import pyqpanda as pq

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)
c = machine.cAlloc_many(4)

def x_measurement(circuit, qubit, clbit):
    circuit << pq.H(qubit) << pq.Measure(qubit, clbit)
    return circuit

# Manual Cleanup
machine.finalize()
