# EVAL_META: task_id=50, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def remove_gate_in_position(circuit, position):
    if isinstance(circuit, list):
        del circuit[position]
    elif hasattr(circuit, 'data'):
        del circuit.data[position]
    else:
        try:
            del circuit[position]
        except Exception:
            pass
    return circuit

machine.finalize()
