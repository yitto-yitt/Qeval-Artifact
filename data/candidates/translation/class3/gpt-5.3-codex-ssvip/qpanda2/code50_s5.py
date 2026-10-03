# EVAL_META: task_id=50, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_q = machine.qAlloc_many(1)

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, "remove_gate"):
        circuit.remove_gate(position)
        return circuit
    if hasattr(circuit, "delete_gate"):
        circuit.delete_gate(position)
        return circuit
    if hasattr(circuit, "m_prog") and hasattr(circuit.m_prog, "remove_gate"):
        circuit.m_prog.remove_gate(position)
        return circuit
    if hasattr(circuit, "m_prog") and hasattr(circuit.m_prog, "delete_gate"):
        circuit.m_prog.delete_gate(position)
        return circuit
    raise AttributeError("Unsupported circuit object: cannot remove gate by position.")

machine.finalize()
