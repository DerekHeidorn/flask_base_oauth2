
class GlobalMessages:

    global_success_msgs = list()
    global_info_msgs = list()
    global_warning_msgs = list()
    global_error_msgs = list()
    has_global_msgs = (len(global_success_msgs) > 0
                       or len(global_info_msgs) > 0
                       or len(global_warning_msgs) > 0
                       or len(global_error_msgs) > 0
                       )

    def add_global_success_msg(self, msg):
        self.global_success_msgs.append(msg)

    def add_global_info_msg(self, msg):
        self.global_info_msgs.append(msg)

    def add_global_warning_msg(self, msg):
        self.global_warning_msgs.append(msg)

    def add_global_error_msg(self, msg):
        self.global_error_msgs.append(msg)
