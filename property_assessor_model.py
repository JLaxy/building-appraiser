# Model of the Property Assessor
# Contains all logical code
import json

class PropertyAssessorModel():    
    # Constructor
    def __init__(self) -> None:
        print("initialized!")
        # Keeps track of the selected materials; False by default, True if selected
        self.selected_materials : dict = self.get_materials()
        self.classifications : dict = self.get_classifications()
        self.classification_scores = self.get_classification_scores()

    # Retrieves materials from json file
    def get_materials(self):
        with open("materials.json") as json_file:
            return json.load(json_file)
        
    # Retrieves classifications
    def get_classifications(self):
        with open("classifications.json") as json_file:
            return json.load(json_file)
    
    # Initialize classification scores
    def get_classification_scores(self):
        return {
            "high" : 0,
            "mid to high" : 0,
            "mid" : 0,
            "low to mid" : 0,
            "low" : 0,
        }

    # Evaluates value of property
    def evaluate(self, floor_area):
        print("evaluating...")

        # Converting to float
        floor_area = float(floor_area)

        # Calculating scores
        # Iterating through each building component
        for components in self.selected_materials:
            # Iterating through each material(s) of building component
            for materials in self.selected_materials[components]:
                # If material is not selected, then skip
                if self.selected_materials[components][materials][0] == False:
                    continue
                
                # Iterating through scores of each material
                index = 0

                for score in self.selected_materials[components][materials][1]:
                    # Add score
                    self.classification_scores[self.classifications[str(index)]] += score
                    index += 1

        # Finding highest score
        highest_score = 0
        for classs in self.classification_scores:
            if self.classification_scores[classs] > highest_score:
                highest_score = self.classification_scores[classs]

        # Finding percentage and highest percentage score
        highest_score_percent = 0
        for classs in self.classification_scores:
            # Calculate percentage score
            score = round((self.classification_scores[classs] / highest_score) * 100, 2)
            # If higher than current percentage score
            if score > highest_score_percent:
                # Assign new score and class
                highest_score_percent = score
            self.classification_scores[classs] = round((self.classification_scores[classs] / highest_score) * 100, 2)

        # Finding what class building belongs
        classification_matched = []
        for classs in self.classification_scores:
            # If equal to highest score, add to matched class
            if self.classification_scores[classs] == highest_score_percent:
                classification_matched.append(classs)

        # # Finding price per sqm
        # average_price = 0
        # # If building is classified more than 1
        # if len(classification_matched) > 1:
        #     # Iterating through each classification
        #     for classs in self.classification_scores:
        #         # If classification is in matched classificiation
        #         if classs in classification_matched:
        #             # Add price
        #             average_price += self.classifications[classs]
        #     # Get average price
        #     average_price /= len(classification_matched)
        # else:
        #     # Get price of single classification matched
        #     average_price = self.classifications[classification_matched[0]]

        average_price = 0

        for classification in self.classification_scores:
            average_price += self.classifications[classification] * (self.classification_scores[classification] / 100)

        average_price /= 5

        print(self.classification_scores)
        print(f"class(es): {classification_matched}")
        print(f"price per sqm: {average_price}")
        print(f"estimated price: {average_price * floor_area}")

        return classification_matched, round(average_price, 2), round(average_price * floor_area, 2)


    
    # Returns true if user has selected at least one material in all building components
    def is_selection_valid(self): 
        # Iterating through each building component
        for components in self.selected_materials:
            hasSelection = False
            # Iterating through each material(s) of building component
            for materials in self.selected_materials[components]:
                # If atleast 1 component is selected
                if self.selected_materials[components][materials][0] == True:
                    # Set to true
                    hasSelection = True
                
            # If component has no selection, return false
            if not hasSelection:
                return False
        # Else, return true
        return True
    
    # Returns true if value on floor area is valid
    def is_floor_area_valid(self, value : str):
        # Try to convert to float
        try:
            floor_area = float(value)
            return True
        # Return false if there is error
        except:
            return False

    # Resets all selected materials
    def reset(self):
        print("resetting...")
        # Reloading selected materials from JSON file
        self.selected_materials : dict = self.get_materials()
        self.classification_scores = self.get_classification_scores()