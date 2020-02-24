import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate(
    '/home/pi/me310/me310_cobot/newagent-xvxsxk-firebase-adminsdk-oxncw-2245188408.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://newagent-xvxsxk.firebaseio.com/'
})

class CobotInfo:
    def __init__(self,):
        # As an admin, the app has access to read and write all data, regradless of Security Rules
        self.machine_status_ref = db.reference("machine_status")
        self.robot_status_ref = db.reference("robot_status")
        self.alert_status_ref = db.reference("alert_status")
        self.robot_name = ["A", "B", "C"]
        self.machine_name = ["A", "B", "C"]
        self.size_name = ["big", "middle", "small"]
        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://newagent-xvxsxk.firebaseio.com/'
        }, 'other')
    
    def update_job_recommendation(self,):
        job = self.machine_status_ref.child("job").get()
        time_left = None
        type_name = None
        machine_name = None
        for machine in self.machine_name:
            if type_name in ["INSTALL", "CMD"]:
                break
            for size in self.size_name:
                tmp_time, tmp_install = self.read_machine_status(machine, size)
                if not tmp_install:
                    # TODO: remove hack
                    machine_name, time_left = machine, 20
                    type_name = "INSTALL"
                    break
                if tmp_time == 0 and tmp_install:
                    machine_name, time_left = machine, 0
                    type_name = "CMD"
                    break
                if time_left is None or tmp_time < time_left:
                    type_name = "FUT_RM"
                    machine_name, time_left = machine, tmp_time
        job["time_left"] = time_left
        job["type"] = type_name
        job["machine"] = machine_name
        self.machine_status_ref.child("job").update(job)

    def update_robot_availability(self, ):
        # resolve all the conflicts on the cloud
        # for alert system, robot system, machine system
        num_available = 0
        time_remain = None
        for robot in self.robot_name:
            _, status, time = self.read_robot_status(robot)
            if status == 0:
                num_available += 1
            elif time_remain is None or time < time_remain:
                time_remain = time
        self._set_num_available_robot(num_available)
        self._set_robot_remain_time(time_remain)

    def read_machine_status(self, machine_name="A", size="big"):
        # input: machine name: "A", "B", "C"
        # size: "big", "middle", "small"
        # output the time (min) the coil can last
        # and whether coil has been installed by the human
        if machine_name not in self.machine_name:
            raise ValueError("{} is not available".format(machine_name))
        if size not in self.size_name:
            raise ValueError("{} is not available".format(size))
        machine = self.machine_status_ref.child(machine_name).get()
        return machine[size], machine["{}_installed".format(size)]

    def write_machine_status(self, 
        machine_name="A", size="big", 
        time_remain=None, installed=None):
        # input: machine name: "A", "B", "C"
        # size: "big", "middle", "small"
        # set the time (min) the coil can last
        # and whether coil has been installed by the human
        if machine_name not in self.machine_name:
            raise ValueError("Machine {} is not available".format(machine_name))
        if size not in self.size_name:
            raise ValueError("Machine {} is not available".format(size))
        machine = self.machine_status_ref.child(machine_name).get()
        if time_remain is not None:
            machine[size] = time_remain
        if type(installed) is bool:
            machine["{}_installed".format(size)] = installed
        self.machine_status_ref.child(machine_name).update(machine)

    def get_num_available_robot(self):
        return self.robot_status_ref.child("num_available").get()

    def _set_num_available_robot(self, num):
        return self.robot_status_ref.update({
                "num_available": num
            })

    def get_robot_remain_time(self):
        return self.robot_status_ref.child("time_remain").get()

    def _set_robot_remain_time(self, time_remain):
        return self.robot_status_ref.update({
                "time_remain": time_remain
            })

    def read_robot_status(self, robot_name="A"):
        # input: robot name: "A", "B", "C"
        # output the coil size is currently carrying
        # the status robot is 0: free, 1: busy, 2: interrupted
        # estimiated time to finish current task
        if robot_name not in self.robot_name:
            raise ValueError("Robot {} is not available".format(robot_name))
        robot = self.robot_status_ref.child(robot_name).get()
        return robot["size"], robot["status"], robot["finish_time"]

    def write_robot_status(
        self, robot_name="A", size_cur=None, 
        status_cur=None, finish_time=None):
        # input: robot name: "A", "B", "C"
        # output the coil size is currently carrying
        # the status robot is 0: free, 1: busy, 2: interrupted
        # estimiated time to finish current task
        if robot_name not in self.robot_name:
            raise ValueError("Robot {} is not available".format(robot_name))
        robot = self.robot_status_ref.child(robot_name).get()
        if size_cur is not None:
            robot["size"] = size_cur
        if status_cur is not None:
            robot["status"] = status_cur
        if finish_time is not None:
            robot["finish_time"] = finish_time
        self.robot_status_ref.child(robot_name).update(robot)
        self.update_robot_availability()

    def read_safe_status(self, ):
        safe_bool = self.alert_status_ref.child("safe_bool").get()
        safe_dir = self.alert_status_ref.child("safe_dir").get()
        safe_part = self.alert_status_ref.child("safe_part").get()
        return safe_bool, safe_dir, safe_part

    def _update_safe_status(self, safe_bool, safe_dir, safe_part):
        self.alert_status_ref.child("safe_bool").update(safe_bool)
        self.alert_status_ref.child("safe_dir").update(safe_dir)
        self.alert_status_ref.child("safe_part").update(safe_part)

    def update_alert_status(self, body_lists, theta, dist_thres=6):
        # body_lists: {
        #   "head": [x, y, z, quaternion]
        #   ...
        # }
        # theta: the angle of the kinect respect to human
        # 0 means right in the front
        safe_bool = True
        if abs(theta) < 20:
            safe_dir = "Front"
        elif abs(theta) > 160:
            safe_dir = "Back"
        elif abs(theta) > 0:
            safe_dir = "Right"
        elif abs(theta) < 0:
            safe_dir = "Left"
        for key, l in body_lists:
            if sqrt(l[0] * l[0] + l[1] * l[1]) < dist_thres:
                safe_part = key
                safe_bool = False
                break
        # TODO: update the coords in the cloud
        self._update_safe_status(body_lists, safe_dir, safe_part)


def main():
    cobot = CobotInfo()
    print(cobot.read_machine_status())
    # cobot.write_machine_status(time_remain=0, installed=False)
    # print(cobot.read_robot_status())
    # cobot.write_robot_status(status_cur=2)
    cobot.write_robot_status(status_cur=1, robot_name="B")
    # cobot.update_job_recommendation()


if __name__ == '__main__':
    pass
    #main()


g_cobot_info = CobotInfo()

