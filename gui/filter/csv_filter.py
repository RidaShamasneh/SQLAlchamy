from gui.filter.basic_filter_qmenu import BasicFilterQMenu


class CSVFilter(object):
    def __init__(self, filter_unique_items=None):
        super(CSVFilter, self).__init__()
        self.__filter_unique_items = filter_unique_items  # header index: unique values
        self.__filter_menus = None  # dict header index: filter_qmenu
        self.__cached_states = None

    @property
    def filter_menus(self):
        return self.__filter_menus

    @filter_menus.setter
    def filter_menus(self, val):
        self.__filter_menus = val

    @property
    def filter_unique_items(self):
        return self.__filter_unique_items

    @filter_unique_items.setter
    def filter_unique_items(self, val):
        self.__filter_unique_items = val

    def filter_menus_enabled(self, is_enabled):
        for header_index, filter_qmenu in self.__filter_menus.iteritems():
            self.__filter_menus[header_index].filter_qmenu_enabled(is_enabled)

    def update_cached_states(self):
        for header_index, filter_qmenu in self.__filter_menus.iteritems():
            self.__cached_states[header_index] = filter_qmenu.get_filter_menu_state()

    def get_csv_unique_filter_values(self):
        return self.__filter_unique_items.iterkeys()

    def construct_filter_menus(self):
        self.__filter_menus = {}
        self.__cached_states = {}
        for csv_column_index, csv_column_unique_values in self.__filter_unique_items.iteritems():
            # create checkboxes menu
            filter_qmenu = BasicFilterQMenu(unique_filter_values_list=csv_column_unique_values)
            self.__filter_menus[csv_column_index] = filter_qmenu
            self.__cached_states[csv_column_index] = filter_qmenu.get_filter_menu_state()

    def is_at_least_one_filter_menu_items_all_unchecked(self):
        '''
        Checks if at least one filer menu items are all unchecked
        :return: boolean
        '''
        for filter_qmenu in self.__filter_menus.itervalues():
            if filter_qmenu.is_all_filter_menu_unchecked():
                return True
        return False

    def is_all_filter_menus_checked(self):
        '''
        Checks if all filter items are checked.
        :return: boolean
        '''
        for filter_qmenu in self.__filter_menus.itervalues():
            if not filter_qmenu.is_all_filter_menu_checked():
                return False
        return True

    def reset_filter_menus(self, is_checked=True):
        for index, filter_qmenu in self.__filter_menus.iteritems():
            filter_qmenu.reset_filter_menu(is_checked)
        self.update_cached_states()

    def reset_filter_menu_at_index_from_cached_state(self, index):
        for checkbox_index in self.__filter_menus[index].filters_model.iterkeys():
            self.__filter_menus[index].set_filter_item(checkbox_index, self.__cached_states[index][checkbox_index])

    def __get_filter_menues_state(self):
        states = {}
        for csv_column_index, filter_qmenu in self.__filter_menus.iteritems():
            states[csv_column_index] = filter_qmenu.get_filter_menu_state()
        return states

    def is_state_changed(self):
        return self.__get_filter_menues_state().items() == self.__cached_states.items()

    def get_enabled_checkboxes_dict(self):
        dict = {}
        for header_index, filter_qmenu in self.__filter_menus.iteritems():
            result = filter_qmenu.get_enabled_checkboxes_actual_text_list()
            if result:
                dict[header_index] = result
        return dict

    def reset_filter_menu_at_index(self, column_index, is_checked=True):
        self.__filter_menus[column_index].reset_filter_menu(is_checked)
        self.update_cached_states()