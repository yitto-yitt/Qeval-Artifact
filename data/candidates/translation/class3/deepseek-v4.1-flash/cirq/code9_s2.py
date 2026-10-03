# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    params = [sympy.Symbol(f'theta_{i}') for i in range(12)]
    
    moments = [
        cirq.Moment(cirq.ry(params[0])(qubits[0]),
                    cirq.ry(params[2])(qubits[1]),
                    cirq.ry(params[4])(qubits[2])),
        cirq.Moment(cirq.rz(params[1])(qubits[0]),
                    cirq.rz(params[3])(qubits[1]),
                    cirq.rz(params[5])(qubits[2])),
        cirq.Moment(cirq.CX(qubits[0], qubits[1])),
        cirq.Moment(cirq.CX(qubits[0], qubits[2])),
        cirq.Moment(cirq.CX(qubits[1], qubits[2])),
        cirq.Moment(cirq.ry(params[6])(qubits[0]),
                    cirq.ry(params[8])(qubits[1]),
                    cirq.ry(params[10])(qubits[2])),
        cirq.Moment(cirq.rz(params[7])(qubits[0]),
                    cirq.rz(params[9])(qubits[1]),
                    cirq.rz(params[11])(qubits[2])),
    ]
    return cirq.Circuit(moments)
