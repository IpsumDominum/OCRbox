# OCRbox

OCR box is a GUI/command line tool written with python to select parts of your screen to monitor and apply OCR/Image comparison to.
OCR is powered by Tesseract OCR.

## Features and how it works:
    Projects are managed as "Boxes".
    1.You start by creating a box, this is the main region,you can give it a name.
    2.Then you may add regions or comp-regions to the area enclosed by the main box.
    3.The regions are saved to a file, which can be loaded to append more regions.
    4.Or, loaded with a script to extract all the OCR/comparison results, without
    5.triggering the GUI/No_GUI application which manage these boxes.
    6.The regions are stored in a file with the format:
    name_of_main_box x1 y1 x2 y2
    name_of_region1 x1 y1 x2 y2
    .
## Work in progress/TODO: 
    1.GUI is still in progress:
        Show region selection on tk monitor
    2.Add load functions and OCR
    3.Create comparison boxes is still in progress for both GUI/NO_GUI
    
