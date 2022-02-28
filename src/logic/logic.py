"""class Logic"""
from pathlib import Path
import imageio


class Logic:
    """ classifier network --> LOGIC --> gui
    -interpret classifications
    -filter bad classifications
    -extract information for gui
    """

    def __init__(self, interface_object=None):
        """

        Args:
            interface_object:
        """
        self.interface_object = interface_object
        self.whole_icon_list = self.get_icon_list()
        self.signnames = ["20kmh", "30kmh", "50kmh", "60kmh",
                          "70kmh", "80kmh", "!=80kmh", "100kmh", "120kmh",
                          "pkw ueberholverb.", "lkw ueberholverb.", "vorfahrt",
                          "vorfahrtsstr", "vorfahrt gew.", "stop", "druchfa. verb.",
                          "lkw verb.", "einbahnstr", "achtung", "achtung links",
                          "achtung rechts", "achtung slalom", "achtung huckel",
                          "achtung rutschen", "fahrbahnvereng.", "baustelle",
                          "ampel", "zebra", "kinder", "fahrrad", "eis", "wild",
                          "no speed limit", "rechts kruve", "links kurve",
                          "gerade aus", "gerade/rechts", "gerade/links",
                          "recht bleiben", "links bleiben", "kreisverkehr",
                          "pkw überhl. verb. aufg.", "lkw überhl. verb. aufg."]
        self.history = None

    def apply_logic(self):
        """
        applies logic to each frame

        """
        logic_mode = self.interface_object.command_object.logic['continues_mode']
        max_classifications = self.interface_object.command_object.classifier['max_class']

        patch_list = self.interface_object.patches_list

        important_patch_list, icon_list = self.extract_signs(patch_list)

        if logic_mode:
            important_patch_list, icon_list = self.history_filter(important_patch_list, icon_list)

        important_patch_list = [patch.patch for patch in important_patch_list]

        self.interface_object.important_patches = important_patch_list[:max_classifications]
        self.interface_object.icon_list = icon_list[:max_classifications]

    def extract_signs(self, patches_list, class_threshhold=0.5):
        """read probabilities of all signs of all patches, apply threshhold
        and save all signs of a Frame in important_patch_list
        and their coresponding icons to icon_list.
        sort both lists


        Args:
            patches_list ([list of patch-objects]):
            class_threshhold (double): threshhold between 0 and 1
        """

        important_patch_list = []
        icon_list = []
        max_probabilities = []

        for patch in patches_list:
            max_index, maximum = Logic.max_index_calc(list(patch.probabilities))
            if maximum > class_threshhold:
                max_probabilities.append(maximum)
                patch.class_strings = self.signnames[max_index]
                patch.class_id = max_index
                important_patch_list.append(patch)
                icon_list.append(self.whole_icon_list[max_index])
        important_patch_list = self.sort_list_backward(important_patch_list, max_probabilities)
        icon_list = self.sort_list_backward(icon_list, max_probabilities)

        return important_patch_list, icon_list

    def history_filter(self, important_patch_list, icon_list, max_dist=50):
        """compare current classifications with earlier classifications to see
        if they make sense. Delete them if not.

        Args:
            important_patch_list (list of patch-objects)
            icon_list (list of images)
            max_dist (int): maximal pixel distance between signs detected earlier and now

        Returns:
            filtered_important_patch_list, filtered_icon_list
        """
        if not self.history:
            filtered_important_patch_list = important_patch_list
            filtered_icon_list = icon_list
        else:
            filtered_important_patch_list = []
            filtered_icon_list = []

            for index, new_patch in enumerate(important_patch_list):
                has_predecessor = False
                for old_patch in self.history:
                    same_class_id = new_patch.class_id == old_patch.class_id
                    x_position_near = abs(new_patch.position[0] - old_patch.position[0]) < max_dist
                    y_postion_near = abs(new_patch.position[1] - old_patch.position[1]) < max_dist
                    if same_class_id and x_position_near and y_postion_near:
                        has_predecessor = True
                        break
                if has_predecessor:
                    filtered_important_patch_list.append(new_patch)
                    filtered_icon_list.append(icon_list[index])

        self.history = important_patch_list
        return filtered_important_patch_list, filtered_icon_list

    @staticmethod
    def max_index_calc(liste):
        """

        Args:
            liste:

        Returns:

        """
        return liste.index(max(liste)), max(liste)

    @staticmethod
    def get_icon_list():
        """
        generate list containing all possible sign-icons

        Returns: icon_list

        """
        a_path = Path(__file__).resolve().parent.parent.parent
        dir_path = a_path / "data" / "icons"
        path_list = sorted(list(Path(dir_path).glob('**/*')))
        icon_list = [imageio.imread(path)[:, :, :3] for path in path_list]
        return icon_list

    @staticmethod
    def sort_list_backward(l_1, l_2):
        """sort l1 according to l2 (backward)

        Args:
            l1 ([type]): list
            l2 ([type]): list of numbers
        Returns: l1_sorted
        """
        l_1_sorted = [y for x, y in sorted(zip(l_2, l_1), key=lambda tub: -tub[0])]
        return l_1_sorted
