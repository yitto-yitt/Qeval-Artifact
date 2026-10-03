# EVAL_META: task_id=50, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, 'data'):
        del circuit.data[position]
    else:
        del circuit[position]
    return circuit

machine.finalize()
