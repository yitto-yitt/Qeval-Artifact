# EVAL_META: task_id=7, framework=cirq, class=3
import cirq
from cirq import Rx

def create_parametrized_gate():
    theta = sympy.Symbol("theta")
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    circuit.append(Rx(rads=theta).on(qubit))
    return circuit
