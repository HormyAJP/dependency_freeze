Simple tool for recursively hashing all contents of folders and then checking the hashes.


# Use case

The primary use case for this tool is to pin dependencies of applications to avoid supply chain
attacks when building the application in CI.

There are many dependency management tools on the market, e.g. Cocoapods, Nuget,
Gradle, Ruby Gems, npm. When a developer specifies a dependency they will commit a config file to their
SCM tool which specifies what dependencies and versions of those dependencies they wish to use.
Generally the tools implement some for of "lock file" which means that those versions can't change
from under your feet.

One problem is that most of these tools don't enforce the actual **content** of the dependencies to be
the same. This leaves developers vulnerable to a supply chain attack which changes the delivered
contents for those dependencies changes unepxected; perhaps maliciously.

Some examples:

* If the owner of Git repo for a dependency had their account compromised then an attacker could
  force push code to their repo and change the content for a specific version of a dependency.
  Cocoapods is vulnerable to this attack.
* The 3rd party web server which servers dependencies, or at least dependency indexes, could be
  compromised.

Some tools adequately prevent supply chain attakcs, but not all. This tool is designed to fill the
gaps simply and consistently to give developers confidence that they are not shipping malware to
their customers

# Implementation Notes

This is *very* basic so far. I'll evolve it as needs arise by experimenting with various dependency
management systems.
