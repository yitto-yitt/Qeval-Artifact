# EVAL_META: task_id=50, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init()
qubits = machine.qAlloc_many(32)

def remove_gate_in_position(circuit, position):
    del circuit[position]
    return circuit

machine.finalize()
