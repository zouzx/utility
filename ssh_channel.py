class Channel(object):
    def __init__(self, host):
        self._host = host
        self._ssh_channel = None
        self._thread_group = None
        self._ret_data = None 
        self._ret_error = None

        print('Connecting to: {}({})'.format(host['hostname'], host['ip']))
        self._ssh_channel = self.create_channel(self._host)
        print("[Successful]")
    
    def create_channel(self, host):
        ip = host['ip']
        port = host['port']
        username = host['username']
        password = host['password']
        hostname = host['hostname']

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)
        return ssh

    def execute_commond(self, cmd):
        stdin, stdout, stderr = self._ssh_channel.exec_command(cmd)
        out = stdout.readlines()
        err = stderr.readlines()

        self._ret_data = ''.join(out)
        self._ret_error = ''.join(err)
        return cmd

    def submit_command_async(self, cmd):
        print("Submitting to [{}]: {}".format(self._host['hostname'], cmd))
        try:
            self._thread_group = threading.Thread(target=self.execute_commond, args=(cmd, ))
            self._thread_group.start()
        except:
            print("Error: cannot launching threads")
            exit(0)

    def query_command_async(self):
            self._thread_group.join()
            self._thread_group = None
            return self._ret_data, self._ret_error

    def __del__(self):
        print("Channel to {}:{} has been closed".format(self._host['hostname'], self._host['ip']))
        self._ssh_channel.close()
    
class SubThread(object):
    def __init__(self):
        self._p = None
        self._ret_data = None
        self._ret_error = None
    
    def local_execute(self, cmd):
        self._p = subprocess.run(cmd, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        self._ret_data = self._p.stdout
        self._ret_error = self._p.stderr
        return 
