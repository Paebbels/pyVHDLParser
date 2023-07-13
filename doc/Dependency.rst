.. _dependency:

Dependencies
############

.. |img-pyTooling-lib-status| image:: https://img.shields.io/librariesio/release/pypi/pyTooling
   :alt: Libraries.io status for latest release
   :height: 22
   :target: https://libraries.io/github/pyTooling/pyTooling
.. |img-pyTooling-val-status| image:: https://img.shields.io/snyk/vulnerabilities/github/pyTooling/pyTooling
   :alt: Snyk Vulnerabilities for GitHub Repo
   :height: 22
   :target: https://img.shields.io/snyk/vulnerabilities/github/pyTooling/pyTooling

+------------------------------------------+------------------------------------------+
| `Libraries.io <https://libraries.io/>`_  | Vulnerabilities Summary                  |
+==========================================+==========================================+
| |img-pyTooling-lib-status|               | |img-pyTooling-val-status|               |
+------------------------------------------+------------------------------------------+

.. _dependency-package:

pyTooling Package (Mandatory)
*****************************

.. rubric:: Manually Installing Package Requirements

Use the :file:`requirements.txt` file to install all dependencies via ``pip3`` or install the package directly from
PyPI (see :ref:`installation`).

.. code-block:: shell

   pip3 install -U -r requirements.txt


.. rubric:: Dependency List

When installed as ``pyTooling``:

+-----------------------------------------------------------------+-------------+-------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Package**                                                     | **Version** | **License**                                                                               | **Dependencies**                                                                                                                                       |
+=================================================================+=============+===========================================================================================+========================================================================================================================================================+
| *No dependencies*                                               | — — — —     | — — — —                                                                                   | — — — —                                                                                                                                                |
+-----------------------------------------------------------------+-------------+-------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+


When installed as ``pyTooling[yaml]``:

+-----------------------------------------------------------------+-------------+-------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Package**                                                     | **Version** | **License**                                                                               | **Dependencies**                                                                                                                                       |
+=================================================================+=============+===========================================================================================+========================================================================================================================================================+
| `ruamel.yaml <https://sourceforge.net/projects/ruamel-yaml/>`__ | ≥0.17       | `MIT <https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree/LICENSE>`__              | *Not yet evaluated.*                                                                                                                                   |
+-----------------------------------------------------------------+-------------+-------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+



.. _dependency-testing:

Unit Testing / Coverage / Type Checking (Optional)
**************************************************

Additional Python packages needed for testing, code coverage collection and static type checking. These packages are
only needed for developers or on a CI server, thus sub-dependencies are not evaluated further.


.. rubric:: Manually Installing Test Requirements

Use the :file:`tests/requirements.txt` file to install all dependencies via ``pip3``. The file will recursively install
the mandatory dependencies too.

.. code-block:: shell

   pip3 install -U -r tests/requirements.txt


.. rubric:: Dependency List

+--------------------------------------------------------------------+-------------+----------------------------------------------------------------------------------------+----------------------+
| **Package**                                                        | **Version** | **License**                                                                            | **Dependencies**     |
+====================================================================+=============+========================================================================================+======================+
| `pytest <https://GitHub.com/pytest-dev/pytest>`__                  | ≥7.3.0      | `MIT <https://GitHub.com/pytest-dev/pytest/blob/master/LICENSE>`__                     | *Not yet evaluated.* |
+--------------------------------------------------------------------+-------------+----------------------------------------------------------------------------------------+----------------------+
| `pytest-cov <https://GitHub.com/pytest-dev/pytest-cov>`__          | ≥4.1.0      | `MIT <https://GitHub.com/pytest-dev/pytest-cov/blob/master/LICENSE>`__                 | *Not yet evaluated.* |
+--------------------------------------------------------------------+-------------+----------------------------------------------------------------------------------------+----------------------+
| `pytest-benchmark <https://GitHub.com/ionelmc/pytest-benchmark>`__ | ≥4.0.0      | `BSD 2-Clause <https://GitHub.com/ionelmc/pytest-benchmark/blob/master/LICENSE>`__     | *Not yet evaluated.* |
+--------------------------------------------------------------------+-------------+----------------------------------------------------------------------------------------+----------------------+
| `Coverage <https://GitHub.com/nedbat/coveragepy>`__                | ≥7.2        | `Apache License, 2.0 <https://GitHub.com/nedbat/coveragepy/blob/master/LICENSE.txt>`__ | *Not yet evaluated.* |
+--------------------------------------------------------------------+-------------+----------------------------------------------------------------------------------------+----------------------+
| `mypy <https://GitHub.com/python/mypy>`__                          | ≥1.2.0      | `MIT <https://GitHub.com/python/mypy/blob/master/LICENSE>`__                           | *Not yet evaluated.* |
+--------------------------------------------------------------------+-------------+----------------------------------------------------------------------------------------+----------------------+
| `lxml <https://GitHub.com/lxml/lxml>`__                            | ≥4.9        | `BSD 3-Clause <https://GitHub.com/lxml/lxml/blob/master/LICENSE.txt>`__                | *Not yet evaluated.* |
+--------------------------------------------------------------------+-------------+----------------------------------------------------------------------------------------+----------------------+


.. _dependency-documentation:

Sphinx Documentation (Optional)
*******************************

Additional Python packages needed for documentation generation. These packages are only needed for developers or on a
CI server, thus sub-dependencies are not evaluated further.


.. rubric:: Manually Installing Documentation Requirements

Use the :file:`doc/requirements.txt` file to install all dependencies via ``pip3``. The file will recursively install
the mandatory dependencies too.

.. code-block:: shell

   pip3 install -U -r doc/requirements.txt


.. rubric:: Dependency List

+-------------------------------------------------------------------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Package**                                                                                     | **Version**  | **License**                                                                                              | **Dependencies**                                                                                                                                     |
+=================================================================================================+==============+==========================================================================================================+======================================================================================================================================================+
| `pyTooling <https://GitHub.com/pyTooling/pyTooling>`__                                          | ≥5.0.0       | `Apache License, 2.0 <https://GitHub.com/pyTooling/pyTooling/blob/main/LICENSE.md>`__                    | *None*                                                                                                                                               |
+-------------------------------------------------------------------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| `Sphinx <https://GitHub.com/sphinx-doc/sphinx>`__                                               | ≥5.3.0       | `BSD 3-Clause <https://GitHub.com/sphinx-doc/sphinx/blob/master/LICENSE>`__                              | *Not yet evaluated.*                                                                                                                                 |
+-------------------------------------------------------------------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| `sphinxcontrib-mermaid <https://GitHub.com/mgaitan/sphinxcontrib-mermaid>`__                    | ≥0.9.2       | `BSD <https://GitHub.com/mgaitan/sphinxcontrib-mermaid/blob/master/LICENSE.rst>`__                       | *Not yet evaluated.*                                                                                                                                 |
+-------------------------------------------------------------------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| `autoapi <https://GitHub.com/carlos-jenkins/autoapi>`__                                         | ≥2.0.1       | `Apache License, 2.0 <https://GitHub.com/carlos-jenkins/autoapi/blob/master/LICENSE>`__                  | *Not yet evaluated.*                                                                                                                                 |
+-------------------------------------------------------------------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| `sphinx_btd_theme <https://GitHub.com/buildthedocs/sphinx.theme>`__                             | ≥0.5.2       | `MIT <https://GitHub.com/buildthedocs/sphinx.theme/blob/master/LICENSE>`__                               | *Not yet evaluated.*                                                                                                                                 |
+-------------------------------------------------------------------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| !! `sphinx_fontawesome <https://GitHub.com/fraoustin/sphinx_fontawesome>`__                     | ≥0.0.6       | `GPL 2.0 <https://GitHub.com/fraoustin/sphinx_fontawesome/blob/master/LICENSE>`__                        | *Not yet evaluated.*                                                                                                                                 |
+-------------------------------------------------------------------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| `sphinx_autodoc_typehints <https://GitHub.com/agronholm/sphinx-autodoc-typehints>`__            | ≥1.19.5      | `MIT <https://GitHub.com/agronholm/sphinx-autodoc-typehints/blob/master/LICENSE>`__                      | *Not yet evaluated.*                                                                                                                                 |
+-------------------------------------------------------------------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| `ruamel.yaml <https://sourceforge.net/projects/ruamel-yaml/>`__                                 | ≥0.17        | `MIT <https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree/LICENSE>`__                             | *Not yet evaluated.*                                                                                                                                 |
+-------------------------------------------------------------------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+

.. _dependency-packaging:

Packaging (Optional)
********************

Additional Python packages needed for installation package generation. These packages are only needed for developers or
on a CI server, thus sub-dependencies are not evaluated further.


.. rubric:: Manually Installing Packaging Requirements

Use the :file:`build/requirements.txt` file to install all dependencies via ``pip3``. The file will recursively
install the mandatory dependencies too.

.. code-block:: shell

   pip3 install -U -r build/requirements.txt


.. rubric:: Dependency List

+----------------------------------------------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Package**                                                                | **Version**  | **License**                                                                                              | **Dependencies**                                                                                                                                     |
+============================================================================+==============+==========================================================================================================+======================================================================================================================================================+
| `pyTooling <https://GitHub.com/pyTooling/pyTooling>`__                     | ≥2.11.0      | `Apache License, 2.0 <https://GitHub.com/pyTooling/pyTooling/blob/main/LICENSE.md>`__                    | *None*                                                                                                                                               |
+----------------------------------------------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| `wheel <https://GitHub.com/pypa/wheel>`__                                  | ≥0.40.0      | `MIT <https://github.com/pypa/wheel/blob/main/LICENSE.txt>`__                                            | *Not yet evaluated.*                                                                                                                                 |
+----------------------------------------------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+


.. _dependency-publishing:

Publishing (CI-Server only)
***************************

Additional Python packages needed for publishing the generated installation package to e.g, PyPI or any equivalent
services. These packages are only needed for maintainers or on a CI server, thus sub-dependencies are not evaluated
further.


.. rubric:: Manually Installing Publishing Requirements

Use the :file:`dist/requirements.txt` file to install all dependencies via ``pip3``. The file will recursively
install the mandatory dependencies too.

.. code-block:: shell

   pip3 install -U -r dist/requirements.txt


.. rubric:: Dependency List

+----------------------------------------------------------+--------------+-------------------------------------------------------------------------------------------+----------------------+
| **Package**                                              | **Version**  | **License**                                                                               | **Dependencies**     |
+==========================================================+==============+===========================================================================================+======================+
| `wheel <https://GitHub.com/pypa/wheel>`__                | ≥0.40.0      | `MIT <https://github.com/pypa/wheel/blob/main/LICENSE.txt>`__                             | *Not yet evaluated.* |
+----------------------------------------------------------+--------------+-------------------------------------------------------------------------------------------+----------------------+
| `Twine <https://GitHub.com/pypa/twine/>`__               | ≥4.0.2       | `Apache License, 2.0 <https://github.com/pypa/twine/blob/main/LICENSE>`__                 | *Not yet evaluated.* |
+----------------------------------------------------------+--------------+-------------------------------------------------------------------------------------------+----------------------+
