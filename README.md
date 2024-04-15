# About
This is a tool that I developed for a physician with Python & QT.
For his clinical studies, he had to collect and evaluate individual values from his patients' laboratory findings. 
This tool saves him this manual work. It can read in a collection of laboratory results, 
lists all the laboratory parameters found there and then gives the user the option of extracting 
individual laboratory values from all the results and exporting them to a single Excel file. 
The tool can import files in CSV or Excel format. As it was only developed to read in a fixed report format, 
the project is primarily for demonstration purposes and requires individual customization to work with 
other report structures. Below you can see a video demonstrating how it works. 
Under the branch windows-build you will also find an executable that can be 
run under Windows with test data so that you can try out the functionality yourself. 

## Demo
https://github.com/Bratsera/Laboratory-Analysis-Tool/assets/83575368/771fabaa-c532-4cb8-89cf-eff0503da530

## Running the project
For the application to work via IDE/Termial you need to have Python installed.
Run the command  `pip install -r requirements.txt` in the projects root directory to install the dependencies listed in the requirements.txt
To run the app via IDE/Terminal, you need to run the main.py script

If the error "no platform plugin could be located" occurs while running main.py, you probaply need to set the environment variable  QT_PLUGIN_PATH:
`set QT_PLUGIN_PATH=C:\path\to\your\pyqt5\installation\platforms`

## How the App works
1. With the app opened click on the button "Quellordner auswählen" and choose the folder, where the csv/xlsx files are located, which you want to import. (There is a "TestData" folder for demonstration in the program folder)
2. If everything worked correct, the Path you choose should be displayed in the UI.
Click on the dropdown and choose the parameter you want to extract and click on the button "Anzeigen".
The list of extracted date should be displayed in the UI.
3. Click on the button "Tabelle exportieren" and choose a directory and filename, where the extracted data should be exported. An Excel file should be generated

## Modifying the UI
If you like to make modification in the UI, you can open the ./ui/mainwindow.ui file with the Program Qt Creator. (You need to have QT installed for this)  
You finally need to run the build.py script to update the UI changes in the code

## Making a standalone build
To build an executable e.g for Windows (also tested with MacOS), run the following command: `python exe.py build`
For further build customization see the cx_freeze docs: https://cx-freeze.readthedocs.io/en/latest/builtdist.html
