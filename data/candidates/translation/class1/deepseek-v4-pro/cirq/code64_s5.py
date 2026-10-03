# EVAL_META: task_id=64, framework=cirq, class=1
import cirq

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    qubits_reg1 = cirq.LineQubit.range(n)
    qubits_reg2 = cirq.LineQubit.range(n, 2 * n)
    
    circuit = cirq.Circuit()
    circuit.append([cirq.H(q) for q in qubits_reg1])
    circuit.append(cirq.Moment())
    for j in range(n):
        circuit.append(cirq.CNOT(qubits_reg1[j], qubits_reg2[j]))
    
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit.append(cirq.CNOT(qubits_reg1[i], qubits_reg2[j]))
        circuit.append(cirq.Moment())
        circuit.append([cirq.H(q) for q in qubits_reg1])
    
    circuit.append(cirq.measure(*qubits_reg1, key='c'))
    return circuit
