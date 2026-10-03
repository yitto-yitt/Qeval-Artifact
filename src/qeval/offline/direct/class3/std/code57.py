# EVAL_META: task_id=57, framework=qiskit, class=3


from qiskit import QuantumCircuit

def create_swap_gate():
    circuit = QuantumCircuit(2)
    circuit.cx(0,1)
    circuit.cx(1,0)
    circuit.cx(0,1)
    return circuit


# ==================================================
