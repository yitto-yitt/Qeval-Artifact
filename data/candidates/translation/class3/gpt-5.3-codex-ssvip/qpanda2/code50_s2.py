# EVAL_META: task_id=50, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, "delete_gate"):
        circuit.delete_gate(position)
        return circuit
    if hasattr(circuit, "remove_gate"):
        circuit.remove_gate(position)
        return circuit
    if hasattr(circuit, "m_prog") and hasattr(circuit.m_prog, "delete_gate"):
        circuit.m_prog.delete_gate(position)
        return circuit
    if hasattr(circuit, "prog") and hasattr(circuit.prog, "delete_gate"):
        circuit.prog.delete_gate(position)
        return circuit
    raise AttributeError("The provided circuit object does not support gate removal by position.")

machine.finalize()
