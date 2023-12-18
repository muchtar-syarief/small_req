import PySimpleGUI as sg
import adbutils
import uiautomator2 as u2


def get_devices() -> list[dict]:
    adb = adbutils.adb

    devices = adb.device_list()

    drivers: list[dict] = []
    for device in devices:
        driver = u2.connect(device.serial)
        drivers.append(driver.device_info)
    
    return [
        {
            "model": "asdasd",
            "serial": "qw123123"
        },
        {
            "model": "qweqweqwe",
            "serial": "asdasd123123123"
        }
    ]

logger = "{asctime} [ {device} ] : {msg}"

sg.theme("DarkTeal")


config_layout = [
        [
            sg.Text("Pilih device :"),
        ],
        [ 
            sg.Radio(text=d["model"], key=f"device_{i}", group_id="device", default=i==0) for i, d in enumerate(get_devices())
        ],
        [
            sg.Text("Masukkan komentar : ")
        ],
        [
            sg.Multiline(
                size=(60,15),
                no_scrollbar=True,
                key="comments",
            )
        ],
        [
            sg.Button("Run"),
            sg.Button("Cancel")
        ]
    ]

layout = [
    [
        sg.Column(
            config_layout
        ),
        sg.VSeparator(),
        sg.Multiline(
            no_scrollbar=True,
            size=(60, 30), 
            key="Logger",
        )
    ],
]

window = sg.Window('Window Title', layout, size=(960, 480))
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == "Run":
        window["comments"].update(value=f"{values['comments']} \n asu")
    print('You entered ', values, event)

window.close()