# EVAL_META: task_id=50, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(32)

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, "remove_gate"):
        circuit.remove_gate(position)
    elif hasattr(circuit, "delete_gate"):
        circuit.delete_gate(position)
    elif hasattr(circuit, "get_qgate_num") and hasattr(circuit, "get_gate"):
        total = circuit.get_qgate_num()
        prog = pq.QProg()
        for i in range(total):
            if i != position:
                prog << circuit.get_gate(i)
        circuit = prog
    else:
        try:
            del circuit[position]
        except Exception:
            pass
    return circuit

machine.finalize()
