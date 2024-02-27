## GestAccount

This project provides an environment for visualizing PlantUML diagrams created in GestAccount.

### Prerequisites

* Docker installed: [https://www.docker.com/](https://www.docker.com/)
* Visual Studio Code (VSCode): [https://code.visualstudio.com/](https://code.visualstudio.com/)
* **PlantUML extension for VSCode:** [https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml)

### How to Use
1. **Execute the following script to start PlantUML Server:**

	```
	docker-compose up -d
	```
2. **Open VSCode and install the PlantUML extension:**

* Open the "Extensions" menu.
* Search for "PlantUML".
* Click the "Install" button to install the extension.

3. **Configure the PlantUML extension:**

* Open the "File" > "Preferences" > "Settings" menu.
* In the search bar, type "plantuml".
* In the "PlantUML: Server" section, set the server URL to "http://localhost:8080".
* In the "PlantUML: Render" section, set the render mode to "PlantUMLServer".

4. **Open a PlantUML (*.puml) file in VSCode.**


5. **Click the "Preview" button in the VSCode status bar to visualize the diagram or use `Alt + D`  keys.**

