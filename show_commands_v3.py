
import yaml
import argparse
import pprint
import threading
from netmiko import ConnectHandler
from getpass import getpass

class MyThread(threading.Thread):
  def __init__(self,device,commands,name):
    threading.Thread.__init__(self)
    self.device_name = name
    self.device = device
    self.commands = commands

  def run(self):
    #接続
    activete = ConnectHandler(**self.device)
    print("{}: Connect!".format(self.device_name))

    #コマンド実行
    with open('{}.log'.format(self.device_name),mode='w') as f:
      f.write("{}: Collecting\n".format(self.device_name))
      for command in self.commands[self.device['device_type']]['commands']:
          f.write("="*15+" {} ".format(command)+"="*15+"\n")
          output = activete.send_command(command)
          f.write("{}\n\n".format(output))
          print("{}: Get_{}".format(self.device_name,command))

    #切断
    activete.disconnect()
    print("{}: Disconnect!\n".format(self.device_name))

if __name__ == "__main__":
  username = input('ユーザ名：')
  password = getpass("パスワード: ")
  threads = [] 

  #外部ファイルインポート
  parser = argparse.ArgumentParser(prog='ACI')
  parser.add_argument('-t','--testbed', dest='yaml_file',help='Please select a file in Yaml format')
  parser.add_argument('-c','--config', dest='config_file',help='Please select a file in Yaml format')
  args = parser.parse_args()

  #loginに必要な情報が記載されたYamlファイルLoad
  hosts_data = open(args.yaml_file,"r")
  hosts = yaml.safe_load(hosts_data)

  commands_data = open(args.config_file,"r")
  commands = yaml.safe_load(commands_data)
  for host in hosts:
    device = {
        "device_type": host['device_type'],
        "ip": host['ip'],
        "username": username,
        "password": password,
        "port": host['port']
        #"secret": host['sercret']
        }
    t = MyThread(device,commands,host['name'])
    t.start()
    threads.append(t)

  for t in threads:
    t.join()
