# EVAL_META: task_id=36, framework=pennylane, class=3
import pennylane as qml

def bv_function(s):
    n = len(s)

    def oracle(wires):
        """Apply the Bernstein-Vazirani oracle defined by bitstring s.
        
        Args:
            wires: list of n+1 wires; wires[0]..wires[n-1] are input qubits,
                   wires[n] is the output qubit.
        """
        for i in range(n):
            if s[-(i + 1)] == "1":
                qml.CNOT(wires=[wires[i], wires[n]])

    return oracle
