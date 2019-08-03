import os
import shutil
from datetime import date
import uuid

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
Base_path, app_name = os.path.split(APP_ROOT)

file_name = "/inventory.db"
SQLITE_PATH = Base_path + file_name
Desktop = os.path.expanduser("~/Desktop")

CLIENT_MAC_ADDRESS = "34-E6-AD-53-39-C8"


def database_backup_func():
    destination_dir = Desktop + "/backupInventory/"
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    copy_destination_path = destination_dir + "inventory_" + str(date.today()) + ".db"
    shutil.copyfile(SQLITE_PATH, copy_destination_path)
    return "complete backup"


def get_mac():
  mac_num = hex(uuid.getnode()).replace('0x', '').upper()
  mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
  return mac


def check_mac_security():
    pc_mac = get_mac()
    client_mac = CLIENT_MAC_ADDRESS.strip()

    if pc_mac == client_mac:
        return True
    else:
        return False


def pager(total_row=None, item_per_page=None):
    pages = {}
    total_page = total_row / item_per_page

    if total_row % item_per_page != 0 and total_page > 1:
        total_page += 1
    for page in range(1, int(total_page) + 1):
        m = page - 1
        pages[page] = item_per_page * m
    return pages


def api_processing(queryset):
    all_data = []
    for item in queryset:
        data = item.__dict__
        data.pop("_sa_instance_state")
        all_data.append(data)
    return all_data


def profit_calculate(purchase_price, sales_price, total_unit):
    price_dff = sales_price - purchase_price
    earning = price_dff*total_unit
    return earning

if __name__ == '__main__':
    print(check_mac_security())




