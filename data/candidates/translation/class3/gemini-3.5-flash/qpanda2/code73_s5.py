# EVAL_META: task_id=73, framework=qpanda2, class=3
import pyqpanda as pq

# Initialize CPUQVM and qAlloc_many at the global scope
machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(4)
_global_cbits = machine.cAlloc_many(4)

def x_measurement(circuit, qubit, clbit):
    circuit << pq.H(qubit) << pq.Measure(qubit, clbit)
    return circuit

# Manual Cleanup
machine.finalize()
