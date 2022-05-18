class Windows:
    window_list = {}

    @staticmethod
    def changedWindow(pres_form, chagned_form):
        if pres_form is not None:
            pres_form.close()
        Windows.window_list[chagned_form].init()
        Windows.window_list[chagned_form].show()  # showMaximized()
        Windows.window_list[chagned_form].exec_()
