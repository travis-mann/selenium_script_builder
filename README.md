# Selenium Script Builder
Interactive GUI tool to create simple Python Selenium scripts. Well suited for automating simple repetitive web tasks such as downloading the same document from a site daily or entering text in a certain field.


# Setup
1. Ensure [Git](https://git-scm.com/) version control and [Python 3.8+](https://www.python.org/downloads/) are installed
2. Run the following terminal commands in the project folder
```
git init
git clone https://github.com/travis-mann/selenium_script_builder
python -m venv ./venv
./venv/Scripts/activate
pip install -r ./selenium_script_builder/requirements.txt

```

# Usage
1. Run app.py to open the application
2. Use the build screen to select Selenium/ Python commands and add them to the command list window with appropriate arguments
3. Drag and drop commands to re-order a script
4. Select a command and click "Remove" to delete a command
5. Click "Clear" to delete all commands from the current script
6. Click "Compile" to create a script from the selected command and transition to the run window
7. In the run window select "Run" to run the script and see the output in the provided window
8. During a script run click "Cancel" to prematurely end the run
9. While a script is not running click "Build" to transition back into the build screen
