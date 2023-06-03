import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QPushButton, QTextEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPen, QColor, QFont, QPixmap, QBrush

class Router:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.data = "Data not found"

class NetworkSimulation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Simulation")
        self.resize(600, 400)

        # Create the graphics view and scene
        self.view = QGraphicsView()
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

        # Set the background image
        background_image = QPixmap("energy.png")
        background_brush = QBrush(background_image.scaled(self.view.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.scene.setBackgroundBrush(background_brush)

        # Create routers
        self.router1 = Router("Router 1", 50, 50)
        self.router2 = Router("Router 2", 200, 150)
        self.router3 = Router("Router 3", 350, 250)

        # Create the base station
        self.base_station = Router("Base Station", 500, 50)

        # Create the user
        self.user = Router("User", 50, 250)

        # Add routers and user to the scene
        router1_icon = QPixmap("rout.png")
        router1_item = self.scene.addPixmap(router1_icon.scaled(60, 60))
        router1_item.setPos(self.router1.x, self.router1.y)

        router2_icon = QPixmap("rout.png")
        router2_item = self.scene.addPixmap(router2_icon.scaled(60, 60))
        router2_item.setPos(self.router2.x, self.router2.y)

        router3_icon = QPixmap("rout.png")
        router3_item = self.scene.addPixmap(router3_icon.scaled(60, 60))
        router3_item.setPos(self.router3.x, self.router3.y)

        base_station_icon = QPixmap("bs.png")
        base_station_item = self.scene.addPixmap(base_station_icon.scaled(60, 60))
        base_station_item.setPos(self.base_station.x, self.base_station.y)

        # Add router names
        self.scene.addText(self.router1.name, QFont("Arial", 10)).setPos(self.router1.x + 10, self.router1.y + 70)
        self.scene.addText(self.router2.name, QFont("Arial", 10)).setPos(self.router2.x + 10, self.router2.y + 70)
        self.scene.addText(self.router3.name, QFont("Arial", 10)).setPos(self.router3.x + 10, self.router3.y + 70)

        # Add base station and user names
        self.scene.addText(self.base_station.name, QFont("Arial", 10)).setPos(self.base_station.x + 10, self.base_station.y + 70)
        self.scene.addText(self.user.name, QFont("Arial", 10)).setPos(self.user.x + 10, self.user.y + 70)

        # Add computer icon for the user
        computer_icon = QPixmap("comp.png")
        user_item = self.scene.addPixmap(computer_icon.scaled(60, 60))
        user_item.setPos(self.user.x, self.user.y)

        # Create lines connecting the routers and base station
        self.router_base_lines = []
        for router in [self.router1, self.router2, self.router3]:
            line = self.scene.addLine(
                self.base_station.x + 40, self.base_station.y, router.x + 40, router.y + 60, QPen(Qt.darkCyan, 3)
            )
            self.router_base_lines.append(line)

        # Create line connecting the user and router 1
        self.user_router_line = self.scene.addLine(
            self.user.x + 40, self.user.y + 60, self.router1.x + 40, self.router1.y, QPen(Qt.black, 3)
        )

        # Create the send request button
        self.send_request_button = QPushButton("Send Request", self)
        self.send_request_button.setGeometry(250, 350, 100, 30)
        self.send_request_button.clicked.connect(self.send_request)

        # Create the text output box
        self.text_output = QTextEdit(self)
        self.text_output.setGeometry(400, 200, 180, 150)
        self.text_output.setReadOnly(True)

        # Create the CS box for Router 1
        self.cs_box = self.scene.addRect(self.router1.x + 10, self.router1.y + 110, 80, 40, QPen(Qt.black, 2), Qt.white)
        self.scene.addText("CS", QFont("Arial", 10)).setPos(self.router1.x + 30, self.router1.y + 130)

        # Create the FIB box for Router 1
        self.fib_box = self.scene.addRect(self.router1.x + 110, self.router1.y + 110, 80, 40, QPen(Qt.black, 2), Qt.white)
        self.scene.addText("FIB", QFont("Arial", 10)).setPos(self.router1.x + 130, self.router1.y + 130)

        # Create the PIT box for Router 1
        self.pit_box = self.scene.addRect(self.router1.x + 210, self.router1.y + 110, 80, 40, QPen(Qt.black, 2), Qt.white)
        self.scene.addText("PIT", QFont("Arial", 10)).setPos(self.router1.x + 230, self.router1.y + 130)

    def send_request(self):
        # Change the color of the user-router line to green and make it bold
        pen = QPen(Qt.green, 3)
        self.user_router_line.setPen(pen)

        # Change the color of the CS box to green
        self.cs_box.setBrush(QBrush(Qt.green))

        # Print "Request not found" to the text output box
        self.text_output.append("Request not found")

        # Create a timer to change the CS box color back to white and change the PIT box color to red after 2 seconds
        timer1 = QTimer(self)
        timer1.timeout.connect(self.change_to_red)
        timer1.setSingleShot(True)
        timer1.start(5000)

    def change_to_red(self):
        # Change the color of the CS box back to white
        self.cs_box.setBrush(QBrush(Qt.white))

        # Change the color of the PIT box to red
        self.pit_box.setBrush(QBrush(Qt.red))

        # Print "Forwarding request to server" to the text output box
        self.text_output.append("Forwarding request to server")

        # Create a timer to change the line color of router 1 and base station to red after 2 seconds
        timer2 = QTimer(self)
        timer2.timeout.connect(self.change_router_base_color)
        timer2.setSingleShot(True)
        timer2.start(5000)

    def change_router_base_color(self):
    # Change the color of the line connecting router 1 and base station to red
        pen = QPen(Qt.red, 3)
        self.router_base_lines[0].setPen(pen)  # Change only the line between router 1 and base station

    # Create a timer to update all 3 routers with a violet line and print "Router updated with request" after 2 seconds
        timer3 = QTimer(self)
        timer3.timeout.connect(self.update_routers)
        timer3.setSingleShot(True)
        timer3.start(5000)

    def update_routers(self):
        # Change the line color of router 1 and base station to violet
        pen = QPen(QColor(138, 43, 226), 3)
        for line in self.router_base_lines:
            line.setPen(pen)

        # Print "Router updated with request" to the text output box
        self.text_output.append("Router updated with request")

        # Create a timer to change the line color of user and router 1 to blue after 2 seconds
        timer4 = QTimer(self)
        timer4.timeout.connect(self.deliver_request)
        timer4.setSingleShot(True)
        timer4.start(5000)

    def deliver_request(self):
        # Change the line color of user and router 1 to blue
        pen = QPen(Qt.blue, 3)
        self.user_router_line.setPen(pen)

        # Print "Request delivered" to the text output box
        self.text_output.append("Request delivered")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    simulation = NetworkSimulation()
    simulation.show()
    sys.exit(app.exec_())
