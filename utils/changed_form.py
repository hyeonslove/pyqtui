class Windows:
    window_list = {}
    opend_list = {}

    @staticmethod
    def changedWindow(pres_form, chagned_form, args=None):
        if pres_form is not None:
            pres_form.close()

        # 한번이라도 안열리면 init을 진행
        if chagned_form not in Windows.opend_list:
            Windows.opend_list[chagned_form] = None
            Windows.window_list[chagned_form].init(args)
        Windows.window_list[chagned_form].show()  # showMaximized()
        # Windows.window_list[chagned_form].exec_()
