pylint ./src/main.py
************* Module main
~~src\main.py:1:0: C0114: Missing module docstring (missing-module-docstring)~~
~~src\main.py:15:0: C0304: Final newline missing (missing-final-newline)~~

For Error 1:

"""

main.py

Provides the Streamlit GUI entry point for the data-visualization application.

Defines `run_app()` in visualize_data.py as the main application loop.

"""

For Error 2:
src\main.py:15:0: C0304: Final newline missing (missing-final-newline)

added: Backspace


PS C:\Users\Micae\OneDrive\Dokumente\GitHub\Fitbit_analysis17> pylint .\src\summary_statistics.py
************* Module summary_statistics
src\summary_statistics.py:22:0: C0301: Line too long (103/100) (line-too-long)
src\summary_statistics.py:37:0: C0301: Line too long (115/100) (line-too-long)
src\summary_statistics.py:41:45: C0303: Trailing whitespace (trailing-whitespace)
src\summary_statistics.py:42:0: C0304: Final newline missing (missing-final-newline)
src\summary_statistics.py:1:0: C0114: Missing module docstring (missing-module-docstring)
src\summary_statistics.py:6:0: C0115: Missing class docstring (missing-class-docstring)
src\summary_statistics.py:8:8: C0103: Attribute name "df" doesn't conform to snake_case naming style (invalid-name)
src\summary_statistics.py:7:23: C0103: Argument name "df" doesn't conform to snake_case naming style (invalid-name)
src\summary_statistics.py:10:4: C0116: Missing function or method docstring (missing-function-docstring)
src\summary_statistics.py:11:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
src\summary_statistics.py:20:4: C0116: Missing function or method docstring (missing-function-docstring)
~~src\summary_statistics.py:26:4: C0116: Missing function or method docstring (missing-function-docstring)~~
~~src\summary_statistics.py:31:4: C0116: Missing function or method docstring (missing-function-docstring)~~
~~src\summary_statistics.py:36:4: C0116: Missing function or method docstring (missing-function-docstring)~~
src\summary_statistics.py:37:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)


added docstring:


Error1:

 """

    Calculate the average daily steps when both 'TotalSteps' and 'ActivityDate' are present.

    Returns:

    float or None: Mean of 'TotalSteps' or None if requirements not met.

    """


Error2:

"""

    Compute the average sleep duration in minutes from 'TotalMinutesAsleep'.

    Returns:

    float or None: Mean minutes asleep or None if column not present.

    """

Error3:

"""

    Compute the total sleep duration in minutes from 'TotalMinutesAsleep'.

    Returns:

    int or float or None: Sum of minutes asleep or None if column not present.

    """
