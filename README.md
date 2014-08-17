Statelet
=============================

Provides a mechanism for an object to inherit the
state of another object, such that changes to the
parent object's state will be reflected in the
child object's state, unless overwritten.

Question: "You have just pointlessly reimplemented inheritance, haven't you?"

Answer: No. Inheritance typically refers to a mechanism for sharing functionality (not to be confused with state) among types. This package uses composition to share state (not to be confused with functionality) in a way that admits attribute access to repeatedly failover to other object instances that are linked together in a chain for this excplicit purpose. Think of it as state inheritance if you need to, but the similarity between the two ends there.