##To solve this problem, we divide it into 2 parts:
    ###1. Object-detective
        - The purpose of this part is to identify the position of the characters in the image of the answer sheet, crop the part of the image containing the character and move to the next part to classify the character.
        - Technologies used: OpenCV
    ###2. Character-recognize
        - Using handwritten characters dataset (download form Kaggle) to train model.
        - Using KNN algorthrm to classify the characters cropped from the answer sheets.
        
