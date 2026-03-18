# THE “UNBREAKABLE” MACHINE

This solo project was carried out as part of the **TIPE (Travaux d’Initiative Personnelle Encadrés -- Engineering School Entrance Research Project)** during the **MP preparatory class year 2024-2025**, whose theme was:  

> **Transition – Transformation – Conversion**

Having chosen the computer science option, this work focuses on the **algorithmic modelling and simulation** of a historical cryptographic system.

The initial objective was to **reproduce the functioning of the Enigma machine as faithfully as possible**, within the limits of the knowledge and technical skills available at this stage of study.
In a second phase, the project evolved towards an **experimental study of decryption**, using the previously implemented machine.

---

## 🎯 Scientific objectives

The purpose of this TIPE is to:

* demonstrate the ability to conduct a **complete scientific approach** (modelling, simulation, analysis),
* connect theoretical notions (permutations, algorithms, complexity) to a **real encryption system**,
* experimentally investigate **brute-force cryptanalysis**,
* analyse the influence of several parameters on the **decryption time**.

---

## ⚙️ Enigma machine modelling

The program implements a software simulation of the Enigma machine, including:

* **rotors I to V**,
* **reflectors A and B**,
* a configurable **plugboard**,
* the **rotor stepping mechanism**,
* the historical **double-stepping phenomenon**,
* configurable **rotor order**,
* configurable **initial rotor positions**.

The model first targets a **standard Enigma configuration**, and was later extended towards richer settings inspired by variants used, in particular, by the **Kriegsmarine**.

---

## 🔐 Encryption process

The main function performs both encryption and decryption, as the Enigma process is symmetric.

General principle:

1. optional permutation through the plugboard
2. forward signal propagation through the rotors
3. reflection
4. backward propagation through the rotors
5. second permutation through the plugboard
6. rotor rotation at each character

Inputs include:

* an uppercase message
* rotor order
* initial rotor positions
* reflector choice
* plugboard connections

---

## 🔎 Cryptanalysis

A second part of the project focuses on **brute-force decryption**.

The implemented strategy consists in:

* systematically testing:

  * all rotor permutations
  * all possible initial positions
* searching for **probable words** in the decrypted message (e.g. *METEO*, *CHANCELIER*),
* measuring the **time required to recover the correct configuration**.

This approach illustrates:

* the **combinatorial complexity** of the Enigma system
* the historical importance of cryptanalysis methods
* the impact of parameters such as message length or rotor settings on computational cost

---

## 📊 Experimental study

The program can generate data suitable for:

* plotting **decryption time graphs**,
* comparing different machine configurations,
* observing the growth of algorithmic complexity.
