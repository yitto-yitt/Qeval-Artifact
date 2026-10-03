# EVAL_META: task_id=44, framework=qiskit, class=3


from qiskit import QuantumCircuit

def tensor_circuits():
    top = QuantumCircuit(1)
    top.x(0)
    bottom = QuantumCircuit(2)
    bottom.cry(0.2, 0, 1)
    tensored = bottom.tensor(top)
    return tensored


# ==================================================
