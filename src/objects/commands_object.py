"Take the settings from GUI and pass it into the pipeline"


class CommandsObject:
    """Class with the commands for the pipeline
    options/features for the user to change are stored in an object of this class
    """

    def __init__(self):
        """
        {'has_started': booleans, 'path': path string, 'valid': booleans}
        {'features_extractor': int 0 , 1, 2, 'frame_to_add': string list 'canny', 'blur'}
        {'classifier_model': int 0 or 1, 'max_class': int 1-5}
        {'apply_ocr': boolean, 'show_src_language': boolean, 'show_trans': boolean}
        {'continues_mode': boolean}
        {'index_of_frame_dict': int 0-4, 'bounding_box': boolean,
        'nr_of_patches': int 1-5,'show_strings': boolean}
        """
        self.command_info = {'has_started': False, 'path': None, 'valid': True}
        self.preprocessor = {'features_extractor': 0,
                             'frame_to_add': []}
        self.classifier = {'classifier_model': 1,
                           'max_class': 5}
        self.ocr_and_trans = {'apply_ocr': 0, 'show_src_string': 0,
                              'show_trans': 0}
        self.logic = {'continues_mode': 0}
        self.visualizer = {'index_of_frame_dict': 1, 'bounding_box': 1, 'nr_of_patches': 5,
                           'show_strings': 1}

    def reset_commands(self):
        "reset everything"
        self.preprocessor = {'features_extractor': 0, 'frame_to_add': ['blur', 'canny']}
        self.classifier = {'classifier_model': 1, 'max_class': 5}
        self.ocr_and_trans = {'apply_ocr': 0, 'show_src_string': 0, 'show_trans': 0}
        self.logic = {'mode': 0}
        self.visualizer = {'index_of_frame_dict': 0, 'bounding_box': 0, 'nr_of_patches': 5,
                           'show_strings': 1}

    def max_visualization(self):
        """
        show all visualizations
        Returns:

        """
        self.preprocessor = {'features_extractor': 0, 'frame_to_add': ['blur', 'canny']}
        self.classifier = {'classifier_model': 1, 'max_class': 5}
        self.ocr_and_trans = {'apply_ocr': 1, 'show_src_string': 1, 'show_trans': 1}
        self.logic = {'mode': 0}
        self.visualizer = {'index_of_frame_dict': 0, 'bounding_box': 1, 'nr_of_patches': 5,
                           'show_strings': 1}

    def is_command_valid(self):
        """
        check if the command is the right format
        Returns:

        """
        self.command_info['valid'] = True
