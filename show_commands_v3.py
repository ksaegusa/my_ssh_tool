from netmiko import ConnectHandler
import yaml
import argparse
from getpass import getpass
import pprint
import threading

class MyThread(threading.Thread):
  def __init__(self,device,commands):
    threading.Thread.__init__(self)
    self.device = device
    self.commands = commands

  def run(self):
    #接続
    activete = ConnectHandler(**device)
    print("{}: Connect!".format(self.device['name']))

      #コマンド実行
    with open('{}.log'.format(self.device['name']),mode='w') as f:
      f.write("{}: Collecting\n".format(self.device['name']))
      for command in self.commands[self.device['device_type']]['commands']:
          f.write("="*15+" {} ".format(command)+"="*15+"\n")
          output = activete.send_command(command)
          f.write("{}\n\n".format(output))
          print("{}: Get_{}".format(self.device['name'],command))

    #切断
    activete.disconnect()
    print("{}: Disconnect!\n".format(self.device['name']))

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
        "name": host['name'],
        "device_type": host['device_type'],
        "ip": host['ip'],
        "username": username,
        "password": password,
        #"secret": host['sercret']
        }
    t = MyThread(device,commands)
    t.start()
    threads.append(t)

  for t in threads:
    t.join()
