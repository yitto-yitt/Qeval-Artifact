# EVAL_META: task_id=50, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, "data"):
        del circuit.data[position]
        return circuit
    if isinstance(circuit, list):
        del circuit[position]
        return circuit
    if hasattr(circuit, "__delitem__"):
        del circuit[position]
        return circuit
    raise TypeError("Unsupported circuit type for gate removal")

machine.finalize()
