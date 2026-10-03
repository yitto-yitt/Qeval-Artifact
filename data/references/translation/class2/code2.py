from math import sqrt

from qiskit.quantum_info import Statevector


def create_bell_statevector():
    return (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)
