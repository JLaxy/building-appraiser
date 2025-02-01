from functools import partial
import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QDialog, QCheckBox, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt6 import uic
from property_assessor_model import PropertyAssessorModel

class PropertyAssessor(QWidget):
    def __init__(self, model : PropertyAssessorModel):
        super().__init__()
        # Setting model
        self.model = model

        self.setWindowTitle("Property Assessor")
        # Loading UI
        uic.loadUi("main_window.ui", self)

        # List of buttons in UI
        self.material_buttons = ["structural_frame_button", "foundations_button", "roofing_button", "truss_button", "interior_ceiling_button", "exterior_ceiling_button", "interior_wall_button", "exterior_wall_button", "partitions_button", "windows_button", "doors_button", "floor_finish_button"]

        # Iterating through each button
        for button in self.material_buttons:
            # Assigns function to be called for each material button
            getattr(self, button).clicked.connect(partial(self.pressed, f"{button}"))

    # Evaluate Button On Press
    def evaluate(self):
        # If value in floor area is valid
        if not self.model.is_floor_area_valid(self.floor_area_field.toPlainText()):
            self.show_dialog("Error!", "Invalid floor area!")
            return

        # If did not select atleast 1 for all components
        if not self.model.is_selection_valid():
            self.show_dialog("Error!", "You must select a material for each component!")
            return
        
        # Evaluate
        classification, price_per_sqm, estimated_price = self.model.evaluate(self.floor_area_field.toPlainText())

        self.show_dialog("Result", f"Classfication: {classification}\n\nPrice per SQM: P{price_per_sqm:,}\n\nEstimated Price: P{estimated_price:,}")
            
    # Reset Button On Press
    def reset(self):
        # Resetting model
        self.model.reset()
        # Iterating through each label using material buttons
        for label in self.material_buttons:
            # Resetting label
            getattr(self, label.replace("_button", "_label")).setText("Nothing selected.")

    # Material Button On Press
    def pressed(self, button_pressed : str):
        # Initializing
        dialog_window = QDialog()
        # Loading .ui file
        uic.loadUi(f"pop_up_dialogs/{button_pressed.replace("_button", ".ui")}", dialog_window)
        dialog_window.setWindowTitle(button_pressed.replace("_button", "").replace("_", " ").title())

        # If user didnt click done
        if dialog_window.exec() != 1:
            # Exit
            return
        
        # Get all QCheckBox children of QDialog
        children = dialog_window.findChildren(QCheckBox)

        label_string = ""
        # Tries to catch if user clicked on done but has not selected any check box
        hasCheck = False

        # Iterate through each children
        for child in children:
            # If checked
            if self.is_check_box_pressed(dialog_window, child.objectName()):
                hasCheck = True
                # Add to label string
                label_string += f"{child.objectName().replace("_", " ").title()}, "
                # Setting selected material to True in model
                self.model.selected_materials[button_pressed.replace("_button", "")][child.objectName()][0] = True
            else:
                self.model.selected_materials[button_pressed.replace("_button", "")][child.objectName()][0] = False

        # If user checked a check box
        if hasCheck:
            # Update label
            getattr(self, button_pressed.replace("_button", "_label")).setText(label_string)
        else:
            getattr(self, button_pressed.replace("_button", "_label")).setText("Nothing selected.")

    # Returns true if specified checkbox is checked
    def is_check_box_pressed(self, dialog_window : QDialog, widget_name : str):
        return dialog_window.findChild(QCheckBox, name = widget_name).isChecked()
    
    # Shows error dialog
    def show_dialog(self, title : str, message : str):
        error_dialog = QDialog()
        error_dialog.setWindowTitle(title)

        ok_button = QDialogButtonBox.StandardButton.Ok
        button_box = QDialogButtonBox(ok_button)
        button_box.accepted.connect(error_dialog.accept)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(message))
        layout.addWidget(button_box)

        error_dialog.setLayout(layout)
        error_dialog.exec()

os.system("cls")
app = QApplication(sys.argv)
mainWindow = PropertyAssessor(PropertyAssessorModel())
mainWindow.show()
sys.exit(app.exec())