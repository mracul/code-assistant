import diff_match_patch as dmp_module

class DiffTool:
    """
    A tool for creating and applying diffs.
    """
    def __init__(self):
        self.dmp = dmp_module.diff_match_patch()

    def create_diff(self, text1, text2):
        """
        Creates a diff between two texts.
        """
        return self.dmp.diff_main(text1, text2)

    def apply_diff(self, diff, text):
        """
        Applies a diff to a text.
        """
        patches = self.dmp.patch_make(text, diff)
        new_text, _ = self.dmp.patch_apply(patches, text)
        return new_text
