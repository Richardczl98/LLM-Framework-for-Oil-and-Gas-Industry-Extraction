## Python Development Environment Setup Instructions

**Requirements:**

* Python >= 3.10

**Instructions:**

1. **Create a Virtual Environment:**
   
   It's highly recommended to use a virtual environment to isolate project dependencies. Refer to [wwwinsights](https://www.wwwinsights.com/lang/python/how-to-use-python-virtual-environment/) for creating virtual environments.

2. **Install `pip-tools`:**
   
   Activate your virtual environment and install `pip-tools` using the following command:

   ```bash
   pip install pip-tools
   ```

3. **Install Dependencies:**
   
   This step uses a pre-compiled and verified `requirements.txt.compiled` file for faster and more reliable installation:

   ```bash
   pip-sync -v requirements.txt.compiled --pip-args "--retries 3 --timeout 3600"
   ```

   - `-v`: Enables verbose output.
   - `--pip-args`: Passes arguments to pip for installation. If your pip installation is slow due to firewalls or blockage, use those parameters might help you.
     - `--retries 3`: Attempts installation up to 3 times on failure.
     - `--timeout 3600`: Sets a timeout of 1 hour for each installation attempt.

4. **Compile Your Own Requirements (Developers ONLY):**
   
   If you added any new python libraries to the souce code, add it in `requirements.in`. Please pin the version if you feel a major update will break your exsiting code.

   ```bash
   pip-compile -v -o requirements.txt.compiled requirements.in --pip-args "--retries 3 --timeout 3600"
   ```

   - `-v`: Enables verbose output.
   - `-o requirements.txt.compiled`: Specifies the output file name.

5. **Check in (Developers ONLY)**

Please check in both `requirements.in` and `requirements.txt.compiled`. 

`requirements.txt.freeze.obsolete` is there for comparision purpose, and do not update or use it anymore.
