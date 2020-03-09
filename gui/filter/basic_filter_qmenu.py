from PyQt4 import QtCore
from PyQt4.QtGui import QCheckBox
from gui.filter.filter_constants import FilterConstants
from gui.filter.CustomQMenu import CustomQMenu


class BasicFilterQMenu(CustomQMenu):
    def __init__(self, unique_filter_values_list):
        super(BasicFilterQMenu, self).__init__()
        self._filters_model = None
        self._setup_ui()
        self._filters_model = {}
        self.__unique_filter_values_list = unique_filter_values_list
        self.__select_all_checkbox = None
        self.__create_menu()

    def filter_qmenu_enabled(self, is_enabled):
        self.__select_all_checkbox.setEnabled(is_enabled)
        for filter_checkbox in self._filters_model.itervalues():
            filter_checkbox.setEnabled(is_enabled)
        self._ok_cancel_dialog_button.setEnabled(is_enabled)

    def set_filter_item(self, filter, state):
        if filter == FilterConstants.SELECT_ALL:
            self.__select_all_checkbox.setChecked(state)
            return

        self._filters_model[filter].setChecked(state)

    def __create_menu(self):
        '''
        Creates a filter qmenu and connects filter_model signals
        '''
        self.__select_all_checkbox = QCheckBox(FilterConstants.SELECT_ALL, self)
        self.__select_all_checkbox.setStyleSheet(FilterConstants.SELECT_ALL_CSS)
        self._scroll_layout.addWidget(self.__select_all_checkbox)
        for filter_item in self.__unique_filter_values_list:
            if filter_item == 'None':  # Empty String are retreived as None str # todo:needs better handling
                ui_text = FilterConstants.BLANKS_STRING
            else:  # whitespaces
                ui_text = filter_item.strip()
            '''
            To prevent duplicates of creating checkboxes with same ui_text but different actual_texts
            '''
            if ui_text not in self._filters_model.keys():
                checkbox = QCheckBox(ui_text, self)
                checkbox.stateChanged.connect(self.__checkbox_state_changed_handler)
                self._scroll_layout.addWidget(checkbox)
                self._filters_model[ui_text] = checkbox
        self.__select_all_checkbox.stateChanged.connect(
            self.__select_all_checkbox_state_changed_handler)
        self.__select_all_checkbox.setChecked(True)
        super(BasicFilterQMenu, self)._create_menu()

    def reset_filter_menu(self, is_checked=True):
        '''
        This method resets filter menu items (__select_all_checkbox and __filter_model) to the given state
        Only setting '__select_all_checkbox' to the given state is sufficient to reset the menu;
            as the 'select_all' signal will handle all _filters_model items state
        '''
        self.__select_all_checkbox.setChecked(is_checked)

    def get_select_all_state(self):
        '''
        get the state of select_all_checkbox
        :return: boolean
        '''
        return self.__select_all_checkbox.isChecked()

    def get_enabled_checkboxes_actual_text_list(self):
        dict = {}
        for filter_index, filter_checkbox in self._filters_model.iteritems():
            if filter_checkbox.isChecked() and not self.get_select_all_state():
                dict[filter_index] = filter_checkbox.text()
        return dict

    def __get_filter_model_state(self, is_checked=None):
        '''
        get the state of the filter_model checkbox items according to 'is_checked' value.
        if is_checked is None it returns all the checkboxes regardless the check state
        :return: dict {checkbox_text: is_checked}
        '''
        states = {}
        for filter_index, filter_checkbox in self._filters_model.iteritems():
            if not is_checked:
                states[filter_index] = filter_checkbox.isChecked()
            elif is_checked and filter_checkbox.isChecked():
                states[filter_index] = filter_checkbox.isChecked()
            elif not is_checked and not filter_checkbox.isChecked():
                states[filter_index] = filter_checkbox.isChecked()
        return states

    def get_filter_menu_state(self, is_checked=None):
        '''
        get the state of the checkboxes in the filter_qmenu including select_all_checkbox (regardless if it is checked or not)
        'is_checked' param is applied on filter_model checkboxes
        if is_checked is None it returns all the checkboxes regardless the check state
        :return: dict {checkbox_text: is_checked}
        '''
        states = self.__get_filter_model_state(is_checked=is_checked)
        states[FilterConstants.SELECT_ALL] = self.get_select_all_state()
        return states

    def is_all_filter_menu_unchecked(self):
        if True in self.get_filter_menu_state(is_checked=False).values():
            return False
        else:
            return True

    def is_all_filter_menu_checked(self):
        if False in self.__get_filter_model_state(is_checked=None).values():
            return False
        return True

    def __select_all_checkbox_state_changed_handler(self, state):
        for checkbox in self._filters_model.itervalues():
            checkbox.blockSignals(True)
            checkbox.setCheckState(state)
            checkbox.blockSignals(False)

    def __checkbox_state_changed_handler(self):
        self.__select_all_checkbox.blockSignals(True)
        if self.is_all_filter_menu_checked():
            self.__select_all_checkbox.setChecked(QtCore.Qt.Checked)
        else:
            self.__select_all_checkbox.setChecked(QtCore.Qt.Unchecked)
        self.__select_all_checkbox.blockSignals(False)

    @property
    def filters_model(self):
        return self._filters_model