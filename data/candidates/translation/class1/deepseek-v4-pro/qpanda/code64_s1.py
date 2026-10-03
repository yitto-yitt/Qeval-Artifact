# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, qubit_allocation, cbit_allocation, H, CNOT, BARRIER, MEASURE

def simons_algorithm(s):
    n = len(s)
    s_rev = s[::-1]  # reverse as in reference Qiskit code
    if n == 0:
        return QCircuit()
    # allocate qubits and classical bits
    q_reg1 = qubit_allocation(n)          # register 1
    q_reg2 = qubit_allocation(n)          # register 2
    c_reg  = cbit_allocation(n, "c")      # classical register named 'c'
    circuit = QCircuit()
    # Hadamard on reg1
    for qubit in q_reg1:
        circuit << H(qubit)
    # Barrier on all qubits
    all_qubits = list(q_reg1) + list(q_reg2)
    circuit << BARRIER(all_qubits)
    # element‑wise CNOT from reg1 to reg2
    for i in range(n):
        circuit << CNOT(q_reg1[i], q_reg2[i])
    # additional CNOTs if s_rev contains a '1'
    if "1" in s_rev:
        i0 = s_rev.find("1")
        for j in range(n):
            if s_rev[j] == "1":
                circuit << CNOT(q_reg1[i0], q_reg2[j])
    # Barrier again
    circuit << BARRIER(all_qubits)
    # Hadamard on reg1
    for qubit in q_reg1:
        circuit << H(qubit)
    # measure reg1 into classical register
    for i in range(n):
        circuit << MEASURE(q_reg1[i], c_reg[i])
    return circuit
